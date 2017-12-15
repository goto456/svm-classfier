#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 12/14/2017
# @Author  : wangbiwen
import codecs

import math


def calculate_vectors(category_file_list, feature_tag_dict, output_file):
    feature_idf = calculate_feature_idf(category_file_list, set(feature_tag_dict.keys()))
    fout = codecs.open(output_file, 'w', 'utf-8')
    for i, category_file in enumerate(category_file_list):
        fin = codecs.open(category_file, 'r', 'utf-8')
        for line in fin:
            words = line.split('\t')
            word_count_dict = {}
            word_count = 0
            for word in words:
                if word not in feature_tag_dict:
                    continue
                word_count += 1
                count = word_count_dict.get(word, 0)
                word_count_dict[word] = count + 1
            # 计算每个词的TF值，并与之间计算的IDF值一起计算TF-IDF值
            vectors_dict = {}
            for word, count in word_count_dict.items():
                tf = count / word_count
                tf_idf = tf * feature_idf[word]
                feature_tag = int(feature_tag_dict[word])
                vectors_dict[feature_tag] = str(tf_idf)
            # 生成libsvm数据格式的行
            if len(vectors_dict) > 0:
                sorted_list = sorted(vectors_dict.items(), key=lambda x: x[0])
                print(sorted_list)
                vectors = [str(item[0]) + ':' + item[1] for item in sorted_list]
                output_line = str(i + 1) + ' ' + ' '.join(vectors)
                fout.write(u'{}\n'.format(output_line))


def calculate_feature_idf(category_file_list, features):
    '''
    计算feature词的IDF
    :param category_file_list: 各个类别的数据文件list
    :param features: feature词的集合
    :return: feature词的idf映射
    '''
    all_docs_num = 0
    feature_docs_count = {}
    for category_file in category_file_list:
        fin = codecs.open(category_file, 'r', 'utf-8')
        for line in fin:
            all_docs_num += 1
            words = line.split('\t')
            word_set = set(words)
            for feature in features:
                if feature not in word_set:
                    continue
                count = feature_docs_count.get(feature, 0)
                feature_docs_count[feature] = count + 1
    # 根据IDF公式来计算feature词的IDF值
    feature_idf = {}
    for feature, count in feature_docs_count.items():
        idf = math.log2(all_docs_num / count)
        feature_idf[feature] = idf
    return feature_idf


def read_features(feature_file):
    '''
    读入feature文件并返回feature词到编号的映射dict
    :param feature_file: feature文件
    :return: feature词到编号的映射dict
    '''
    feature_tag_dict = {}
    fin = codecs.open(feature_file, 'r', 'utf-8')
    for line in fin:
        items = line.split('\t')
        if len(items) == 2:
            feature_tag_dict[items[1].strip()] = items[0].strip()
    return feature_tag_dict


if __name__ == '__main__':
    feature_file = 'data/feature.txt'
    feature_tag_dict = read_features(feature_file)
    category_file_list = []
    category_file_list.append('data/celebrity_washed.txt')
    category_file_list.append('data/merchant_washed.txt')
    category_file_list.append('data/pastime_washed.txt')
    vector_file = 'data/vectors.txt'
    calculate_vectors(category_file_list, feature_tag_dict, vector_file)
