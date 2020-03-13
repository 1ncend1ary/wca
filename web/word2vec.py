# -*- coding: utf-8 -*-
"""
Pre-trained word2vec model to compute distance between vectorised words

Programmer: Aleksei Seliverstov <alexseliverstov@yahoo.com>
"""
import gensim
import numpy
import math
import sys


class Vectoriser:
    """
    Words and vectors handling utility class
    """
    __path = 'model/GoogleNews-vectors-negative300.bin'
    __limit = 100000
    __isBinary = True
    print('Starting training', file=sys.stdout, flush=True)
    __model = gensim.models.KeyedVectors.load_word2vec_format(__path, binary=__isBinary, limit=__limit)
    print('Finished training', file=sys.stdout, flush=True)

    def __to_vec(self, word):
        """
        Convert a word to vector using a pre trained model
        """
        vector = None
        for w in word.split():
            try:
                cur_model = self.__model[w]
                if vector is None:
                    vector = cur_model
                else:
                    vector = numpy.add(vector, cur_model)
            except KeyError:
                # Word not found in model
                return None
        return vector

    def sort(self, base, words):
        """
        Sort words based on euclidean distance from base word
        """
        base_vec = self.__to_vec(base)

        sorted_words = sorted(words, key=lambda x: self.__euclidean(base_vec, self.__to_vec(x)))
        print("Interests before sort:", words, file=sys.stdout, flush=True)
        print("Interests after sort:", sorted_words, file=sys.stdout, flush=True)
        return sorted_words

    @staticmethod
    def __pow2(value):
        return math.pow(value, 2)

    def __euclidean(self, vector1, vector2):
        """
        Get euclidean distance between two vectors
        """
        if vector1 is None or vector2 is None:
            return float('inf')
        return math.sqrt(sum(list((map(self.__pow2, map(lambda x, y: x - y, vector1, vector2))))))

    def __new__(cls):
        """
        Declare this class as singleton

        This method is initiated before __init__ and check whether an instance of this class already exists
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(Vectoriser, cls).__new__(cls)
        return cls.instance
