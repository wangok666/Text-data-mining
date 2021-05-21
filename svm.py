import pickle as pkl
import numpy as np
from sklearn.svm import LinearSVC, SVC
from sklearn import metrics
import sklearn.metrics as sm
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

def linersvm(train_tfidf, train_label, test_tfidf, test_label, model_dir='./linersvm.pkl'):
    train_start = datetime.datetime.now()
    clf = LinearSVC()
    clf.fit(train_tfidf, train_label)
    train_end = datetime.datetime.now()
    with open(model_dir, 'wb') as f:
        pkl.dump(clf, f)
    train_time = train_end - train_start
    print('train time:', train_time)
    test_start = datetime.datetime.now()
    y_pred = clf.predict(test_tfidf)
    test_end = datetime.datetime.now()
    test_time = test_end - test_start
    print('test time:', test_time)

    confusion_matrix = sm.confusion_matrix(test_label, y_pred)
    con_mat_norm = confusion_matrix.astype('float') / confusion_matrix.sum(axis=1)[:, np.newaxis]  # 归一化
    con_mat_norm = np.around(con_mat_norm, decimals=2)
    # === plot ===
    plt.figure(figsize=(8, 8))
    sns.heatmap(con_mat_norm, annot=True, cmap='Blues')
    plt.ylim(0, 10)
    plt.xlabel('Predicted labels')
    plt.ylabel('True labels')
    plt.show()

    print('the metrics of linersvm on train set: ')
    print(metrics.accuracy_score(test_label, y_pred))
    print(metrics.confusion_matrix(test_label, y_pred))
    r = sm.classification_report(test_label, y_pred)
    print('分类报告为：', r, sep='\n')


def svm(train_tfidf, train_label, test_tfidf, test_label, model_dir='./svm.pkl'):
    clf = SVC(kernel='rbf', C=1000)
    clf.fit(train_tfidf, train_label)

    with open(model_dir, 'wb') as f:
        pkl.dump(clf, f)

    y_pred = clf.predict(test_tfidf)
    print('the metrics of svm on train set: ')
    print(metrics.accuracy_score(test_label, y_pred))
    print(metrics.confusion_matrix(test_label, y_pred))


if __name__ == '__main__':
    len_features = 10000

    with open('origin/dict/tfidf' + str(len_features) + '_train.pkl', 'rb') as f:
        train_tfidf = pkl.load(f)
    train_label = np.load('origin/file/train_label.npy')
    with open('origin/dict/tfidf' + str(len_features) + '_test.pkl', 'rb') as f:
        test_tfidf = pkl.load(f)
    test_label = np.load('origin/file/test_label.npy')


    linersvm(train_tfidf, train_label, test_tfidf, test_label, model_dir='origin/dict/linersvm{}.pkl'.format(len_features))
    # svm(train_tfidf, train_label, test_tfidf, test_label, model_dir='origin/dict/svm{}.pkl'.format(len_features))

'''
train time: 0:00:20.620441
test time: 0:00:00.264298
the metrics of linersvm on train set: 
0.9675098892674451
[[58657    45   153    79   289   284    57    37   281   117]
 [  107 37651   207   104    73   132   426   153   162   254]
 [  392   132 57160   701   127   367   131   143   670   176]
 [  128    53   670 35933    68   263   122    73   522   193]
 [  265    17    67    39 59208   195    17    51    53    87]
 [  505    46   225   246   210 57591    63    85   830   198]
 [   63   283   149    98    36    98 44512   110   203   254]
 [   33    52    91    52    52    85    95 49623    72   152]
 [  346    22   424   354    44   645   112    60 48138   383]
 [  119    50   101    79    35   227   132    65   432 48770]]
分类报告为：
             precision    recall  f1-score   support

          0       0.97      0.98      0.97     59999
          1       0.98      0.96      0.97     39269
          2       0.96      0.95      0.96     59999
          3       0.95      0.94      0.95     38025
          4       0.98      0.99      0.99     59999
          5       0.96      0.96      0.96     59999
          6       0.97      0.97      0.97     45806
          7       0.98      0.99      0.99     50307
          8       0.94      0.95      0.94     50528
          9       0.96      0.98      0.97     50010

avg / total       0.97      0.97      0.97    513941
'''
