from sklearn.ensemble import RandomForestRegressor
from sklearn.base import BaseEstimator
from sklearn.ensemble import AdaBoostRegressor

class Regressor(BaseEstimator):
    def __init__(self):
        cl = RandomForestRegressor(n_estimators=12, max_depth=39, max_features=8)
        self.clf = AdaBoostRegressor(base_estimator = cl, n_estimators=50)

    def fit(self, X, y):
        self.clf.fit(X, y)

    def predict(self, X):
        return self.clf.predict(X)
#RandomForestClassifier
