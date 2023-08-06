# -*- encoding: utf-8 -*-
# @Author: Yihuai Lan
# @Time: 2021/08/21 04:33:54
# @File: multiencdec.py

import copy
import random

import torch
import numpy as np
from torch import nn
from torch.nn import functional as F

from mwptoolkit.module.Encoder.graph_based_encoder import GraphBasedMultiEncoder, NumEncoder
from mwptoolkit.module.Decoder.tree_decoder import TreeDecoder
#from mwptoolkit.module.Decoder.rnn_decoder import AttentionalRNNDecoder
from mwptoolkit.module.Layer.layers import TreeAttnDecoderRNN
from mwptoolkit.module.Layer.tree_layers import NodeGenerater, SubTreeMerger, TreeNode, TreeEmbedding
from mwptoolkit.module.Layer.tree_layers import Prediction, GenerateNode, Merge
from mwptoolkit.module.Embedder.basic_embedder import BaiscEmbedder
from mwptoolkit.module.Strategy.beam_search import TreeBeam, Beam
from mwptoolkit.loss.masked_cross_entropy_loss import MaskedCrossEntropyLoss, masked_cross_entropy
from mwptoolkit.utils.enum_type import SpecialTokens, NumMask
from mwptoolkit.utils.utils import copy_list


class MultiEncDec(nn.Module):
    """
    Reference:
        Shen et al. "Solving Math Word Problems with Multi-Encoders and Multi-Decoders" in COLING 2020.
    """
    def __init__(self, config, dataset):
        super(MultiEncDec, self).__init__()
        self.device = config['device']
        self.USE_CUDA = True if self.device == torch.device('cuda') else False
        self.rnn_cell_type = config['rnn_cell_type']
        self.embedding_size = config['embedding_size']
        self.hidden_size = config['hidden_size']
        self.n_layers = config['num_layers']
        self.hop_size = config['hop_size']
        self.teacher_force_ratio = config['teacher_force_ratio']
        self.beam_size = config['beam_size']
        self.max_out_len = config['max_output_len']
        self.dropout_ratio = config['dropout_ratio']

        self.operator_nums = dataset.operator_nums
        self.generate_nums = len(dataset.generate_list)
        self.num_start1 = dataset.num_start1
        self.num_start2 = dataset.num_start2
        self.input1_size = len(dataset.in_idx2word_1)
        self.input2_size = len(dataset.in_idx2word_2)
        self.output2_size = len(dataset.out_idx2symbol_2)
        self.unk1 = dataset.out_symbol2idx_1[SpecialTokens.UNK_TOKEN]
        self.unk2 = dataset.out_symbol2idx_2[SpecialTokens.UNK_TOKEN]
        self.sos2 = dataset.out_symbol2idx_2[SpecialTokens.SOS_TOKEN]
        self.eos2 = dataset.out_symbol2idx_2[SpecialTokens.EOS_TOKEN]

        self.out_symbol2idx1 = dataset.out_symbol2idx_1
        self.out_idx2symbol1 = dataset.out_idx2symbol_1
        self.out_symbol2idx2 = dataset.out_symbol2idx_2
        self.out_idx2symbol2 = dataset.out_idx2symbol_2
        generate_list = dataset.generate_list
        self.generate_list = [self.out_symbol2idx1[symbol] for symbol in generate_list]
        self.mask_list = NumMask.number

        try:
            self.out_sos_token1 = self.out_symbol2idx1[SpecialTokens.SOS_TOKEN]
        except:
            self.out_sos_token1 = None
        try:
            self.out_eos_token1 = self.out_symbol2idx1[SpecialTokens.EOS_TOKEN]
        except:
            self.out_eos_token1 = None
        try:
            self.out_pad_token1 = self.out_symbol2idx1[SpecialTokens.PAD_TOKEN]
        except:
            self.out_pad_token1 = None
        try:
            self.out_sos_token2 = self.out_symbol2idx2[SpecialTokens.SOS_TOKEN]
        except:
            self.out_sos_token2 = None
        try:
            self.out_eos_token2 = self.out_symbol2idx2[SpecialTokens.EOS_TOKEN]
        except:
            self.out_eos_token2 = None
        try:
            self.out_pad_token2 = self.out_symbol2idx2[SpecialTokens.PAD_TOKEN]
        except:
            self.out_pad_token2 = None
        # Initialize models
        embedder = nn.Embedding(self.input1_size, self.embedding_size)
        in_embedder = self._init_embedding_params(dataset.trainset, dataset.in_idx2word_1, config['embedding_size'], embedder)

        self.encoder = GraphBasedMultiEncoder(input1_size=self.input1_size,
                                              input2_size=self.input2_size,
                                              embed_model=in_embedder,
                                              embedding1_size=self.embedding_size,
                                              embedding2_size=self.embedding_size // 4,
                                              hidden_size=self.hidden_size,
                                              n_layers=self.n_layers,
                                              hop_size=self.hop_size)
        self.numencoder = NumEncoder(node_dim=self.hidden_size, hop_size=self.hop_size)
        self.predict = Prediction(hidden_size=self.hidden_size, op_nums=self.operator_nums, input_size=self.generate_nums)
        self.generate = GenerateNode(hidden_size=self.hidden_size, op_nums=self.operator_nums, embedding_size=self.embedding_size)
        self.merge = Merge(hidden_size=self.hidden_size, embedding_size=self.embedding_size)
        self.decoder = TreeAttnDecoderRNN(self.hidden_size, self.embedding_size, self.output2_size, self.output2_size, self.n_layers, self.dropout_ratio)

        self.loss = MaskedCrossEntropyLoss()

    def _init_embedding_params(self, train_data, vocab, embedding_size, embedder):
        sentences = []
        for data in train_data:
            sentence = []
            for word in data['question']:
                if word in vocab:
                    sentence.append(word)
                else:
                    sentence.append(SpecialTokens.UNK_TOKEN)
            sentences.append(sentence)
        from gensim.models import word2vec
        model = word2vec.Word2Vec(sentences, vector_size=embedding_size, min_count=1)
        emb_vectors = []
        pad_idx = vocab.index(SpecialTokens.PAD_TOKEN)
        for idx in range(len(vocab)):
            if idx != pad_idx:
                emb_vectors.append(np.array(model.wv[vocab[idx]]))
            else:
                emb_vectors.append(np.zeros((embedding_size)))
        emb_vectors = np.array(emb_vectors)
        embedder.weight.data.copy_(torch.from_numpy(emb_vectors))

        return embedder

    def calculate_loss(self, batch_data):
        """Finish forward-propagating, calculating loss and back-propagation.
        
        Args:
            batch_data (dict): one batch data.
        
        Returns:
            float: loss value.
        """
        input1_var = batch_data['input1']
        input2_var = batch_data['input2']
        input_length = batch_data['input1 len']
        target1 = batch_data['output1']
        target1_length = batch_data['output1 len']
        target2 = batch_data['output2']
        target2_length = batch_data['output2 len']
        num_stack_batch = batch_data['num stack']
        num_size_batch = batch_data['num size']
        generate_list = self.generate_list
        num_pos_batch = batch_data['num pos']
        num_order_batch = batch_data['num order']
        parse_graph = batch_data['parse graph']
        equ_mask1 = batch_data['equ mask1']
        equ_mask2 = batch_data['equ mask2']

        unk1 = self.unk1
        unk2 = self.unk2
        num_start1 = self.num_start1
        num_start2 = self.num_start2
        sos2 = self.sos2
        loss = self.train_double(input1_var,
                                 input2_var,
                                 input_length,
                                 target1,
                                 target1_length,
                                 target2,
                                 target2_length,
                                 num_stack_batch,
                                 num_size_batch,
                                 generate_list,
                                 unk1,
                                 unk2,
                                 num_start1,
                                 num_start2,
                                 sos2,
                                 num_pos_batch,
                                 num_order_batch,
                                 parse_graph,
                                 beam_size=5,
                                 use_teacher_forcing=0.83,
                                 english=False)
        if self.USE_CUDA:
            torch.cuda.empty_cache()
        return loss

    def model_test(self, batch_data):
        """Model test.
        
        Args:
            batch_data (dict): one batch data.
        
        Returns:
            tuple(str,list,list): predicted type, predicted equation, target equation.
        """
        input1_var = batch_data['input1']
        input2_var = batch_data['input2']
        input_length = batch_data['input1 len']
        target1 = batch_data['output1']
        target1_length = batch_data['output1 len']
        target2 = batch_data['output2']
        target2_length = batch_data['output2 len']
        num_stack_batch = batch_data['num stack']
        num_size_batch = batch_data['num size']
        generate_list = self.generate_list
        num_pos_batch = batch_data['num pos']
        num_order_batch = batch_data['num order']
        parse_graph = batch_data['parse graph']
        equ_mask1 = batch_data['equ mask1']
        equ_mask2 = batch_data['equ mask2']
        num_list = batch_data['num list']

        unk1 = self.unk1
        unk2 = self.unk2
        num_start1 = self.num_start1
        num_start2 = self.num_start2
        sos2 = self.sos2
        eos2 = self.eos2

        result_type, test_res, score = self.evaluate_double(input1_var,
                                                            input2_var,
                                                            input_length,
                                                            generate_list,
                                                            num_start1,
                                                            sos2,
                                                            eos2,
                                                            num_pos_batch,
                                                            num_order_batch,
                                                            parse_graph,
                                                            beam_size=5,)
        if result_type == "tree":
            output1 = self.convert_idx2symbol1(test_res, num_list[0], copy_list(num_stack_batch[0]))
            targets1 = self.convert_idx2symbol1(target1[0], num_list[0], copy_list(num_stack_batch[0]))
            if self.USE_CUDA:
                torch.cuda.empty_cache()
            return result_type, output1, targets1
        else:
            output2 = self.convert_idx2symbol2(torch.tensor(test_res).view(1, -1), num_list, copy_list(num_stack_batch))
            targets2 = self.convert_idx2symbol2(target2, num_list, copy_list(num_stack_batch))
            if self.USE_CUDA:
                torch.cuda.empty_cache()
            return result_type, output2, targets2

    def train_double(self,
                     input1_batch,
                     input2_batch,
                     input_length,
                     target1_batch,
                     target1_length,
                     target2_batch,
                     target2_length,
                     num_stack_batch,
                     num_size_batch,
                     generate_num1_ids,
                     unk1,
                     unk2,
                     num_start1,
                     num_start2,
                     sos2,
                     num_pos_batch,
                     num_order_batch,
                     parse_graph_batch,
                     beam_size=5,
                     use_teacher_forcing=0.83,
                     english=False):
        # sequence mask for attention
        seq_mask = []
        max_len = max(input_length)
        for i in input_length:
            seq_mask.append([0 for _ in range(i)] + [1 for _ in range(i, max_len)])
        seq_mask = torch.ByteTensor(seq_mask)

        num_mask = []
        max_num_size = max(num_size_batch) + len(generate_num1_ids)
        for i in num_size_batch:
            d = i + len(generate_num1_ids)
            num_mask.append([0] * d + [1] * (max_num_size - d))
        num_mask = torch.ByteTensor(num_mask)

        num_pos_pad = []
        max_num_pos_size = max(num_size_batch)
        for i in range(len(num_pos_batch)):
            temp = num_pos_batch[i] + [-1] * (max_num_pos_size - len(num_pos_batch[i]))
            num_pos_pad.append(temp)
        num_pos_pad = torch.LongTensor(num_pos_pad)

        num_order_pad = []
        max_num_order_size = max(num_size_batch)
        for i in range(len(num_order_batch)):
            temp = num_order_batch[i] + [0] * (max_num_order_size - len(num_order_batch[i]))
            num_order_pad.append(temp)
        num_order_pad = torch.LongTensor(num_order_pad)

        num_stack1_batch = copy.deepcopy(num_stack_batch)
        num_stack2_batch = copy.deepcopy(num_stack_batch)

        # Turn padded arrays into (batch_size x max_len) tensors, transpose into (max_len x batch_size)
        # input1_var = torch.LongTensor(input1_batch).transpose(0, 1)
        # input2_var = torch.LongTensor(input2_batch).transpose(0, 1)
        # target1 = torch.LongTensor(target1_batch).transpose(0, 1)
        # target2 = torch.LongTensor(target2_batch).transpose(0, 1)
        # parse_graph_pad = torch.LongTensor(parse_graph_batch)
        input1_var = input1_batch.transpose(0, 1)
        input2_var = input2_batch.transpose(0, 1)
        target1 = target1_batch.transpose(0, 1)
        target2 = target2_batch.transpose(0, 1)
        parse_graph_pad = parse_graph_batch

        padding_hidden = torch.FloatTensor([0.0 for _ in range(self.hidden_size)]).unsqueeze(0)
        batch_size = len(input_length)

        if self.USE_CUDA:
            input1_var = input1_var.cuda()
            input2_var = input2_var.cuda()
            seq_mask = seq_mask.cuda()
            padding_hidden = padding_hidden.cuda()
            num_mask = num_mask.cuda()
            num_pos_pad = num_pos_pad.cuda()
            num_order_pad = num_order_pad.cuda()
            parse_graph_pad = parse_graph_pad.cuda()

        # Run words through encoder

        encoder_outputs, encoder_hidden = self.encoder(input1_var, input2_var, input_length, parse_graph_pad)
        copy_num_len = [len(_) for _ in num_pos_batch]
        num_size = max(copy_num_len)
        num_encoder_outputs, masked_index = self.get_all_number_encoder_outputs(encoder_outputs, num_pos_batch, batch_size, num_size, self.hidden_size)
        encoder_outputs, num_outputs, problem_output = self.numencoder(encoder_outputs, num_encoder_outputs, num_pos_pad, num_order_pad)
        num_outputs = num_outputs.masked_fill_(masked_index.bool(), 0.0)

        decoder_hidden = encoder_hidden[:self.n_layers]  # Use last (forward) hidden state from encoder

        loss_0 = self.train_tree_double(encoder_outputs, problem_output, num_outputs, target1, target1_length, num_start1, batch_size, padding_hidden, seq_mask, num_mask, num_pos_batch, num_order_pad,
                                        num_stack1_batch, unk1)

        loss_1 = self.train_attn_double(encoder_outputs, decoder_hidden, target2, target2_length, sos2, batch_size, seq_mask, num_start2, num_stack2_batch, unk2, beam_size, use_teacher_forcing)

        loss = loss_0 + loss_1
        loss.backward()

        return loss.item()  # , loss_0.item(), loss_1.item()

    def train_tree_double(self, encoder_outputs, problem_output, all_nums_encoder_outputs, target, target_length, num_start, batch_size, padding_hidden, seq_mask, num_mask, num_pos, num_order_pad,
                          nums_stack_batch, unk):
        # Prepare input and output variables
        node_stacks = [[TreeNode(_)] for _ in problem_output.split(1, dim=0)]

        max_target_length = max(target_length)

        all_node_outputs = []
        # all_leafs = []

        embeddings_stacks = [[] for _ in range(batch_size)]
        left_childs = [None for _ in range(batch_size)]
        for t in range(max_target_length):
            num_score, op, current_embeddings, current_context, current_nums_embeddings = self.predict(node_stacks, left_childs, encoder_outputs, all_nums_encoder_outputs, padding_hidden, seq_mask,
                                                                                                       num_mask)

            # all_leafs.append(p_leaf)
            outputs = torch.cat((op, num_score), 1)
            all_node_outputs.append(outputs)

            target_t, generate_input = self.generate_tree_input(target[t].tolist(), outputs, nums_stack_batch, num_start, unk)
            target[t] = target_t
            if self.USE_CUDA:
                generate_input = generate_input.cuda()
            left_child, right_child, node_label = self.generate(current_embeddings, generate_input, current_context)
            left_childs = []
            for idx, l, r, node_stack, i, o in zip(range(batch_size), left_child.split(1), right_child.split(1), node_stacks, target[t].tolist(), embeddings_stacks):
                if len(node_stack) != 0:
                    node = node_stack.pop()
                else:
                    left_childs.append(None)
                    continue

                if i < num_start:
                    node_stack.append(TreeNode(r))
                    node_stack.append(TreeNode(l, left_flag=True))
                    o.append(TreeEmbedding(node_label[idx].unsqueeze(0), False))
                else:
                    current_num = current_nums_embeddings[idx, i - num_start].unsqueeze(0)
                    while len(o) > 0 and o[-1].terminal:
                        sub_stree = o.pop()
                        op = o.pop()
                        current_num = self.merge(op.embedding, sub_stree.embedding, current_num)
                    o.append(TreeEmbedding(current_num, True))
                if len(o) > 0 and o[-1].terminal:
                    left_childs.append(o[-1].embedding)
                else:
                    left_childs.append(None)

        # all_leafs = torch.stack(all_leafs, dim=1)  # B x S x 2
        all_node_outputs = torch.stack(all_node_outputs, dim=1)  # B x S x N

        target = target.transpose(0, 1).contiguous()
        if self.USE_CUDA:
            # all_leafs = all_leafs.cuda()
            all_node_outputs = all_node_outputs.cuda()
            target = target.cuda()
            target_length = torch.LongTensor(target_length).cuda()
        else:
            target_length = torch.LongTensor(target_length)
        # op_target = target < num_start
        # loss_0 = masked_cross_entropy_without_logit(all_leafs, op_target.long(), target_length)
        loss = masked_cross_entropy(all_node_outputs, target, target_length)
        # loss = loss_0 + loss_1
        return loss  # , loss_0.item(), loss_1.item()

    def train_attn_double(self, encoder_outputs, decoder_hidden, target, target_length, sos, batch_size, seq_mask, num_start, nums_stack_batch, unk, beam_size, use_teacher_forcing):
        # Prepare input and output variables
        decoder_input = torch.LongTensor([sos] * batch_size)

        max_target_length = max(target_length)
        all_decoder_outputs = torch.zeros(max_target_length, batch_size, self.decoder.output_size)

        # Move new Variables to CUDA
        if self.USE_CUDA:
            all_decoder_outputs = all_decoder_outputs.cuda()

        if random.random() < use_teacher_forcing:
            # Run through decoder one time step at a time
            for t in range(max_target_length):
                if self.USE_CUDA:
                    decoder_input = decoder_input.cuda()

                decoder_output, decoder_hidden = self.decoder(decoder_input, decoder_hidden, encoder_outputs, seq_mask)
                all_decoder_outputs[t] = decoder_output
                decoder_input = self.generate_decoder_input(target[t].cpu().tolist(), decoder_output, nums_stack_batch, num_start, unk)
                target[t] = decoder_input
        else:
            beam_list = list()
            score = torch.zeros(batch_size)
            if self.USE_CUDA:
                score = score.cuda()
            beam_list.append(Beam(score, decoder_input, decoder_hidden, all_decoder_outputs))
            # Run through decoder one time step at a time
            for t in range(max_target_length):
                beam_len = len(beam_list)
                beam_scores = torch.zeros(batch_size, self.decoder.output_size * beam_len)
                all_hidden = torch.zeros(decoder_hidden.size(0), batch_size * beam_len, decoder_hidden.size(2))
                all_outputs = torch.zeros(max_target_length, batch_size * beam_len, self.decoder.output_size)
                if self.USE_CUDA:
                    beam_scores = beam_scores.cuda()
                    all_hidden = all_hidden.cuda()
                    all_outputs = all_outputs.cuda()

                for b_idx in range(len(beam_list)):
                    decoder_input = beam_list[b_idx].input_var
                    decoder_hidden = beam_list[b_idx].hidden

                    #                rule_mask = generate_rule_mask(decoder_input, num_batch, output_lang.word2index, batch_size,
                    #                                               num_start, copy_nums, generate_nums, english)
                    if self.USE_CUDA:
                        #                    rule_mask = rule_mask.cuda()
                        decoder_input = decoder_input.cuda()

                    decoder_output, decoder_hidden = self.decoder(decoder_input, decoder_hidden, encoder_outputs, seq_mask)

                    #                score = f.log_softmax(decoder_output, dim=1) + rule_mask
                    score = F.log_softmax(decoder_output, dim=1)
                    beam_score = beam_list[b_idx].score
                    beam_score = beam_score.unsqueeze(1)
                    repeat_dims = [1] * beam_score.dim()
                    repeat_dims[1] = score.size(1)
                    beam_score = beam_score.repeat(*repeat_dims)
                    score += beam_score
                    beam_scores[:, b_idx * self.decoder.output_size:(b_idx + 1) * self.decoder.output_size] = score
                    all_hidden[:, b_idx * batch_size:(b_idx + 1) * batch_size, :] = decoder_hidden

                    beam_list[b_idx].all_output[t] = decoder_output
                    all_outputs[:, batch_size * b_idx: batch_size * (b_idx + 1), :] = \
                        beam_list[b_idx].all_output
                topv, topi = beam_scores.topk(beam_size, dim=1)
                beam_list = list()

                for k in range(beam_size):
                    temp_topk = topi[:, k]
                    temp_input = temp_topk % self.decoder.output_size
                    temp_input = temp_input.data
                    if self.USE_CUDA:
                        temp_input = temp_input.cpu()
                    temp_beam_pos = temp_topk / self.decoder.output_size

                    indices = torch.LongTensor(range(batch_size))
                    if self.USE_CUDA:
                        indices = indices.cuda()
                    indices += temp_beam_pos * batch_size

                    temp_hidden = all_hidden.index_select(1, indices)
                    temp_output = all_outputs.index_select(1, indices)

                    beam_list.append(Beam(topv[:, k], temp_input, temp_hidden, temp_output))
            all_decoder_outputs = beam_list[0].all_output

            for t in range(max_target_length):
                target[t] = self.generate_decoder_input(target[t].cpu().tolist(), all_decoder_outputs[t], nums_stack_batch, num_start, unk)
        # Loss calculation and backpropagation

        if self.USE_CUDA:
            target = target.cuda()
            target_length = torch.LongTensor(target_length).cuda()
        else:
            target_length = torch.LongTensor(target_length)

        loss = masked_cross_entropy(
            all_decoder_outputs.transpose(0, 1).contiguous(),  # -> batch x seq
            target.transpose(0, 1).contiguous(),  # -> batch x seq
            target_length)

        return loss

    def evaluate_double(self,
                        input1_batch,
                        input2_batch,
                        input_length,
                        generate_num1_ids,
                        num_start1,
                        sos2,
                        eos2,
                        num_pos_batch,
                        num_order_batch,
                        parse_graph_batch,
                        beam_size=5,
                        english=False,
                        max_length=30):
        seq_mask = torch.ByteTensor(1, input_length).fill_(0)
        # num_pos_pad = torch.LongTensor([num_pos_batch])
        # num_order_pad = torch.LongTensor([num_order_batch])
        # parse_graph_pad = torch.LongTensor(parse_graph_batch)
        # Turn padded arrays into (batch_size x max_len) tensors, transpose into (max_len x batch_size)
        # input1_var = torch.LongTensor(input1_batch).transpose()
        # input2_var = torch.LongTensor(input2_batch).unsqueeze(1)
        num_pos_pad = torch.LongTensor(num_pos_batch)
        num_order_pad = torch.LongTensor(num_order_batch)
        parse_graph_pad = parse_graph_batch
        input1_var = input1_batch.transpose(0, 1)
        input2_var = input2_batch.transpose(0, 1)

        num_mask = torch.ByteTensor(1, len(num_pos_batch[0]) + len(generate_num1_ids)).fill_(0)

        padding_hidden = torch.FloatTensor([0.0 for _ in range(self.hidden_size)]).unsqueeze(0)

        batch_size = 1

        if self.USE_CUDA:
            input1_var = input1_var.cuda()
            input2_var = input2_var.cuda()
            seq_mask = seq_mask.cuda()
            padding_hidden = padding_hidden.cuda()
            num_mask = num_mask.cuda()
            num_pos_pad = num_pos_pad.cuda()
            num_order_pad = num_order_pad.cuda()
            parse_graph_pad = parse_graph_pad.cuda()
        # Run words through encoder

        encoder_outputs, encoder_hidden = self.encoder(input1_var, input2_var, input_length, parse_graph_pad)
        copy_num_len = [len(_) for _ in num_pos_batch]
        num_size = max(copy_num_len)
        #num_size = len(num_pos_batch)
        num_encoder_outputs, masked_index = self.get_all_number_encoder_outputs(encoder_outputs, num_pos_batch, batch_size, num_size, self.hidden_size)
        encoder_outputs, num_outputs, problem_output = self.numencoder(encoder_outputs, num_encoder_outputs, num_pos_pad, num_order_pad)
        decoder_hidden = encoder_hidden[:self.n_layers]  # Use last (forward) hidden state from encoder

        tree_beam = self.evaluate_tree_double(encoder_outputs, problem_output, num_outputs, num_start1, batch_size, padding_hidden, seq_mask, num_mask, max_length, num_pos_batch, num_order_pad,
                                              beam_size)

        attn_beam = self.evaluate_attn_double(encoder_outputs, decoder_hidden, sos2, eos2, batch_size, seq_mask, max_length, beam_size)

        if tree_beam.score >= attn_beam.score:
            return "tree", tree_beam.out, tree_beam.score
        else:
            return "attn", attn_beam.all_output, attn_beam.score

    def evaluate_tree_double(self, encoder_outputs, problem_output, all_nums_encoder_outputs, num_start, batch_size, padding_hidden, seq_mask, num_mask, max_length, num_pos, num_order_pad, beam_size):
        # Prepare input and output variables
        node_stacks = [[TreeNode(_)] for _ in problem_output.split(1, dim=0)]

        # B x P x N
        embeddings_stacks = [[] for _ in range(batch_size)]
        left_childs = [None for _ in range(batch_size)]

        beams = [TreeBeam(0.0, node_stacks, embeddings_stacks, left_childs, [])]

        for t in range(max_length):
            current_beams = []
            while len(beams) > 0:
                b = beams.pop()
                if len(b.node_stack[0]) == 0:
                    current_beams.append(b)
                    continue
                # left_childs = torch.stack(b.left_childs)
                left_childs = b.left_childs

                num_score, op, current_embeddings, current_context, current_nums_embeddings = self.predict(b.node_stack, left_childs, encoder_outputs, all_nums_encoder_outputs, padding_hidden,
                                                                                                           seq_mask, num_mask)

                out_score = nn.functional.log_softmax(torch.cat((op, num_score), dim=1), dim=1)

                topv, topi = out_score.topk(beam_size)

                for tv, ti in zip(topv.split(1, dim=1), topi.split(1, dim=1)):
                    current_node_stack = copy_list(b.node_stack)
                    current_left_childs = []
                    current_embeddings_stacks = copy_list(b.embedding_stack)
                    current_out = copy.deepcopy(b.out)

                    out_token = int(ti)
                    current_out.append(out_token)

                    node = current_node_stack[0].pop()

                    if out_token < num_start:
                        generate_input = torch.LongTensor([out_token])
                        if self.USE_CUDA:
                            generate_input = generate_input.cuda()
                        left_child, right_child, node_label = self.generate(current_embeddings, generate_input, current_context)

                        current_node_stack[0].append(TreeNode(right_child))
                        current_node_stack[0].append(TreeNode(left_child, left_flag=True))

                        current_embeddings_stacks[0].append(TreeEmbedding(node_label[0].unsqueeze(0), False))
                    else:
                        current_num = current_nums_embeddings[0, out_token - num_start].unsqueeze(0)

                        while len(current_embeddings_stacks[0]) > 0 and current_embeddings_stacks[0][-1].terminal:
                            sub_stree = current_embeddings_stacks[0].pop()
                            op = current_embeddings_stacks[0].pop()
                            current_num = self.merge(op.embedding, sub_stree.embedding, current_num)
                        current_embeddings_stacks[0].append(TreeEmbedding(current_num, True))
                    if len(current_embeddings_stacks[0]) > 0 and current_embeddings_stacks[0][-1].terminal:
                        current_left_childs.append(current_embeddings_stacks[0][-1].embedding)
                    else:
                        current_left_childs.append(None)
                    current_beams.append(TreeBeam(b.score + float(tv), current_node_stack, current_embeddings_stacks, current_left_childs, current_out))
            beams = sorted(current_beams, key=lambda x: x.score, reverse=True)
            beams = beams[:beam_size]
            flag = True
            for b in beams:
                if len(b.node_stack[0]) != 0:
                    flag = False
            if flag:
                break

        return beams[0]

    def evaluate_attn_double(self, encoder_outputs, decoder_hidden, sos, eos, batch_size, seq_mask, max_length, beam_size):
        # Create starting vectors for decoder
        decoder_input = torch.LongTensor([sos])  # SOS
        beam_list = list()
        score = 0
        beam_list.append(Beam(score, decoder_input, decoder_hidden, []))

        # Run through decoder
        for di in range(max_length):
            temp_list = list()
            beam_len = len(beam_list)
            for xb in beam_list:
                if int(xb.input_var[0]) == eos:
                    temp_list.append(xb)
                    beam_len -= 1
            if beam_len == 0:
                return beam_list[0]
            beam_scores = torch.zeros(self.decoder.output_size * beam_len)
            hidden_size_0 = decoder_hidden.size(0)
            hidden_size_2 = decoder_hidden.size(2)
            all_hidden = torch.zeros(beam_len, hidden_size_0, 1, hidden_size_2)
            if self.USE_CUDA:
                beam_scores = beam_scores.cuda()
                all_hidden = all_hidden.cuda()
            all_outputs = []
            current_idx = -1

            for b_idx in range(len(beam_list)):
                decoder_input = beam_list[b_idx].input_var
                if int(decoder_input[0]) == eos:
                    continue
                current_idx += 1
                decoder_hidden = beam_list[b_idx].hidden

                # rule_mask = generate_rule_mask(decoder_input, [num_list], output_lang.word2index,
                #                                1, num_start, copy_nums, generate_nums, english)
                if self.USE_CUDA:
                    # rule_mask = rule_mask.cuda()
                    decoder_input = decoder_input.cuda()

                decoder_output, decoder_hidden = self.decoder(decoder_input, decoder_hidden, encoder_outputs, seq_mask)
                # score = f.log_softmax(decoder_output, dim=1) + rule_mask.squeeze()
                score = F.log_softmax(decoder_output, dim=1)
                score += beam_list[b_idx].score
                beam_scores[current_idx * self.decoder.output_size:(current_idx + 1) * self.decoder.output_size] = score
                all_hidden[current_idx] = decoder_hidden
                all_outputs.append(beam_list[b_idx].all_output)
            topv, topi = beam_scores.topk(beam_size)

            for k in range(beam_size):
                word_n = int(topi[k])
                word_input = word_n % self.decoder.output_size
                temp_input = torch.LongTensor([word_input])
                indices = int(word_n / self.decoder.output_size)

                temp_hidden = all_hidden[indices]
                temp_output = all_outputs[indices] + [word_input]
                temp_list.append(Beam(float(topv[k]), temp_input, temp_hidden, temp_output))

            temp_list = sorted(temp_list, key=lambda x: x.score, reverse=True)

            if len(temp_list) < beam_size:
                beam_list = temp_list
            else:
                beam_list = temp_list[:beam_size]
        return beam_list[0]

    def generate_tree_input(self, target, decoder_output, nums_stack_batch, num_start, unk):
        # when the decoder input is copied num but the num has two pos, chose the max
        target_input = copy.deepcopy(target)
        for i in range(len(target)):
            if target[i] == unk:
                num_stack = nums_stack_batch[i].pop()
                max_score = -float("1e12")
                for num in num_stack:
                    if decoder_output[i, num_start + num] > max_score:
                        target[i] = num + num_start
                        max_score = decoder_output[i, num_start + num]
            if target_input[i] >= num_start:
                target_input[i] = 0
        return torch.LongTensor(target), torch.LongTensor(target_input)

    def get_all_number_encoder_outputs(self, encoder_outputs, num_pos, batch_size, num_size, hidden_size):
        indices = list()
        sen_len = encoder_outputs.size(0)
        masked_index = []
        temp_1 = [1 for _ in range(hidden_size)]
        temp_0 = [0 for _ in range(hidden_size)]
        for b in range(batch_size):
            for i in num_pos[b]:
                indices.append(i + b * sen_len)
                masked_index.append(temp_0)
            indices += [0 for _ in range(len(num_pos[b]), num_size)]
            masked_index += [temp_1 for _ in range(len(num_pos[b]), num_size)]
        indices = torch.LongTensor(indices)
        masked_index = torch.ByteTensor(masked_index)
        masked_index = masked_index.view(batch_size, num_size, hidden_size)
        if self.USE_CUDA:
            indices = indices.cuda()
            masked_index = masked_index.cuda()
        all_outputs = encoder_outputs.transpose(0, 1).contiguous()
        all_embedding = all_outputs.view(-1, encoder_outputs.size(2))  # S x B x H -> (B x S) x H
        all_num = all_embedding.index_select(0, indices)
        all_num = all_num.view(batch_size, num_size, hidden_size)
        return all_num.masked_fill_(masked_index.bool(), 0.0), masked_index

    def generate_decoder_input(self, target, decoder_output, nums_stack_batch, num_start, unk):
        # when the decoder input is copied num but the num has two pos, chose the max
        if self.USE_CUDA:
            decoder_output = decoder_output.cpu()
        target = torch.LongTensor(target)
        for i in range(target.size(0)):
            if target[i] == unk:
                num_stack = nums_stack_batch[i].pop()
                max_score = -float("1e12")
                for num in num_stack:
                    if decoder_output[i, num_start + num] > max_score:
                        target[i] = num + num_start
                        max_score = decoder_output[i, num_start + num]
        return target

    def convert_idx2symbol1(self, output, num_list, num_stack):
        #batch_size=output.size(0)
        '''batch_size=1'''
        seq_len = len(output)
        num_len = len(num_list)
        output_list = []
        res = []
        for s_i in range(seq_len):
            idx = output[s_i]
            if idx in [self.out_sos_token1, self.out_eos_token1, self.out_pad_token1]:
                break
            symbol = self.out_idx2symbol1[idx]
            if "NUM" in symbol:
                num_idx = self.mask_list.index(symbol)
                if num_idx >= num_len:
                    res = []
                    break
                res.append(num_list[num_idx])
            elif symbol == SpecialTokens.UNK_TOKEN:
                try:
                    pos_list = num_stack.pop()
                    c = num_list[pos_list[0]]
                    res.append(c)
                except:
                    return None
            else:
                res.append(symbol)
        output_list.append(res)
        return output_list

    def convert_idx2symbol2(self, output, num_list, num_stack):
        batch_size = output.size(0)
        seq_len = output.size(1)
        output_list = []
        for b_i in range(batch_size):
            res = []
            num_len = len(num_list[b_i])
            for s_i in range(seq_len):
                idx = output[b_i][s_i]
                if idx in [self.out_sos_token2, self.out_eos_token2, self.out_pad_token2]:
                    break
                symbol = self.out_idx2symbol2[idx]
                if "NUM" in symbol:
                    num_idx = self.mask_list.index(symbol)
                    if num_idx >= num_len:
                        res.append(symbol)
                    else:
                        res.append(num_list[b_i][num_idx])
                elif symbol == SpecialTokens.UNK_TOKEN:
                    try:
                        pos_list = num_stack[b_i].pop()
                        c = num_list[b_i][pos_list[0]]
                        res.append(c)
                    except:
                        res.append(symbol)
                else:
                    res.append(symbol)
            output_list.append(res)
        return output_list


