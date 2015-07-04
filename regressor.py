from sklearn.ensemble import RandomForestRegressor
from sklearn.base import BaseEstimator
from sklearn.ensemble import AdaBoostRegressor

class Regressor(BaseEstimator):
    def __init__(self):
        cl = RandomForestRegressor(n_estimators=2.7, max_depth=1.9, max_features=10)
        self.clf = AdaBoostRegressor(base_estimator = cl, n_estimators=100)

    def fit(self, X, y):
        self.clf.fit(X, y)

    def predict(self, X):
        return self.clf.predict(X)
#RandomForestClassifier
