import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import numpy as np
from xgboost import XGBClassifier
import sys


def main():
    names = ['Age', 'Workclass', 'fnlwgt', 'Education', 'Education-num',
                   'Marital-status', 'Occupation', 'Relationship', 'Race', 'Sex',
                   'Capital-gain', 'Capital-loss', 'Hours-per-week', 'Native-country', 'target']
    cate = ['Workclass', 'Education', 'Marital-status', 'Occupation', 'Relationship', 'Race', 'Sex', 'Native-country']
    train = pd.read_csv(sys.argv[1], index_col=False, names=names)
    test = pd.read_csv(sys.argv[2], index_col=False, names=names)
    test = test.iloc[:, :-1]
    for x in cate:
        le = preprocessing.LabelEncoder()
        le.fit(train[x].values)
        train[x] = le.transform(train[x].values)
        test[x] = le.transform(test[x].values)
    ignored_feature = ['Marital-status', 'fnlwgt']
    for x in [train, test]:
        x.drop(columns=ignored_feature, inplace=True)
        x['Capital-loss'] = np.log(x['Capital-loss']+1)
        x['Capital-gain'] = np.log(x['Capital-gain']+1)
    train_X, test_X, train_y, test_y = train_test_split(train.iloc[:, :-1], train.iloc[:, -1:], test_size=0)
    boost = XGBClassifier(colsample_bylevel=0.6, colsample_bytree=0.9, gamma=5, max_delta_step=0, max_depth=7,
                          min_child_weight=0, n_estimators=600, subsample=0.8)
    boost.fit(train_X, train_y.values.ravel())
    ans = boost.predict(test)
    test['ans'] = ans
    test = test.iloc[:, -1:]
    test.index.name = 'ID'
    test.to_csv('answer.csv')


if __name__ == '__main__':
    main()