class _MultiEncDec_(nn.Module):
    def __init__(self, config, dataset):
        super(_MultiEncDec_, self).__init__()
        self.device = config['device']
        self.rnn_cell_type = config['rnn_cell_type']
        self.embedding_size = config['embedding_size']
        self.hidden_size = config['hidden_size']
        self.n_layers = config['num_layers']
        self.hop_size = config['hop_size']
        self.teacher_force_ratio = config['teacher_force_ratio']
        self.beam_size = config['beam_size']
        self.max_out_len = config['max_output_len']
        self.dropout_ratio = config['dropout_ratio']

        self.operator_nums = dataset.operator_nums
        self.generate_nums = len(dataset.generate_list)
        self.num_start1 = dataset.num_start1
        self.num_start2 = dataset.num_start2
        self.input1_size = len(dataset.in_idx2word_1)
        self.input2_size = len(dataset.in_idx2word_2)
        self.output2_size = len(dataset.out_idx2symbol_2)
        self.unk1 = dataset.out_symbol2idx_1[SpecialTokens.UNK_TOKEN]
        self.unk2 = dataset.out_symbol2idx_2[SpecialTokens.UNK_TOKEN]
        self.sos2 = dataset.out_symbol2idx_2[SpecialTokens.SOS_TOKEN]
        self.eos2 = dataset.out_symbol2idx_2[SpecialTokens.EOS_TOKEN]

        self.out_symbol2idx1 = dataset.out_symbol2idx_1
        self.out_idx2symbol1 = dataset.out_idx2symbol_1
        self.out_symbol2idx2 = dataset.out_symbol2idx_2
        self.out_idx2symbol2 = dataset.out_idx2symbol_2
        generate_list = dataset.generate_list
        self.generate_list = [self.out_symbol2idx1[symbol] for symbol in generate_list]
        self.mask_list = NumMask.number

        try:
            self.out_sos_token1 = self.out_symbol2idx1[SpecialTokens.SOS_TOKEN]
        except:
            self.out_sos_token1 = None
        try:
            self.out_eos_token1 = self.out_symbol2idx1[SpecialTokens.EOS_TOKEN]
        except:
            self.out_eos_token1 = None
        try:
            self.out_pad_token1 = self.out_symbol2idx1[SpecialTokens.PAD_TOKEN]
        except:
            self.out_pad_token1 = None
        try:
            self.out_sos_token2 = self.out_symbol2idx2[SpecialTokens.SOS_TOKEN]
        except:
            self.out_sos_token2 = None
        try:
            self.out_eos_token2 = self.out_symbol2idx2[SpecialTokens.EOS_TOKEN]
        except:
            self.out_eos_token2 = None
        try:
            self.out_pad_token2 = self.out_symbol2idx2[SpecialTokens.PAD_TOKEN]
        except:
            self.out_pad_token2 = None
        # Initialize models
        embedder = BaiscEmbedder(self.input1_size, self.embedding_size, self.dropout_ratio)
        in_embedder = self._init_embedding_params(dataset.trainset, dataset.in_idx2word_1, config['embedding_size'], embedder)

        #self.out_embedder = BaiscEmbedder(self.output2_size,self.embedding_size,self.dropout_ratio)

        self.encoder = GraphBasedMultiEncoder(input1_size=self.input1_size,
                                              input2_size=self.input2_size,
                                              embed_model=in_embedder,
                                              embedding1_size=self.embedding_size,
                                              embedding2_size=self.embedding_size // 4,
                                              hidden_size=self.hidden_size,
                                              n_layers=self.n_layers,
                                              hop_size=self.hop_size)

        self.numencoder = NumEncoder(node_dim=self.hidden_size, hop_size=self.hop_size)

        self.predict = TreeDecoder(hidden_size=self.hidden_size, op_nums=self.operator_nums, generate_size=self.generate_nums)

        self.generate = NodeGenerater(hidden_size=self.hidden_size, op_nums=self.operator_nums, embedding_size=self.embedding_size)

        self.merge = SubTreeMerger(hidden_size=self.hidden_size, embedding_size=self.embedding_size)

        self.decoder = TreeAttnDecoderRNN(self.hidden_size, self.embedding_size, self.output2_size, self.output2_size, self.n_layers, self.dropout_ratio)

        # self.decoder = AttentionalRNNDecoder(embedding_size=self.embedding_size,
        #                                      hidden_size=self.hidden_size,
        #                                      context_size=self.hidden_size,
        #                                      num_dec_layers=self.n_layers,
        #                                      rnn_cell_type=self.rnn_cell_type,
        #                                      dropout_ratio=self.dropout_ratio)
        #self.out = nn.Linear(self.hidden_size, self.output2_size)

        self.loss = MaskedCrossEntropyLoss()

    def _init_embedding_params(self, train_data, vocab, embedding_size, embedder):
        sentences = []
        for data in train_data:
            sentence = []
            for word in data['question']:
                if word in vocab:
                    sentence.append(word)
                else:
                    sentence.append(SpecialTokens.UNK_TOKEN)
            sentences.append(sentence)
        from gensim.models import word2vec
        model = word2vec.Word2Vec(sentences, size=embedding_size, min_count=1)
        emb_vectors = []
        pad_idx = vocab.index(SpecialTokens.PAD_TOKEN)
        for idx in range(len(vocab)):
            if idx != pad_idx:
                emb_vectors.append(np.array(model.wv[vocab[idx]]))
            else:
                emb_vectors.append(np.zeros((embedding_size)))
        emb_vectors = np.array(emb_vectors)
        embedder.embedder.weight.data.copy_(torch.from_numpy(emb_vectors))

        return embedder


    def forward(self,input1_var, input2_var, input_length, target1, target1_length, target2, target2_length,\
                num_stack_batch, num_size_batch,generate_list,num_pos_batch, num_order_batch, parse_graph):
        # sequence mask for attention
        seq_mask = []
        max_len = max(input_length)
        for i in input_length:
            seq_mask.append([0 for _ in range(i)] + [1 for _ in range(i, max_len)])
        seq_mask = torch.ByteTensor(seq_mask)

        num_mask = []
        max_num_size = max(num_size_batch) + len(generate_list)
        for i in num_size_batch:
            d = i + len(generate_list)
            num_mask.append([0] * d + [1] * (max_num_size - d))
        num_mask = torch.ByteTensor(num_mask)

        num_pos_pad = []
        max_num_pos_size = max(num_size_batch)
        for i in range(len(num_pos_batch)):
            temp = num_pos_batch[i] + [-1] * (max_num_pos_size - len(num_pos_batch[i]))
            num_pos_pad.append(temp)
        num_pos_pad = torch.LongTensor(num_pos_pad)

        num_order_pad = []
        max_num_order_size = max(num_size_batch)
        for i in range(len(num_order_batch)):
            temp = num_order_batch[i] + [0] * (max_num_order_size - len(num_order_batch[i]))
            num_order_pad.append(temp)
        num_order_pad = torch.LongTensor(num_order_pad)

        num_stack1_batch = copy.deepcopy(num_stack_batch)
        num_stack2_batch = copy.deepcopy(num_stack_batch)
        #num_start2 = output2_lang.n_words - copy_nums - 2
        #unk1 = output1_lang.word2index["UNK"]
        #unk2 = output2_lang.word2index["UNK"]

        # Turn padded arrays into (batch_size x max_len) tensors, transpose into (max_len x batch_size)
        # input1_var = torch.LongTensor(input1_batch).transpose(0, 1)
        # input2_var = torch.LongTensor(input2_batch).transpose(0, 1)
        # target1 = torch.LongTensor(target1_batch).transpose(0, 1)
        # target2 = torch.LongTensor(target2_batch).transpose(0, 1)
        input1_var = input1_var.transpose(0, 1)
        input2_var = input2_var.transpose(0, 1)
        target1 = target1.transpose(0, 1)
        target2 = target2.transpose(0, 1)
        parse_graph_pad = torch.LongTensor(parse_graph)

        padding_hidden = torch.FloatTensor([0.0 for _ in range(self.hidden_size)]).unsqueeze(0)
        batch_size = len(input_length)

        encoder_outputs, encoder_hidden = self.encoder(input1_var, input2_var, input_length, parse_graph_pad)
        copy_num_len = [len(_) for _ in num_pos_batch]
        num_size = max(copy_num_len)
        num_encoder_outputs, masked_index = self.get_all_number_encoder_outputs(encoder_outputs, num_pos_batch, num_size, self.hidden_size)
        encoder_outputs, num_outputs, problem_output = self.numencoder(encoder_outputs, num_encoder_outputs, num_pos_pad, num_order_pad)
        num_outputs = num_outputs.masked_fill_(masked_index.bool(), 0.0)

        decoder_hidden = encoder_hidden[self.n_layers]  # Use last (forward) hidden state from encoder
        if target1 != None:
            all_output1 = self.train_tree_double(encoder_outputs, problem_output, num_outputs, target1, target1_length, batch_size, padding_hidden, seq_mask, num_mask, num_pos_batch, num_order_pad,
                                                 num_stack1_batch)

            all_output2 = self.train_attn_double(encoder_outputs, decoder_hidden, target2, target2_length, batch_size, seq_mask, num_stack2_batch)
            return "train", all_output1, all_output2
        else:
            all_output1 = self.evaluate_tree_double(encoder_outputs, problem_output, num_outputs, batch_size, padding_hidden, seq_mask, num_mask)
            all_output2 = self.evaluate_attn_double(encoder_outputs, decoder_hidden, batch_size, seq_mask)
            if all_output1.score >= all_output2.score:
                return "tree", all_output1.out, all_output1.score
            else:
                return "attn", all_output2.all_output, all_output2.score

    def calculate_loss(self, batch_data):
        input1_var = batch_data['input1']
        input2_var = batch_data['input2']
        input_length = batch_data['input1 len']
        target1 = batch_data['output1']
        target1_length = batch_data['output1 len']
        target2 = batch_data['output2']
        target2_length = batch_data['output2 len']
        num_stack_batch = batch_data['num stack']
        num_size_batch = batch_data['num size']
        generate_list = self.generate_list
        num_pos_batch = batch_data['num pos']
        num_order_batch = batch_data['num order']
        parse_graph = batch_data['parse graph']
        equ_mask1 = batch_data['equ mask1']
        equ_mask2 = batch_data['equ mask2']
        # sequence mask for attention
        seq_mask = []
        max_len = max(input_length)
        for i in input_length:
            seq_mask.append([0 for _ in range(i)] + [1 for _ in range(i, max_len)])
        seq_mask = torch.BoolTensor(seq_mask).to(self.device)

        num_mask = []
        max_num_size = max(num_size_batch) + len(generate_list)
        for i in num_size_batch:
            d = i + len(generate_list)
            num_mask.append([0] * d + [1] * (max_num_size - d))
        num_mask = torch.BoolTensor(num_mask).to(self.device)

        num_pos_pad = []
        max_num_pos_size = max(num_size_batch)
        for i in range(len(num_pos_batch)):
            temp = num_pos_batch[i] + [-1] * (max_num_pos_size - len(num_pos_batch[i]))
            num_pos_pad.append(temp)
        num_pos_pad = torch.LongTensor(num_pos_pad).to(self.device)

        num_order_pad = []
        max_num_order_size = max(num_size_batch)
        for i in range(len(num_order_batch)):
            temp = num_order_batch[i] + [0] * (max_num_order_size - len(num_order_batch[i]))
            num_order_pad.append(temp)
        num_order_pad = torch.LongTensor(num_order_pad).to(self.device)

        num_stack1_batch = copy.deepcopy(num_stack_batch)
        num_stack2_batch = copy.deepcopy(num_stack_batch)
        #num_start2 = output2_lang.n_words - copy_nums - 2
        #unk1 = output1_lang.word2index["UNK"]
        #unk2 = output2_lang.word2index["UNK"]

        # Turn padded arrays into (batch_size x max_len) tensors, transpose into (max_len x batch_size)
        # input1_var = torch.LongTensor(input1_batch).transpose(0, 1)
        # input2_var = torch.LongTensor(input2_batch).transpose(0, 1)
        # target1 = torch.LongTensor(target1_batch).transpose(0, 1)
        # target2 = torch.LongTensor(target2_batch).transpose(0, 1)
        # input1_var = input1_var.transpose(0, 1)
        # input2_var = input2_var.transpose(0, 1)
        # target1 = target1.transpose(0, 1)
        # target2 = target2.transpose(0, 1)
        parse_graph_pad = parse_graph.long()

        padding_hidden = torch.FloatTensor([0.0 for _ in range(self.hidden_size)]).unsqueeze(0).to(self.device)
        batch_size = len(input_length)

        encoder_outputs, encoder_hidden = self.encoder(input1_var, input2_var, input_length, parse_graph_pad)
        copy_num_len = [len(_) for _ in num_pos_batch]
        num_size = max(copy_num_len)
        num_encoder_outputs, masked_index = self.get_all_number_encoder_outputs(encoder_outputs, num_pos_batch, num_size, self.hidden_size)
        encoder_outputs, num_outputs, problem_output = self.numencoder(encoder_outputs, num_encoder_outputs, num_pos_pad, num_order_pad)
        num_outputs = num_outputs.masked_fill_(masked_index.bool(), 0.0)

        decoder_hidden = encoder_hidden[:self.n_layers]  # Use last (forward) hidden state from encoder
        all_output1, target1 = self.train_tree_double(encoder_outputs, problem_output, num_outputs, target1, target1_length, batch_size, padding_hidden, seq_mask, num_mask, num_pos_batch,
                                                      num_order_pad, num_stack1_batch)

        all_output2, target2_ = self.train_attn_double(encoder_outputs, decoder_hidden, target2, target2_length, batch_size, seq_mask, num_stack2_batch)
        self.loss.reset()
        self.loss.eval_batch(all_output1, target1, equ_mask1)
        self.loss.eval_batch(all_output2, target2_, equ_mask2)
        self.loss.backward()
        return self.loss.get_loss()

    def model_test(self, batch_data):
        input1_var = batch_data['input1']
        input2_var = batch_data['input2']
        input_length = batch_data['input1 len']
        target1 = batch_data['output1']
        target1_length = batch_data['output1 len']
        target2 = batch_data['output2']
        target2_length = batch_data['output2 len']
        num_stack_batch = batch_data['num stack']
        num_size_batch = batch_data['num size']
        generate_list = self.generate_list
        num_pos_batch = batch_data['num pos']
        num_order_batch = batch_data['num order']
        parse_graph = batch_data['parse graph']
        num_list = batch_data['num list']
        # sequence mask for attention
        seq_mask = []
        max_len = max(input_length)
        for i in input_length:
            seq_mask.append([0 for _ in range(i)] + [1 for _ in range(i, max_len)])
        seq_mask = torch.BoolTensor(seq_mask).to(self.device)

        num_mask = []
        max_num_size = max(num_size_batch) + len(generate_list)
        for i in num_size_batch:
            d = i + len(generate_list)
            num_mask.append([0] * d + [1] * (max_num_size - d))
        num_mask = torch.BoolTensor(num_mask).to(self.device)

        num_pos_pad = []
        max_num_pos_size = max(num_size_batch)
        for i in range(len(num_pos_batch)):
            temp = num_pos_batch[i] + [-1] * (max_num_pos_size - len(num_pos_batch[i]))
            num_pos_pad.append(temp)
        num_pos_pad = torch.LongTensor(num_pos_pad).to(self.device)

        num_order_pad = []
        max_num_order_size = max(num_size_batch)
        for i in range(len(num_order_batch)):
            temp = num_order_batch[i] + [0] * (max_num_order_size - len(num_order_batch[i]))
            num_order_pad.append(temp)
        num_order_pad = torch.LongTensor(num_order_pad).to(self.device)

        num_stack1_batch = copy.deepcopy(num_stack_batch)
        num_stack2_batch = copy.deepcopy(num_stack_batch)
        #num_start2 = output2_lang.n_words - copy_nums - 2
        #unk1 = output1_lang.word2index["UNK"]
        #unk2 = output2_lang.word2index["UNK"]

        # Turn padded arrays into (batch_size x max_len) tensors, transpose into (max_len x batch_size)
        # input1_var = torch.LongTensor(input1_batch).transpose(0, 1)
        # input2_var = torch.LongTensor(input2_batch).transpose(0, 1)
        # target1 = torch.LongTensor(target1_batch).transpose(0, 1)
        # target2 = torch.LongTensor(target2_batch).transpose(0, 1)
        # input1_var = input1_var.transpose(0, 1)
        # input2_var = input2_var.transpose(0, 1)
        # target1 = target1.transpose(0, 1)
        # target2 = target2.transpose(0, 1)
        parse_graph_pad = parse_graph.long()

        padding_hidden = torch.FloatTensor([0.0 for _ in range(self.hidden_size)]).unsqueeze(0).to(self.device)
        batch_size = len(input_length)

        encoder_outputs, encoder_hidden = self.encoder(input1_var, input2_var, input_length, parse_graph_pad)
        copy_num_len = [len(_) for _ in num_pos_batch]
        num_size = max(copy_num_len)
        num_encoder_outputs, masked_index = self.get_all_number_encoder_outputs(encoder_outputs, num_pos_batch, num_size, self.hidden_size)
        encoder_outputs, num_outputs, problem_output = self.numencoder(encoder_outputs, num_encoder_outputs, num_pos_pad, num_order_pad)
        num_outputs = num_outputs.masked_fill_(masked_index.bool(), 0.0)

        decoder_hidden = encoder_hidden[:self.n_layers]  # Use last (forward) hidden state from encoder
        all_output1 = self.evaluate_tree_double(encoder_outputs, problem_output, num_outputs, batch_size, padding_hidden, seq_mask, num_mask)
        all_output2 = self.evaluate_attn_double(encoder_outputs, decoder_hidden, batch_size, seq_mask)
        if all_output1.score >= all_output2.score:
            output1 = self.convert_idx2symbol1(all_output1.out, num_list[0], copy_list(num_stack1_batch[0]))
            targets1 = self.convert_idx2symbol1(target1[0], num_list[0], copy_list(num_stack1_batch[0]))
            return "tree", output1, targets1
        else:
            output2 = self.convert_idx2symbol2(torch.tensor(all_output2.all_output).view(1, -1), num_list, copy_list(num_stack2_batch))
            targets2 = self.convert_idx2symbol2(target2, num_list, copy_list(num_stack2_batch))
            return "attn", output2, targets2

    def train_tree_double(self, encoder_outputs, problem_output, all_nums_encoder_outputs, target, target_length, batch_size, padding_hidden, seq_mask, num_mask, num_pos, num_order_pad,
                          nums_stack_batch):
        # Prepare input and output variables
        node_stacks = [[TreeNode(_)] for _ in problem_output.split(1, dim=0)]

        max_target_length = max(target_length)

        all_node_outputs = []

        embeddings_stacks = [[] for _ in range(batch_size)]
        left_childs = [None for _ in range(batch_size)]
        for t in range(max_target_length):
            num_score, op, current_embeddings, current_context, current_nums_embeddings = self.predict(node_stacks, left_childs, encoder_outputs, all_nums_encoder_outputs, padding_hidden, seq_mask,
                                                                                                       num_mask)

            # all_leafs.append(p_leaf)
            outputs = torch.cat((op, num_score), 1)
            all_node_outputs.append(outputs)

            target_t, generate_input = self.generate_tree_input(target[:, t].tolist(), outputs, nums_stack_batch)
            target[:, t] = target_t
            # if USE_CUDA:
            #     generate_input = generate_input.cuda()
            generate_input = generate_input.to(self.device)
            left_child, right_child, node_label = self.generate(current_embeddings, generate_input, current_context)
            left_childs = []
            for idx, l, r, node_stack, i, o in zip(range(batch_size), left_child.split(1), right_child.split(1), node_stacks, target[:, t].tolist(), embeddings_stacks):
                if len(node_stack) != 0:
                    node = node_stack.pop()
                else:
                    left_childs.append(None)
                    continue

                if i < self.num_start1:
                    node_stack.append(TreeNode(r))
                    node_stack.append(TreeNode(l, left_flag=True))
                    o.append(TreeEmbedding(node_label[idx].unsqueeze(0), False))
                else:
                    current_num = current_nums_embeddings[idx, i - self.num_start1].unsqueeze(0)
                    while len(o) > 0 and o[-1].terminal:
                        sub_stree = o.pop()
                        op = o.pop()
                        current_num = self.merge(op.embedding, sub_stree.embedding, current_num)
                    o.append(TreeEmbedding(current_num, True))
                if len(o) > 0 and o[-1].terminal:
                    left_childs.append(o[-1].embedding)
                else:
                    left_childs.append(None)

        # all_leafs = torch.stack(all_leafs, dim=1)  # B x S x 2
        all_node_outputs = torch.stack(all_node_outputs, dim=1)  # B x S x N

        return all_node_outputs, target

    def train_attn_double(self, encoder_outputs, decoder_hidden, target, target_length, batch_size, seq_mask, nums_stack_batch):
        max_target_length = max(target_length)
        decoder_input = torch.LongTensor([self.sos2] * batch_size).to(self.device)
        all_decoder_outputs = torch.zeros(batch_size, max_target_length, self.output2_size).to(self.device)
        #all_decoder_outputs = []

        seq_mask = torch.unsqueeze(seq_mask, dim=1)

        # Move new Variables to CUDA
        # if USE_CUDA:
        #     all_decoder_outputs = all_decoder_outputs.cuda()
        if random.random() < self.teacher_force_ratio:
            # if random.random() < 0:
            # Run through decoder one time step at a time
            #decoder_inputs = torch.cat([decoder_input.view(batch_size,1),target],dim=1)[:,:-1]
            all_decoder_outputs = []
            for t in range(max_target_length):
                #decoder_inputs[:,t]=decoder_input
                #decoder_input = decoder_inputs[:,t]
                decoder_output, decoder_hidden = self.decoder(decoder_input, decoder_hidden, encoder_outputs, seq_mask.squeeze(1))
                #all_decoder_outputs[:,t,:] = decoder_output
                all_decoder_outputs.append(decoder_output)
                decoder_input = self.generate_decoder_input(target[:, t].tolist(), decoder_output, nums_stack_batch)
                target[:, t] = decoder_input
            all_decoder_outputs = torch.stack(all_decoder_outputs, dim=1)
        else:
            decoder_input = torch.LongTensor([self.sos2] * batch_size).to(self.device)
            beam_list = list()
            score = torch.zeros(batch_size).to(self.device)
            # if USE_CUDA:
            #     score = score.cuda()
            beam_list.append(Beam(score, decoder_input, decoder_hidden, all_decoder_outputs))
            # Run through decoder one time step at a time
            for t in range(max_target_length):
                beam_len = len(beam_list)
                beam_scores = torch.zeros(batch_size, self.output2_size * beam_len).to(self.device)
                all_hidden = torch.zeros(decoder_hidden.size(0), batch_size * beam_len, decoder_hidden.size(2)).to(self.device)
                all_outputs = torch.zeros(batch_size * beam_len, max_target_length, self.output2_size).to(self.device)

                # if USE_CUDA:
                #     beam_scores = beam_scores.cuda()
                #     all_hidden = all_hidden.cuda()
                #     all_outputs = all_outputs.cuda()

                for b_idx in range(len(beam_list)):
                    decoder_input = beam_list[b_idx].input_var
                    decoder_hidden = beam_list[b_idx].hidden

                    decoder_input = decoder_input.to(self.device)
                    decoder_output, decoder_hidden = self.decoder(decoder_input, decoder_hidden, encoder_outputs, seq_mask.squeeze(1))

                    score = F.log_softmax(decoder_output, dim=1)
                    beam_score = beam_list[b_idx].score
                    beam_score = beam_score.unsqueeze(1)
                    repeat_dims = [1] * beam_score.dim()
                    repeat_dims[1] = score.size(1)
                    beam_score = beam_score.repeat(*repeat_dims)
                    score = score + beam_score
                    beam_scores[:, b_idx * self.output2_size:(b_idx + 1) * self.output2_size] = score
                    all_hidden[:, b_idx * batch_size:(b_idx + 1) * batch_size, :] = decoder_hidden

                    beam_list[b_idx].all_output[:, t, :] = decoder_output

                    all_outputs[batch_size * b_idx: batch_size * (b_idx + 1),:, :] = \
                        beam_list[b_idx].all_output

                topv, topi = beam_scores.topk(self.beam_size, dim=1)
                beam_list = list()

                for k in range(self.beam_size):
                    temp_topk = topi[:, k]
                    temp_input = temp_topk % self.output2_size
                    temp_input = temp_input.data
                    temp_beam_pos = temp_topk // self.output2_size

                    indices = torch.LongTensor(range(batch_size)).to(self.device)
                    indices += temp_beam_pos * batch_size

                    temp_hidden = all_hidden.index_select(dim=1, index=indices)
                    temp_output = all_outputs.index_select(dim=0, index=indices)

                    beam_list.append(Beam(topv[:, k], temp_input, temp_hidden, temp_output))

            all_decoder_outputs = beam_list[0].all_output
            for t in range(max_target_length):
                target[:, t] = self.generate_decoder_input(target[:, t].tolist(), all_decoder_outputs[:, t], nums_stack_batch)
        return all_decoder_outputs, target

    def evaluate_tree_double(self, encoder_outputs, problem_output, all_nums_encoder_outputs, batch_size, padding_hidden, seq_mask, num_mask):
        # Prepare input and output variables
        node_stacks = [[TreeNode(_)] for _ in problem_output.split(1, dim=0)]

        #num_start = output_lang.num_start
        # B x P x N
        embeddings_stacks = [[] for _ in range(batch_size)]
        left_childs = [None for _ in range(batch_size)]

        beams = [TreeBeam(0.0, node_stacks, embeddings_stacks, left_childs, [])]

        for t in range(self.max_out_len):
            current_beams = []
            while len(beams) > 0:
                b = beams.pop()
                if len(b.node_stack[0]) == 0:
                    current_beams.append(b)
                    continue
                # left_childs = torch.stack(b.left_childs)
                left_childs = b.left_childs

                num_score, op, current_embeddings, current_context, current_nums_embeddings = self.predict(b.node_stack, left_childs, encoder_outputs, all_nums_encoder_outputs, padding_hidden,
                                                                                                           seq_mask, num_mask)

                out_score = nn.functional.log_softmax(torch.cat((op, num_score), dim=1), dim=1)

                topv, topi = out_score.topk(self.beam_size)

                for tv, ti in zip(topv.split(1, dim=1), topi.split(1, dim=1)):
                    current_node_stack = copy_list(b.node_stack)
                    current_left_childs = []
                    current_embeddings_stacks = copy_list(b.embedding_stack)
                    current_out = copy.deepcopy(b.out)

                    out_token = int(ti)
                    current_out.append(out_token)

                    node = current_node_stack[0].pop()

                    if out_token < self.num_start1:
                        generate_input = torch.LongTensor([out_token]).to(self.device)
                        # if USE_CUDA:
                        #     generate_input = generate_input.cuda()
                        left_child, right_child, node_label = self.generate(current_embeddings, generate_input, current_context)

                        current_node_stack[0].append(TreeNode(right_child))
                        current_node_stack[0].append(TreeNode(left_child, left_flag=True))

                        current_embeddings_stacks[0].append(TreeEmbedding(node_label[0].unsqueeze(0), False))
                    else:
                        current_num = current_nums_embeddings[0, out_token - self.num_start1].unsqueeze(0)

                        while len(current_embeddings_stacks[0]) > 0 and current_embeddings_stacks[0][-1].terminal:
                            sub_stree = current_embeddings_stacks[0].pop()
                            op = current_embeddings_stacks[0].pop()
                            current_num = self.merge(op.embedding, sub_stree.embedding, current_num)
                        current_embeddings_stacks[0].append(TreeEmbedding(current_num, True))
                    if len(current_embeddings_stacks[0]) > 0 and current_embeddings_stacks[0][-1].terminal:
                        current_left_childs.append(current_embeddings_stacks[0][-1].embedding)
                    else:
                        current_left_childs.append(None)
                    current_beams.append(TreeBeam(b.score + float(tv), current_node_stack, current_embeddings_stacks, current_left_childs, current_out))
            beams = sorted(current_beams, key=lambda x: x.score, reverse=True)
            beams = beams[:self.beam_size]
            flag = True
            for b in beams:
                if len(b.node_stack[0]) != 0:
                    flag = False
            if flag:
                break

        return beams[0]

    def evaluate_attn_double(self, encoder_outputs, decoder_hidden, batch_size, seq_mask):
        # Create starting vectors for decoder
        decoder_input = torch.LongTensor([self.sos2]).to(self.device)  # SOS
        beam_list = list()
        score = 0
        beam_list.append(Beam(score, decoder_input, decoder_hidden, []))

        # Run through decoder
        for di in range(self.max_out_len):
            temp_list = list()
            beam_len = len(beam_list)
            for xb in beam_list:
                if int(xb.input_var[0]) == self.eos2:
                    temp_list.append(xb)
                    beam_len -= 1
            if beam_len == 0:
                return beam_list[0]
            beam_scores = torch.zeros(self.output2_size * beam_len).to(self.device)
            hidden_size_0 = decoder_hidden.size(0)
            hidden_size_2 = decoder_hidden.size(2)
            all_hidden = torch.zeros(beam_len, hidden_size_0, 1, hidden_size_2).to(self.device)

            all_outputs = []
            current_idx = -1

            for b_idx in range(len(beam_list)):
                decoder_input = beam_list[b_idx].input_var
                if int(decoder_input[0]) == self.eos2:
                    continue
                current_idx += 1
                decoder_hidden = beam_list[b_idx].hidden

                decoder_output, decoder_hidden = self.decoder(decoder_input, decoder_hidden, encoder_outputs, seq_mask)
                #decoder_output = self.out(decoder_output).squeeze(dim=1)
                score = F.log_softmax(decoder_output, dim=1)
                score += beam_list[b_idx].score
                beam_scores[current_idx * self.output2_size:(current_idx + 1) * self.output2_size] = score
                all_hidden[current_idx] = decoder_hidden
                all_outputs.append(beam_list[b_idx].all_output)
            topv, topi = beam_scores.topk(self.beam_size)

            for k in range(self.beam_size):
                word_n = int(topi[k])
                word_input = word_n % self.output2_size
                temp_input = torch.LongTensor([word_input]).to(self.device)
                indices = int(word_n / self.output2_size)

                temp_hidden = all_hidden[indices]
                temp_output = all_outputs[indices] + [word_input]
                temp_list.append(Beam(float(topv[k]), temp_input, temp_hidden, temp_output))

            temp_list = sorted(temp_list, key=lambda x: x.score, reverse=True)

            if len(temp_list) < self.beam_size:
                beam_list = temp_list
            else:
                beam_list = temp_list[:self.beam_size]
        return beam_list[0]

    def get_all_number_encoder_outputs(self, encoder_outputs, num_pos, num_size, hidden_size):
        indices = list()
        sen_len = encoder_outputs.size(1)
        batch_size = encoder_outputs.size(0)
        masked_index = []
        temp_1 = [1 for _ in range(hidden_size)]
        temp_0 = [0 for _ in range(hidden_size)]
        for b in range(batch_size):
            for i in num_pos[b]:
                if i == -1:
                    indices.append(0)
                    masked_index.append(temp_1)
                    continue
                indices.append(i + b * sen_len)
                masked_index.append(temp_0)
            indices = indices + [0 for _ in range(len(num_pos[b]), num_size)]
            masked_index = masked_index + [temp_1 for _ in range(len(num_pos[b]), num_size)]
        # indices = torch.LongTensor(indices)
        # masked_index = torch.ByteTensor(masked_index)
        indices = torch.LongTensor(indices).to(self.device)
        masked_index = torch.BoolTensor(masked_index).to(self.device)
        masked_index = masked_index.view(batch_size, num_size, hidden_size)
        all_outputs = encoder_outputs.transpose(0, 1).contiguous()
        all_embedding = all_outputs.view(-1, encoder_outputs.size(2))  # S x B x H -> (B x S) x H
        all_num = all_embedding.index_select(0, indices)
        all_num = all_num.view(batch_size, num_size, hidden_size)
        return all_num.masked_fill_(masked_index.bool(), 0.0), masked_index

    def generate_tree_input(self, target, decoder_output, nums_stack_batch):
        # when the decoder input is copied num but the num has two pos, chose the max
        target_input = copy.deepcopy(target)
        for i in range(len(target)):
            if target[i] == self.unk1:
                num_stack = nums_stack_batch[i].pop()
                max_score = -float("1e12")
                for num in num_stack:
                    if decoder_output[i, self.num_start1 + num] > max_score:
                        target[i] = num + self.num_start1
                        max_score = decoder_output[i, self.num_start1 + num]
            if target_input[i] >= self.num_start1:
                target_input[i] = 0
        return torch.LongTensor(target), torch.LongTensor(target_input)

    def generate_decoder_input(self, target, decoder_output, nums_stack_batch):
        # when the decoder input is copied num but the num has two pos, chose the max
        # if USE_CUDA:
        #     decoder_output = decoder_output.cpu()
        target = torch.LongTensor(target).to(self.device)
        for i in range(target.size(0)):
            if target[i] == self.unk2:
                num_stack = nums_stack_batch[i].pop()
                max_score = -float("1e12")
                for num in num_stack:
                    if decoder_output[i, self.num_start2 + num] > max_score:
                        target[i] = num + self.num_start2
                        max_score = decoder_output[i, self.num_start2 + num]
        return target

    def convert_idx2symbol1(self, output, num_list, num_stack):
        #batch_size=output.size(0)
        '''batch_size=1'''
        seq_len = len(output)
        num_len = len(num_list)
        output_list = []
        res = []
        for s_i in range(seq_len):
            idx = output[s_i]
            if idx in [self.out_sos_token1, self.out_eos_token1, self.out_pad_token1]:
                break
            symbol = self.out_idx2symbol1[idx]
            if "NUM" in symbol:
                num_idx = self.mask_list.index(symbol)
                if num_idx >= num_len:
                    res = []
                    break
                res.append(num_list[num_idx])
            elif symbol == SpecialTokens.UNK_TOKEN:
                try:
                    pos_list = num_stack.pop()
                    c = num_list[pos_list[0]]
                    res.append(c)
                except:
                    return None
            else:
                res.append(symbol)
        output_list.append(res)
        return output_list

    def convert_idx2symbol2(self, output, num_list, num_stack):
        batch_size = output.size(0)
        seq_len = output.size(1)
        output_list = []
        for b_i in range(batch_size):
            res = []
            num_len = len(num_list[b_i])
            for s_i in range(seq_len):
                idx = output[b_i][s_i]
                if idx in [self.out_sos_token2, self.out_eos_token2, self.out_pad_token2]:
                    break
                symbol = self.out_idx2symbol2[idx]
                if "NUM" in symbol:
                    num_idx = self.mask_list.index(symbol)
                    if num_idx >= num_len:
                        res.append(symbol)
                    else:
                        res.append(num_list[b_i][num_idx])
                elif symbol == SpecialTokens.UNK_TOKEN:
                    try:
                        pos_list = num_stack[b_i].pop()
                        c = num_list[b_i][pos_list[0]]
                        res.append(c)
                    except:
                        res.append(symbol)
                else:
                    res.append(symbol)
            output_list.append(res)
        return output_list

    # def get_all_number_encoder_outputs(self,encoder_outputs, num_pos, num_size, hidden_size):
    #     indices = list()
    #     sen_len = encoder_outputs.size(1)
    #     batch_size=encoder_outputs.size(0)
    #     masked_index = []
    #     temp_1 = [1 for _ in range(hidden_size)]
    #     temp_0 = [0 for _ in range(hidden_size)]
    #     for b in range(batch_size):
    #         for i in num_pos[b]:
    #             indices.append(i + b * sen_len)
    #             masked_index.append(temp_0)
    #         indices += [0 for _ in range(len(num_pos[b]), num_size)]
    #         masked_index += [temp_1 for _ in range(len(num_pos[b]), num_size)]
    #     indices = torch.LongTensor(indices).to(self.device)
    #     masked_index = torch.BoolTensor(masked_index).to(self.device)

    #     masked_index = masked_index.view(batch_size, num_size, hidden_size)
    #     all_outputs = encoder_outputs.contiguous()
    #     all_embedding = all_outputs.view(-1, encoder_outputs.size(2))  # S x B x H -> (B x S) x H
    #     all_num = all_embedding.index_select(0, indices)
    #     all_num = all_num.view(batch_size, num_size, hidden_size)
    #     return all_num.masked_fill_(masked_index, 0.0)


# def replace_masked_values(tensor, mask, replace_with):
#     return tensor.masked_fill((1 - mask).bool(), replace_with)
