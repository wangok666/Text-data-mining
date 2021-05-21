from gensim import corpora


def file_dict(dir='origin/fenci/'):
    data = []

    category = 'ga'
    url = dir+'{}.txt'.format(category)
    fp = open(url, encoding='utf-8')
    contents = fp.readlines()
    length = len(contents)
    for i in range(length):
        data.append(contents[i][:-1].split(" "))
    fp.close()
    dictionary = corpora.Dictionary(data)
    dictionary.filter_extremes(no_below=5, no_above=0.5, keep_n=1000)
    dictionary.compactify()

    path = 'origin/file_dict/' + category + '.txt'
    dict_file(path, dictionary)

def dict_file(path, dic):

    fp = open(path, 'w', encoding='utf-8')
    for key in dic:
        if dic[key] != '\n':
            fp.writelines(dic[key] + '\n')
    fp.close()


def del_high():
    dic_path ='origin/file_dict/' + 'ga' + '.txt'

    fp = open(dic_path, encoding='utf-8')
    datas = []
    contents = fp.readlines()
    length = len(contents)
    for i in range(length):
        datas.append(contents[i][:-1])
    fp.close()

    fenci_path = 'origin/fenci/' + 'cj' + '.txt'
    file_path = 'origin/fenci_new/' + 'cj' + '.txt'
    fp_read = open(fenci_path, encoding='utf-8')
    fp_write = open(file_path, 'w', encoding='utf-8')
    contents = fp_read.readlines()
    for content in contents:
        content = content.split(' ')
        for data in datas:
            if data in content:
                content.remove(data)
        fp_write.writelines(' '.join(content))
    fp_read.close()
    fp_write.close()


if __name__ == '__main__':
    file_dict()
    # del_high()
