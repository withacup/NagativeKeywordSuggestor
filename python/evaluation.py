def Percent_Correctness(predict_y, test_y):
	'''
		evluate result use Percent_Correctness
	'''
	right = 0
	for i in range(len(test_y)):
		if(predict_y[i] == test_y[i]):
			right+=1.
	return right/len(test_y)


def f_score(predict_y, test_y):
	'''
		evluate result use f_score
		F1 = 2 * (precision * recall) / (precision + recall)
	'''
	TN, TP, FN, FP = 0, 0, 0, 0
	print(predict_y, test_y)
	for i in range(len(test_y)):
		if(predict_y[i] == 'good'):
			if(test_y[i] == 'good'):
				TP += 1.
			else:
				FP += 1.
		else:
			if(test_y[1] == 'bad'):
				TN += 1.
			else:
				FN += 1.
	precision = TP / (TP+FP)
	recall = TP / (TP+FN)
	print(precision, recall)
	return 2*(precision*recall)/(precision+recall)

def mse(predict_y, test_y):
	'''
		evaluate result use mse score
		mse = 1/n * (sum_{i = 1}^n(\hat(yi) - yi)^2)
	'''
	mse = 0.
	for i in range(len(test_y)):
		mse += (predict_y[i] - test_y[i])**2
	return mse / len(test_y)

