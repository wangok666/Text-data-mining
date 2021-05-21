import json
import pymysql
import numpy as np


def insert(cursor, value, topic):

    sql = "INSERT INTO " + topic + "(TITLE,ARTICLE) VALUES (%s, %s)"
    try:
        cursor.execute(sql, value)
        db.commit()
        print('OK')
    except:
        db.rollback()
        print("ERROR")


def fileToMysql(cursor):
    for i in range(0, 3):
        d_one = []
        url = r'F:\dm_lab1\origin\chinanews_extra\chinanews_tw_extra_' + str(i) + '.txt'
        file_one = open(url, encoding='utf-8')
        for line in file_one:
            d_one.append(json.loads(line))
        # topic = ['gj', 'sh', 'ty', 'cj', 'ga', 'js', 'qc', 'wh', 'tw', 'yl']
        num = len(d_one[0])
        for j in range(0, num):
            value = (d_one[0][j]['title'], d_one[0][j]['content'])
            # label = d_one[0][j]['topic']
            insert(cursor, value, 'tw')
            print(i, j)
            # if label not in ['gj', 'sh', 'cj']:
            #     print(label)
                # insert(cursor, value, label)
                # insert(cursor, value, 'qc')
            # print(i, j)
        file_one.close()
    db.close()


def file_delete_none():
    topics = ['yl']
    for topic in topics:
        fp1_url = 'origin/fenci/' + topic + '.txt'
        fp2_url = 'origin/fenci/' + topic + '_new.txt'
        fp1 = open(fp1_url, encoding='utf-8')
        fp2 = open(fp2_url, 'w', encoding='utf-8')
        content = fp1.readline()
        i = 1
        while content:
            outNum = content.split(" ")
            if outNum != ['\n']:
                fp2.writelines(" ".join(outNum))
                i = i + 1
            # if outNum == '\n':
            #     # fp2.write(outNum + '\n')
            #     print(outNum)
            #     i = i + 1
            # print(outNum)
            content = fp1.readline()
        print(topic, 'ok', i)
        fp1.close()
        # fp2.close()


def get_num():
    topics = ['cj', 'ga', 'gj', 'js', 'qc', 'sh', 'tw', 'ty', 'wh', 'yl']
    # topics = ['js']
    for topic in topics:
        fp1_url = 'origin/fenci/' + topic + '.txt'
        fp1 = open(fp1_url, encoding='utf-8')
        content = fp1.readlines()
        print(topic, len(content))
        fp1.close()
    # with open('origin/fenci/qc.txt', 'rb') as lines:
    #     count = 0
    #     for line in lines:
    #         count = count + 1
    #     print(count)

def file_copy():
    topics = ['gj', 'cj', 'sh', 'qc']
    for topic in topics:
        fp1_url = 'origin/fenci/' + topic + '.txt'
        fp2_url = 'origin/fenci/' + topic + '_new.txt'
        fp1 = open(fp1_url, encoding='utf-8')
        fp2 = open(fp2_url, 'w', encoding='utf-8')
        content = fp1.readline()
        i = 1
        while i <= 120000:
            fp2.writelines(content)
            i = i + 1
            content = fp1.readline()
        print(topic, 'ok', i)
        fp1.close()
        fp2.close()


if __name__ == '__main__':
    # get_num()
    a1 = np.array(
        [
            [1/2, 0, 0],
            [0, 1/3, 0],
            [0, 0, 1/4]
        ]
    )
    a2 = np.array(
        [
            [1, 2, 3, 4, 5],
            [6, 7, 8, 9, 10],
            [11, 12, 13, 14, 15]
        ]
    )
    print(a1.dot(a2))
'''
gj 187272
sh 327974
ty 78551 
cj 187608
ga 31989
js 22272 
qc 10000
wh 58367
tw 34907
yl 46287
'''

'''
gj 187272 !
sh 327974 !
ty 82822 + 17890 = 109736 !
cj 187608 !
ga 52926 + 26914 !
js 74022 + 5951 !
qc 60000 + 68000
wh 61005 + 40152
tw 66330 + 27374
yl 82822 + 20026
'''
'''
gj 125000
sh 125000
ty 100616
cj 125000
ga 78539
js 76052
qc 125000
wh 101057
tw 91613
yl 78030
'''