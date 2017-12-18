import data_processor as dp
import evaluation
from sklearn.neighbors import KNeighborsClassifier
from scipy.sparse import coo_matrix, hstack

def knn(X_train, Y_train, X_test, neighbor = 78):
	'''
		evaluate accuracy on knn model

		input:
			feature:
			target:
			n_train: praction of train data
			neighbor: number of k
		output:
			(float) accuracy on test data
	'''
	neigh = KNeighborsClassifier(n_neighbors = neighbor)
	neigh.fit(X_train,Y_train)

	Y_predict = neigh.predict(X_test)
	# evaluate
	# if(analyze_pos_neg):
	# 	print("Percent_Correctness : " + str(evaluation.Percent_Correctness(Y_predict,Y_test)))
	# 	print("f_score: " + str(evaluation.f_score(Y_predict,Y_test)))
	# else:
	# 	print("Percent_Correctness: " + str(evaluation.Percent_Correctness(Y_predict,Y_test)))
	# return evaluation.Percent_Correctness(Y_predict,Y_test)
	return Y_predict
