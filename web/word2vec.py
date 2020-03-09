import gensim
import numpy
import math
import sys

path = 'model/GoogleNews-vectors-negative300.bin'
print('Starting training', file=sys.stdout, flush=True)
model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True, limit=100000)
print('Finished training', file=sys.stdout, flush=True)


def to_vector(word):
    return model[word]


def get_vector(word):
    """
    word - a string (mb with spaces)
    """
    diss = None
    for cat in word.split():
        try:
            cur_model = model[cat]
            if diss is None:
                diss = cur_model
            else:
                diss = numpy.add(diss, cur_model)
                # diss += cur_model
        except KeyError:
            print('Model not found for', cat, file=sys.stdout, flush=True)
            return None
    return diss


def sort_interests(category_name, interests):
    """
    category name - string (mb with spaces)
    interest - list(string)  (every string mb with spaces)
    """
    diss = get_vector(category_name)
    a = []
    # for xy in interests:
    #     a += [euclidian(diss, get_vector(xy))]
    # print(a)

    qq = sorted(interests, key=lambda x: euclidian(diss, get_vector(x)))
    print("Interests before sort:", interests, file=sys.stdout, flush=True)
    print("Interests after sort:", qq, file=sys.stdout, flush=True)
    return qq

    # diss2 = None
    # for inter in interest:
    #     try:
    #         cur_model = model[cat]
    #         if diss is None:
    #             diss = cur_model
    #         else:
    #             diss += cur_model
    #     except KeyError:
    #         print('Model not found for', cat, file=sys.stdout, flush=True)
    #         return -1
    #
    # return euclidian(diss, cat_name)


def pow2(x):
    return math.pow(x, 2)


def euclidian(vector1, vector2):
    if vector1 is None or vector2 is None:
        return float('inf')
    return math.sqrt(sum(list((map(pow2, map(lambda x, y: x - y, vector1, vector2))))))


# print(sort_interests('spaceship', ['hello', 'wow', 'cow', 'microbe', 'nano', 'Britain']))
