import data_processor as dp
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
import evaluation 
# import get_matrix

def naive_bayes(X_train, Y_train, X_test, bernoulli = True):
	if bernoulli:
		print("FITTING DATA")
		clf = BernoulliNB().fit(X_train, Y_train)
	else:
		clf = MultinomialNB().fit(X_train, Y_train)
	Y_predict = clf.predict(X_test)
	print()
	return Y_predict
	# print("Percent_Correctness : " + str(evaluation.Percent_Correctness(Y_predict,Y_test)))
	# print("f_score: " + str(evaluation.f_score(Y_predict,Y_test)))

# if __name__ == "__main__":
	# X_train, Y_train = dp.pipeline_process_data('trainingData', haveTarget = True)
	# X_test = dp.pipeline_process_data('http://www.cnn.com/')
	# naive_bayes(X_train, Y_train, X_test, bernoulli = False)