#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 12/12/2017
# @Author  : wangbiwen
import codecs


def select_feature(input_files, k, output_file):
    '''
    用卡方检验来进行特征选择，对于各个类别中每个词
    根据卡方检验公式计算： N * (AD - BC) ^ 2 / (A + B) * (C + D) * (A + C) * (B + D)
    :param input_files: 各个类别的数据文件list
    :param k: 每个类别选取top k的特征数
    :param output_file: 最后合并各个类别中特征的文件
    :return: 无返回
    '''

    # 统计总文档数，以及各个类别下每个词的文档数
    N = 0
    docs_num_list = []
    for input_file in input_files:
        N += count_docs_in_category(input_file)
        docs_num_list.append(count_docs_in_category_of_each_word(input_file))

    # 计算各个类别中每个词的CHI值（卡方检验值）
    word_chi_value_list = []
    for i, input_file in enumerate(input_files):
        cur_docs_num = count_docs_in_category(input_file)
        cur_word_docs_num_dict = docs_num_list[i]
        word_chi_value_dict = {}
        for word, count in cur_word_docs_num_dict.items():
            # A: 属于属于当前类别，并包含该词的文档数
            A = count
            # B: 不属于当前类别，但包含该词的文档数
            B = 0
            for j, docs_num_dict in enumerate(docs_num_list):
                if i == j:
                    continue
                temp_word_docs_num = docs_num_list[j]
                B += temp_word_docs_num.get(word, 0)
            # C: 属于当前类别，但不包含该词的文档数
            C = cur_docs_num - A
            # D: 不属于当前类别，且不包含该词的文档数
            D = N - cur_docs_num - B
            cur_chi_value = N * (A * D - B * C) ** 2 / (A + B) * (C + D) * (A + C) * (B + D)
            word_chi_value_dict[word] = cur_chi_value
        word_chi_value_list.append(word_chi_value_dict)
    # 从各个类别中选出top K 作为特征词，并合并成个总的特征词表
    feature_set = set()
    for item in word_chi_value_list:
        sorted_list = sorted(item.items(), key=lambda x: x[1], reverse=True)
        feature_list = [temp[0] for temp in sorted_list[:k]]
        feature_set |= set(feature_list)

    # 特征词输出到文本文件
    fout = codecs.open(output_file, 'w', 'utf-8')
    category_tag = 0
    for word in feature_set:
        category_tag += 1
        fout.write(u'{}\t{}\n'.format(category_tag, word))


def count_docs_in_category_of_each_word(category_file):
    '''
    统计各个类别中包含每个词的文档数
    :param category_file: 各个类别的数据
    :return: 每个词出现的文档数的dict
    '''
    fin = codecs.open(category_file, 'r', 'utf-8')
    word_docs_dict = {}
    for line in fin:
        line = line.strip()
        words = line.split('\t')
        word_set = set(words)
        for word in word_set:
            docs_count = word_docs_dict.get(word, 0)
            word_docs_dict[word] = docs_count + 1
    return word_docs_dict


def count_docs_in_category(category_file):
    '''
    统计各个类别中的文档数
    :param category_file: 各个类别数据
    :return: 文档数
    '''
    fin = codecs.open(category_file, 'r', 'utf-8')
    count = 0
    for line in fin:
        count += 1
    return count


if __name__ == '__main__':
    file_list = []
    file_list.append('data/celebrity_washed.txt')
    file_list.append('data/merchant_washed.txt')
    file_list.append('data/pastime_washed.txt')
    k = 500
    feature_file = 'data/feature.txt'
    select_feature(file_list, k, feature_file)
