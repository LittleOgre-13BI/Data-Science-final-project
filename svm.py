from sklearn import svm
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


def show_accuracy(y_hat, y_test, str):
    pass


def svm(path):
    # dtype:传入数据类型 delimiter:分隔符
    # 如果需要映射函数的话 converters={2:type_fun}即为将数据第三列通过type_fun()转换成dtype类型
    data = np.loadtxt(path, dtype=int, delimiter=',')

    x, y = np.split(data, (4,), axis=1)
    # x = x[:, :2]
    # test_size:样本占比
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, train_size=0.6)

    # kernel='linear'时为线性核，C越大分类效果约好
    # kernel='rbf'时为高斯核，gamma值越大分类效果越好
    # 'ovr' one v test 一个类别与其他类别进行区分
    # 'ovo' one v one 类别两两之间进行划分
    classifier = svm.SVC(C=0.8, kernel='rbf', gamma=20, decision_function_shape='ovo')

    print("SVM-输出训练集的准确率为：", classifier.score(x_train, y_train))
    y_hat = classifier.predict(x_train)
    show_accuracy(y_hat, y_train, '训练集')
    print("SVM-输出测试集的准确率为：", classifier.score(x_test, y_test))
    y_hat = classifier.predict(x_test)
    show_accuracy(y_hat, y_test, '测试集')


if __name__ == '__main__':
    path = 'D:/data/result.txt'
    file = open(path, 'rb')
    svm(path)
