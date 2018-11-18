import pandas as pd
from sklearn import preprocessing, ensemble
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import KFold, train_test_split
from sklearn.metrics import f1_score
import numpy as np


def main():
    names = ['Age', 'Workclass','fnlwgt', 'Education', 'Education-num',
                   'Marital-status', 'Occupation', 'Relationship', 'Race', 'Sex',
                   'Capital-gain', 'Capital-loss', 'Hours-per-week', 'Native-country', 'target']
    cate = ['Workclass', 'Education', 'Marital-status', 'Occupation', 'Relationship', 'Race', 'Sex', 'Native-country']
    train = pd.read_csv('train.csv', index_col=False, names=names)
    test = pd.read_csv('test.csv', index_col=False, names=names)
    test = test.iloc[:, :-1]
    for x in cate:
        le = preprocessing.LabelEncoder()
        le.fit(train[x].values)
        train[x] = le.transform(train[x].values)
        test[x] = le.transform(test[x].values)
    ignored_feature = ['Marital-status', 'fnlwgt']
    train.drop(columns=ignored_feature, inplace=True)
    test.drop(columns=ignored_feature, inplace=True)
    train_X, test_X, train_y, test_y = train_test_split(train.iloc[:, :-1], train.iloc[:, -1:], test_size=0)
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    xx = []
    for a in np.linspace(2000,2000,1):
        ans = []
        for train_index, test_index in kf.split(train_X):
            X_train, X_test = train_X.iloc[train_index, :], train_X.iloc[test_index, :]
            y_train, y_test = train_y.iloc[train_index, :], train_y.iloc[test_index, :]
            boost = ensemble.AdaBoostClassifier(DecisionTreeClassifier(max_depth=1, class_weight={0:1, 1:1.189}), n_estimators = int(a))
            boost_fit = boost.fit(X_train, y_train.values.ravel())
            y_predict = boost.predict(X_test)
            ans.append(f1_score(y_test, y_predict, average='weighted'))
        print(a, np.mean(ans))
        xx.append(np.mean(ans))
    ans = boost.predict(test)
    test['ans'] = ans
    test = test.iloc[:, -1:]
    test.index.name = 'ID'
    test.to_csv('sub.csv')


if __name__ == '__main__':
    main()
