from sklearn.datasets.base import Bunch
import pickle
import os
import numpy as np

train_bunch_path = "origin/file/train_bunch.dat"
test_bunch_path = "origin/file/test_bunch.dat"
topics = {
    '财经': 0,
    '港澳': 1,
    '国际': 2,
    '军事': 3,
    '汽车': 4,
    '社会': 5,
    '台湾': 6,
    '体育': 7,
    '文化': 8,
    '娱乐': 9
}

def get_bunch(type, wordbag_path):
    '''
    bunch对象持久化
    :param type: train test
    :param wordbag_path: bunch文件路径
    :return:
    '''
    if os.path.exists(wordbag_path):
        print(type + 'bunch对象已经存在')
        bunch = read_bunch(wordbag_path)
        return bunch
    else:
        bunch = Bunch(target_name=[], label=[], filenames=[], contents=[])

        catelist = ['cj', 'ga', 'gj', 'js', 'qc',
                    'sh', 'tw', 'ty', 'wh', 'yl']
        label = ['财经', '港澳', '国际', '军事', '汽车',
                 '社会', '台湾', '体育', '文化', '娱乐']
        bunch.target_name.extend(label)  # 将类别信息保存到Bunch对象

        for i in range(len(catelist)):
            topic = catelist[i]
            path = 'origin/fenci/' + topic + '.txt'

            fp = open(path, encoding='utf-8')
            contents = fp.readlines()
            num = len(contents)
            fp.close()

            fp = open(path, encoding='utf-8')
            count = 1
            while count < num/2:
                # train
                if type == 'train':
                    content = fp.readline()
                    bunch.label.append(label[i])
                    bunch.filenames.append(path)
                    bunch.contents.append(content[:-1])
                    content = fp.readline()
                    count = count + 1
                # test
                else:
                    content = fp.readline()
                    content = fp.readline()
                    bunch.label.append(label[i])
                    bunch.filenames.append(path)
                    bunch.contents.append(content[:-1])
                    count = count + 1
            print(label[i] + ' ' + type + ' set number:' + str(count-1))
            fp.close()

        write_bunch(wordbag_path, bunch)
        print("构建文本对象结束")
        return bunch


def write_bunch(path, bunch):
    file_obj = open(path, "wb")
    pickle.dump(bunch, file_obj)
    file_obj.close()


def read_bunch(path):
    file_obj = open(path, "rb")
    bunch = pickle.load(file_obj)
    file_obj.close()
    return bunch

def get_train_data():
    train_bunch = get_bunch('train', train_bunch_path)



    train_data = []
    train_label = []


    train_length = len(train_bunch.contents)
    for i in range(train_length):
        train_data.append(train_bunch.contents[i].split(" "))
        train_label.append(topics[train_bunch.label[i]])
    print('训练集bunch', len(train_data))
    return train_data, train_label

def get_test_data():
    test_bunch = get_bunch('test', test_bunch_path)
    test_data = []
    test_label = []
    test_length = len(test_bunch.contents)
    for i in range(test_length):
        test_data.append(test_bunch.contents[i].split(" "))
        test_label.append(topics[test_bunch.label[i]])

    print('测试集bunch', len(test_data))
    return test_data, test_label
