import data_processor as dp

import knn
import lg
import naive_bayes as nb


def getKeywordsFromResult(model, Y_test, data):
	documents = []
	for i, (k, v) in enumerate(data.items()):
		if Y_test[i] == 'bad':
			documents.append(v)
	# print("\n\n", "bad news found: ",len(documents))
	dp.getKeywords(model,documents)

def main(paths, dataNum = 20000,  remove_stop_word = True,
	stem = True, lamma = True, bigram = True):
	X_train, Y_train = dp.pipeline_process_data('trainingData', dataNum = 499, haveTarget = True)
	
	X_test,data = dp.pipeline_process_data(paths, dataNum = 500)


	print("\n\nfinish process data...")
	# print ("bernoulli nb")
	# Y_test = nb.naive_bayes(X_train,Y_train,X_test, bernoulli = True)
	# getKeywordsFromResult("bnb", Y_test, data)

	print ("\n\nModel used: mutinomial nb")
	Y_test = nb.naive_bayes(X_train,Y_train, X_test, bernoulli = False)
	getKeywordsFromResult("mnb", Y_test, data)

	# print ("knn")
	# Y_test = knn.knn(X_train,Y_train, X_test, neighbor = 22)
	# getKeywordsFromResult("knn",Y_test, data)


	# print ("lg")
	# Y_test = lg.logistic_regression(X_train, Y_train, X_test)
	# getKeywordsFromResult("lg",Y_test, data)


if __name__ == "__main__":
	paths = ['http://www.cnn.com/', "http://www.foxnews.com/", 'http://www.usatoday.com/' ]
	main(paths)