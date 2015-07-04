
from sklearn.base import BaseEstimator
from sklearn.ensemble import BaggingRegressor, RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor, AdaBoostRegressor, GradientBoostingRegressor

class Regressor(BaseEstimator):
    def __init__(self):
 #       cl = RandomForestRegressor(n_estimators=31, max_depth=25, max_features=20, n_jobs=4)
#base_estimator = cl
        self.clf1 = ExtraTreesRegressor(n_estimators=500, max_depth = 10, bootstrap = True, n_jobs= 1)

        self.clf2 = BaggingRegressor(n_estimators=500, max_features=10, bootstrap=True, bootstrap_features=True, n_jobs=1)
        cl = RandomForestRegressor(n_estimators=31, max_depth=25, max_features=20, n_jobs=1)
        self.clf3 = AdaBoostRegressor(base_estimator = cl, n_estimators=39)
        self.clf4 = GradientBoostingRegressor(n_estimators = 500, max_depth = 25, max_features = 20)
    def fit(self, X, y):
        self.clf1.fit(X, y)
        self.clf2.fit(X, y)
        self.clf3.fit(X, y)
        self.clf4.fit(X, y)

    def predict(self, X):
        return (self.clf1.predict(X) +self.clf2.predict(X) +self.clf3.predict(X) +self.clf4.predict(X))/4
