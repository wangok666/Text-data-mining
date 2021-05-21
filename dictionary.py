import os
import numpy as np
from gensim import corpora
from bunch import get_train_data
from bunch import get_test_data


def get_dictionary(corpus, len_dict, dir='origin/dict/'):
    '''
    :param corpus: 分词后的语料，多维度list
    :param len_dict: 字典的长度
    :param dir: 保存位置
    :return: 字典对象
    '''
    url = dir + 'dictionary' + str(len_dict) + '.dict'
    if os.path.exists(url):
        print('dictionary has exist.')
        dict = corpora.Dictionary.load(url)
    else:
        dict = corpora.Dictionary(corpus)
        dict.filter_extremes(no_below=5, no_above=0.5, keep_n=len_dict)
        dict.compactify()   # 除去多余的空格
        print('saving dictionary.', url)
        dict.save(url)
    return dict


def print_dict(dic):
    for key in dic:
        print(key, dic[key])


def dict_file(dic, dic_len):
    path = 'origin/file/dic' + str(dic_len) + '.txt'
    fp = open(path, 'w', encoding='utf-8')
    for key in dic:
        if dic[key] != '\n':
            fp.writelines(dic[key] + '\n')
    fp.close()


def get_bow(corpus, dictionary, dir='origin/dict/', type='train'):
    """
    通过下面一句得到语料中每一篇文档对应的稀疏向量（这里是bow向量） 即 词袋模型
    向量的每一个元素代表了一个word在这篇文档中出现的次数
    :param corpus: 语料
    :param dictionary: 词典
    :return: 词袋bow
    """
    url = dir + 'bow' + str(len(dictionary)) + '_' + type + '.mm'
    if os.path.exists(url):
        print('bow has exist')
        bow = corpora.MmCorpus(url)
    else:
        bow = [dictionary.doc2bow(doc) for doc in corpus]
        print('saving bow.', url)
        corpora.MmCorpus.serialize(url, bow)
    return bow


if __name__ == '__main__':
    len_dictionary = 15000
    train_data, train_label = get_train_data()
    # np.save('origin/file/train_label.npy', train_label)
    # train_data = []
    # train_label = []
    # dictionary = get_dictionary(train_data, len_dictionary)
    # print_dict(dictionary)
    # dict_file(dictionary, len_dictionary)
    # train_bow = get_bow(train_data, dictionary, type='train')
    # print('bow', type(train_bow), len(train_bow))

    # test_data, test_label = get_test_data()
    # np.save('origin/file/test_label.npy', test_label)
    # test_bow = get_bow(test_data, dictionary, type='test')
    # print('bow', type(test_bow), len(test_bow))

