# -*- coding: utf-8 -*-
import re
import jieba.posseg
import MySQLdb


def get_stopwords(path):
    '''
    :param path: 停用词列表文件地址
    :return: 停用词表list
    '''
    stopwords = []
    for word in open(path, 'r'):
        stopwords.append(word.strip())
    return stopwords


def word_segment():
    '''
    :return: jieba.posseg.cut
    '''
    # 连接数据库
    db = MySQLdb.connect("localhost", "root", "123456", "dm", charset='utf8')
    cursor = db.cursor()

    stopwords = get_stopwords('stop_words_ch.txt')

    topics = ['cj', 'ga', 'gj', 'jk', 'js', 'sh', 'tw', 'ty', 'wh', 'yl']

    for j in range(len(topics)):
        i = 1

        sql = 'select article from ' + topics[j]
        cursor.execute(sql)
        results = cursor.fetchall()
        # print(len(results))

        path2 = r"WordCut\\" + topics[j] + ".txt"
        write_file = open(path2, "a", encoding='utf-8')

        for row in results:
            contents = []
            content = re.sub("[@·《》、.%，。？“”（）：(\u3000)(\xa0)！… ；▼]|[a-zA-Z0-9]|['月''日''年']", "", row[0])
            words = jieba.posseg.cut(content)
            for w in words:
                if w.word not in stopwords and w.flag == 'n':
                    contents.append(w.word)

            write_file.writelines(str(i) + ' ' + " ".join(contents) + '\n')
            print(topics[j], i)

            i = i+1

        write_file.close()
    cursor.close()


if __name__ == "__main__":
    word_segment()
