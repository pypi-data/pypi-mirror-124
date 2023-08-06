import numpy as np
from sklearn.neighbors import KDTree
from sklearn.base import BaseEstimator, ClassifierMixin

class WeaklySupervisedKNeighborsClassifier(BaseEstimator, ClassifierMixin):
    '''
    A class to perform classification for weakly supervised data, based on k-nearest neighbors.
    The y input to the fit method should be given as an iterable of DiscreteWeakLabel

    Parameters
    ----------
    :param k: The number of neighbors
    :type k: int, default=3

    :param metric: The metric for neighbors queries
    :type metric: str or callable, default 'minkowski'

    Attributes
    ----------
    :ivar y: A copy of the input y
    :vartype y: ndarray

    :ivar tree: A tree object for nearest neighbors queries speed-up
    :vartype tree: KDTree object

    :ivar n_classes: The number of unique classes in y
    :vartype n_classes: int

    :ivar classes_: The unique classes in y
    :vartype classes: ndarray
    '''
    def __init__(self, k=3, metric='minkowski'):
        self.k = k
        self.metric = metric
        
    def fit(self, X, y):
        """
        Fit the WeaklySupervisedKNeighborsClassifier model
        """
        self.__X = X
        self.__y = y
        
        self.__tree = KDTree(X, metric=self.metric)
        self.__n_classes = y[0].n_classes
        return self

    
    def predict(self, X):
        """
        Returns predictions for the given X
        """
        y_pred = np.zeros(X.shape[0])
        for i in range(X.shape[0]):
            _, indices = self.__tree.query(X[i], self.k)
            classes = np.zeros(self.__n_classes)
            classes += np.add.reduce(self.__y[indices])
            y_pred[i] = np.argmax(classes)
        return y_pred
    
    def predict_proba(self, X):
        """
        Returns probability distributions for the given X
        """
        y_pred = np.zeros((X.shape[0], self.__n_classes))
        for i in range(X.shape[0]):
            _, indices = self.__tree.query(X[i], self.k)
            for j in indices:
                y_pred[i, :] += self.__y[j]
            y_pred[i, :] /= np.sum(y_pred[i,:])
        return y_pred







class WeaklySupervisedRadiusClassifier(BaseEstimator, ClassifierMixin):
    '''
    A class to perform classification for weakly supervised data, based on radius neighbors.
    The y input to the fit method should be given as an iterable of DiscreteWeakLabel

    Parameters
    ----------
    :param radius: The size of the radius
    :type radius: float, default=1.0

    :param metric: The metric for neighbors queries
    :type metric: str or callable, default 'minkowski'

    Attributes
    ----------
    :ivar y: A copy of the input y
    :vartype y: ndarray

    :ivar tree: A tree object for nearest neighbors queries speed-up
    :vartype tree: KDTree object

    :ivar n_classes: The number of unique classes in y
    :vartype n_classes: int

    :ivar classes_: The unique classes in y
    :vartype classes: ndarray
    '''
    def __init__(self, radius=1.0, metric='minkowski'):
        self.radius = radius
        self.metric = metric
        
    def fit(self, X, y):
        """
        Fit the WeaklySupervisedRadiusClassifier model
        """
        self.__X = X
        self.__y = y
        
        self.__tree = KDTree(X, metric=self.metric)
        self.__n_classes = y[0].n_classes
        return self

    
    def predict(self, X):
        """
        Returns predictions for the given X
        """
        y_pred = np.zeros(X.shape[0])
        for i in range(X.shape[0]):
            _, indices = self.__tree.query_radius(X[i], self.radius)
            classes = np.zeros(self.__n_classes)
            classes += np.add.reduce(self.__y[indices])
            y_pred[i] = np.argmax(classes)
        return y_pred
    
    def predict_proba(self, X):
        """
        Returns probability distributions for the given X
        """
        y_pred = np.zeros((X.shape[0], self.__n_classes))
        for i in range(X.shape[0]):
            _, indices = self.__tree.query(X[i], self.radius)
            for j in indices:
                y_pred[i, :] += self.__y[j]
            y_pred[i, :] /= np.sum(y_pred[i,:])
        return y_pred