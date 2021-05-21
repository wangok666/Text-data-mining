from gensim import corpora
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.feature_extraction.text import TfidfTransformer
import pickle as pkl


# gensim转换成scipy.sparse.csr_matrix
def convert(corpus):
    data = []
    rows = []
    cols = []
    line_count = 0
    for line in corpus:
        for col, value in line:
            rows.append(line_count)
            cols.append(col)
            data.append(value)
        line_count += 1
    matrix = csr_matrix((data, (rows, cols))) # 稀疏向量
    return matrix


def print_dict_new(ch2, dict):
    dict_list_new = ch2.get_support(indices=True).tolist()
    dict_new = []
    for key in dict:
        if key in dict_list_new:
            dict_new.append(dict[key])
    url = 'origin/file/dict_new.txt'
    fp = open(url, 'w', encoding='utf-8')
    for word in dict_new:
        fp.write(word + ', ')
    fp.close()

# n[(A11/n1n1+A12/n1n2+...+Arc/nrnc)-1]
def chi2_test(train_data, test_data, len_features):
    ch2 = SelectKBest(chi2, k=len_features)
    train_data = ch2.fit_transform(train_data, train_label)
    test_data = ch2.transform(test_data)
    return train_data, test_data, ch2

'''
N_w/N,  N_w在某一文本中词条w出现的次数，N是该文本总词条数
IDF_w=log(\frac{Y}{Y_w+1})
其中Y是语料库的文档总数，Y_w是包含词条w的文档数，分母加一是为了避免w未出现在任何文档中从而导致分母为0的情况。
'''
def get_tfidf(train_data, test_data):
    transformer = TfidfTransformer()
    train_data = transformer.fit_transform(train_data)
    test_data = transformer.transform(test_data)
    return train_data, test_data


def write_file(train_data, test_data, len_features):
    train_url = 'origin/dict/tfidf' + str(len_features) + '_train.pkl'
    test_url = 'origin/dict/tfidf' + str(len_features) + '_test.pkl'
    with open(train_url, 'wb') as f:
        pkl.dump(train_data, f)
    with open(test_url, 'wb') as f:
        pkl.dump(test_data, f)

if __name__ == '__main__':
    len_dict = 15000
    len_features = 10000

    train_data = corpora.MmCorpus('origin/dict/bow' + str(len_dict) + '_train.mm')
    train_label = np.load('origin/file/train_label.npy')
    test_data = corpora.MmCorpus('origin/dict/bow' + str(len_dict) + '_test.mm')
    test_label = np.load('origin/file/test_label.npy')

    train_data = convert(train_data)
    test_data = convert(test_data)

    train_data, test_data, ch2 = chi2_test(train_data, test_data, len_features)

    dic = corpora.Dictionary.load('origin/dict/dictionary' + str(len_dict) + '.dict')
    # print_dict_new(ch2, dic)

    train_data, test_data = get_tfidf(train_data, test_data)
    write_file(train_data, test_data, len_features)