#!/usr/bin/env python
# -*- coding: utf-8 -*

from libsvm.python.svmutil import *
from libsvm.python.svm import *


def train():
    y, x = svm_read_problem('../data/heart_scale')
    problem = svm_problem(y, x)
    param = svm_parameter('-t 4 -c 4 -b 1')
    m = svm_train(problem, param)
    svm_save_model('../data/heart_scale.model', m)


if __name__ == '__main__':
    train()