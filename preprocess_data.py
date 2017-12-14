#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 12/12/17
# @Author  : wangbiwen

import codecs

stopwords = set()


def init_stopwords(stopwords_file):
    fin = codecs.open(stopwords_file, 'r', 'utf-8')
    for line in fin:
        line = line.strip()
        stopwords.add(line)


init_stopwords('data/stopwords.txt')


def preprocess(input_file, output_file):
    fin = codecs.open(input_file, 'r', 'utf-8')
    fout = codecs.open(output_file, 'w', 'utf-8')

    for line in fin:
        line = line.strip()
        # line = wash_label(line)
        line = wash_stopwords(line)
        fout.write(u'{}\n'.format(line))


def wash_label(line):
    labels = line.split('||')
    words = []
    for label in labels:
        items = label.split('/')
        word = items[0]
        words.append(word)
    return '\t'.join(words)


def wash_stopwords(line):
    words = line.split('\t')
    need_words = []
    for word in words:
        if len(word) < 2:
            continue
        if word in stopwords:
            continue
        need_words.append(word)
    return '\t'.join(need_words)


if __name__ == '__main__':
    # preprocess('data/celebrity_label.txt', 'data/celebrity_splited.txt')
    # preprocess('data/merchant_label.txt', 'data/merchant_splited.txt')
    # preprocess('data/pastime_label.txt', 'data/pastime_splited.txt')

    preprocess('data/celebrity_splited.txt', 'data/celebrity_washed.txt')
    preprocess('data/merchant_splited.txt', 'data/merchant_washed.txt')
    preprocess('data/pastime_splited.txt', 'data/pastime_washed.txt')
