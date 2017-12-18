import data_processor as dp
from sklearn.neighbors import KNeighborsClassifier
from scipy.sparse import coo_matrix, hstack
from sklearn.linear_model import LogisticRegression
import evaluation

def logistic_regression(X_train, Y_train, X_test):
    model = LogisticRegression()
    model.fit(X_train,Y_train)
    Y_predict = model.predict(X_test)
    return Y_predict