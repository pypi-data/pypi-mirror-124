import numpy as np
import pandas as pd
import wuml

from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier

class classification:
	'''
	Automatically run classification on data

	data: can be any data type
	classifier='GP', 'SVM', 'RandomForest', 'KNN', 'NeuralNet'
	split_train_test: automatically splits the data, default is true
	'''

	def __init__(self, data, y=None, y_column_name=None, split_train_test=True, classifier='GP', kernel=None, 
				networkStructure=[(100,'relu'),(100,'relu'),(1,'none')], max_epoch=500, learning_rate=0.001	):
		NP = wuml.ensure_numpy
		S = np.squeeze

		X = NP(data)
		if y is not None:
			y = S(NP(y))
		elif y_column_name is not None:
			y = data[y_column_name].values
		elif type(data).__name__ == 'wData':
			y = data.Y
		else: raise ValueError('Undefined label Y')

		if split_train_test:
			X_train, X_test, y_train, y_test = wuml.split_training_test(data, label=y, xdata_type="%.4f", ydata_type="%.4f")
		else:
			X_train = X
			y_train = y

		if classifier == 'GP':
			kernel = 1.0 * RBF(1.0) 
			model = GaussianProcessClassifier(kernel=kernel, random_state=0)
		elif classifier == 'SVM':
			model = make_pipeline(StandardScaler(), SVC(gamma='auto'))
		elif classifier == 'RandomForest':
			model = RandomForestClassifier(max_depth=3, random_state=0)
		elif classifier == 'KNN':
			model = KNeighborsClassifier(n_neighbors=4)
		elif classifier == 'NeuralNet':
			model = MLPClassifier(random_state=1, max_iter=400)

		model.fit(NP(X_train), S(NP(y_train)))
		self.ŷ_train = model.predict(NP(X_train))
		self.Train_acc = wuml.accuracy(S(NP(y_train)), self.ŷ_train)

		if split_train_test:
			self.ŷ_test = model.predict(NP(X_test))
			self.Test_acc = wuml.accuracy(S(NP(y_test)), self.ŷ_test)

		self.split_train_test = split_train_test
		self.model = model
		self.classifier = classifier
		self.kernel = kernel

	def result_summary(self, print_out=True):
		NPR = np.round

		if self.split_train_test:
			column_names = ['classifier', 'Train', 'Test']
			data = np.array([[self.classifier, NPR(self.Train_acc, 4) , NPR(self.Test_acc, 4)]])
		else:
			column_names = ['classifier', 'Train']
			data = np.array([[self.classifier, NPR(self.Train_acc, 4)]])

		df = pd.DataFrame(data, columns=column_names,index=[''])
		if print_out: print(df)
		return df



	def __call__(self, data):
		X = wuml.ensure_numpy(data)	

		[self.ŷ, self.σ] = model.predict(X, return_std=True)

		output = self.model.predict(X, return_std=True, return_cov=False)
		return wuml.ensure_data_type(output, type_name=type(data).__name__)
		#else: raise ValueError('Regressor not recognized, must use regressor="GP"')
		

	def __str__(self):
		return str(self.result_summary(print_out=False))


def run_every_classifier(data, y=None, y_column_name=None, order_by='Test'):
	'''
	order_by: 'Test', 'Train'
	'''
	regressors=['GP', 'SVM', 'RandomForest', 'KNN', 'NeuralNet']

	df = pd.DataFrame()
	for reg in regressors:
		reg = classification(data, y=y, classifier=reg)
		df = df.append(reg.result_summary(print_out=False))

	df = df.sort_values(order_by, ascending=False)
	return df

