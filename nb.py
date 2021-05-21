import pickle as pkl
import numpy as np
from scipy.sparse import diags
from sklearn import metrics
import sklearn.metrics as sm
import datetime


len_features = 10000
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



with open('origin/dict/tfidf'+ str(len_features) + '_train.pkl', 'rb') as f:
    train_tfidf = pkl.load(f)
train_label = np.load('origin/file/train_label.npy')
with open('origin/dict/tfidf'+ str(len_features) + '_test.pkl', 'rb') as f:
    test_tfidf = pkl.load(f)
test_label = np.load('origin/file/train_label.npy')

train_start = datetime.datetime.now()
scores = np.ones((len(np.unique(train_label)), train_tfidf.shape[1]))   # 10*10000
for i in range(len(train_label)):
    doc = train_tfidf[i].toarray().flatten()  # tfidf shape (513941, 10000)
    scores[train_label[i]] += doc     # total to 10*10000
# print(scores.shape)
rowsum = scores.sum(1)  # row total
p_label = []
sum = np.sum(rowsum)
for i in range(len(np.unique(train_label))):
    p_label.append(rowsum[i]/sum)
p_label = np.array(p_label)
r_inv = np.power(rowsum, -1).flatten()
sp_ma = diags(r_inv)    # 对角线矩阵
# print(r_mat_inv.shape)
scores = sp_ma.dot(scores) # score 10*10000
train_end = datetime.datetime.now()
train_time = train_end - train_start
print('train time:', train_time)

test_start = datetime.datetime.now()
y_pred = []
for i in range(test_tfidf.shape[0]):
    doc = test_tfidf[i]
    doc = doc.toarray().flatten()
    tmp = scores.dot(doc)*p_label
    y_pred.append(tmp.argmax())
test_end = datetime.datetime.now()
test_time = test_end - test_start
print('test time:', test_time)

print(metrics.accuracy_score(test_label, y_pred))
print(metrics.confusion_matrix(test_label, y_pred))
r = sm.classification_report(test_label, y_pred)
print('分类报告为：', r, sep='\n')

'''
train time: 0:00:51.291757
test time: 0:00:59.355152
0.8945365324035249
[[52106   287   797   147  3898   958   294   444   757   311]
 [ 1274 31368  1216   194   909   508  1001   862  1134   803]
 [ 1359   390 52652   866  1189   741   736   943   669   454]
 [  351   174  1291 32082  1456   617   507   783   402   362]
 [  134    48    26     5 59418   175    33    97    11    52]
 [ 1550   223  1843   209  1406 51832   241   655  1390   650]
 [  584   192   750   303   599   372 40698   410  1138   760]
 [  101    37   178    14   228   107   138 49076   226   202]
 [  351   178   590   664   759  1227   507   688 42971  2593]
 [  175   157    73    22   313   287   458   500   489 47536]]
分类报告为：
             precision    recall  f1-score   support

          0       0.90      0.87      0.88     59999
          1       0.95      0.80      0.87     39269
          2       0.89      0.88      0.88     59999
          3       0.93      0.84      0.88     38025
          4       0.85      0.99      0.91     59999
          5       0.91      0.86      0.89     59999
          6       0.91      0.89      0.90     45806
          7       0.90      0.98      0.94     50307
          8       0.87      0.85      0.86     50528
          9       0.88      0.95      0.92     50010

avg / total       0.90      0.89      0.89    513941

'''