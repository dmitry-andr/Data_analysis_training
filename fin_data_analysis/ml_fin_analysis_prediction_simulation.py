# Load libraries
import pandas
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import os

#custom modules imports
import utils


DISPLAY_PLOTS = False


print("\n*** Starting ML classifier ***\n")

# Load dataset

'''
#Irirs demo dataset
url = "data/ml_data_generated/iris.data.csv"
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
dataset = pandas.read_csv(url, names=names)
'''


#Indexes demo dataset
url = "data/ml_data_generated/resulting_data.csv"
names = ['date', 'dj', 'nd', 'sp','gld', 'eur_usd', 'class']#['date', 'dj', 'nd', 'sp', 'class']
#dataset = pandas.read_csv(url, names=names)
dataset = pandas.read_csv(url, names=names, usecols=['dj', 'nd', 'sp', 'gld', 'class'])#usecols=['dj', 'nd', 'sp', 'gld', 'class']





print("dataset shape")
print(dataset.shape)

print("dataset head")
print(dataset.head(15))

print("dataset descriptions")
print(dataset.describe())

print("dataset class distribution")
print(dataset.groupby('class').size())



'''
dataset['djnorm'] = dataset['dj'].apply(lambda val: round(val, 1))
#print(dataset['djnorm'])
dataset['dj'] = dataset['djnorm']
del dataset['djnorm']
dataset['ndnorm'] = dataset['nd'].apply(lambda val: round(val, 1))
#print(dataset['ndnorm'])
dataset['nd'] = dataset['ndnorm']
del dataset['ndnorm']
dataset['spnorm'] = dataset['sp'].apply(lambda val: round(val, 1))
#print(dataset['spnorm'])
dataset['sp'] = dataset['spnorm']
del dataset['spnorm']
print("dataset descriptions after normalization")
print(dataset.describe())
'''




if(DISPLAY_PLOTS):
	# box and whisker plots
	dataset.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
	plt.show()

	# histograms
	dataset.hist()
	plt.show()

	# scatter plot matrix
	scatter_matrix(dataset)
	plt.show()






# Split-out validation dataset
array = dataset.values
#print(array)
X = array[:,0:(len(dataset.columns) - 1)]#!!!!!define Label index here
#print(X)
Y = array[:,(len(dataset.columns) - 1)]#!!!!!define Label index here
#print(Y)
validation_size = 0.20
seed = 7
scoring = 'accuracy'
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)



# Spot Check Algorithms
models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))
# evaluate each model in turn
results = []
names = []
for name, model in models:
	kfold = model_selection.KFold(n_splits=10, random_state=seed)
	cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
	results.append(cv_results)
	names.append(name)
	msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
	print(msg)





# Make predictions on validation dataset - using LR
print("\nMake predictions using *LR* model\n")
lr = LogisticRegression()
lr.fit(X_train, Y_train)
predictions = lr.predict(X_validation)
print("Predictions")
print(predictions)
print("Accuracy : ", accuracy_score(Y_validation, predictions))
print("Confusion matrix")
print(confusion_matrix(Y_validation, predictions))
print("Classification report")
print(classification_report(Y_validation, predictions))


# Make predictions on validation dataset - using LDA
print("\nMake predictions using *LDA* model\n")
lda = LinearDiscriminantAnalysis()
lda.fit(X_train, Y_train)
predictions = lda.predict(X_validation)
print("Predictions")
print(predictions)
print("Accuracy : ", accuracy_score(Y_validation, predictions))
print("Confusion matrix")
print(confusion_matrix(Y_validation, predictions))
print("Classification report")
print(classification_report(Y_validation, predictions))


# Make predictions on validation dataset - using KNN
print("\nMake predictions using *KNN* model\n")
knn = KNeighborsClassifier()
knn.fit(X_train, Y_train)
predictions = knn.predict(X_validation)
print("Predictions")
print(predictions)
print("Accuracy : ", accuracy_score(Y_validation, predictions))
print("Confusion matrix")
print(confusion_matrix(Y_validation, predictions))
print("Classification report")
print(classification_report(Y_validation, predictions))


# Make predictions on validation dataset - using CART
print("\nMake predictions using *CART* model\n")
cart = DecisionTreeClassifier()
cart.fit(X_train, Y_train)
predictions = cart.predict(X_validation)
print("Predictions")
print(predictions)
print("Accuracy : ", accuracy_score(Y_validation, predictions))
print("Confusion matrix")
print(confusion_matrix(Y_validation, predictions))
print("Classification report")
print(classification_report(Y_validation, predictions))



# Make predictions on validation dataset - using NB
print("\nMake predictions using *NB* model\n")
nb = GaussianNB()
nb.fit(X_train, Y_train)
predictions = nb.predict(X_validation)
print("Predictions")
print(predictions)
print("Accuracy : ", accuracy_score(Y_validation, predictions))
print("Confusion matrix")
print(confusion_matrix(Y_validation, predictions))
print("Classification report")
print(classification_report(Y_validation, predictions))



# Make predictions on validation dataset - using SVM
print("\nMake predictions using *SVM* model\n")
svm = SVC()
svm.fit(X_train, Y_train)
predictions = svm.predict(X_validation)
print("Predictions")
print(predictions)
print("Accuracy : ", accuracy_score(Y_validation, predictions))
print("Confusion matrix")
print(confusion_matrix(Y_validation, predictions))
print("Classification report")
print(classification_report(Y_validation, predictions))


'''
print("*********************************************************************")
print("\nMy predictions")
custom_input = [[4.4, 2.1, 5.5, 1.8]]
predictions = knn.predict(custom_input)
print(predictions)
print(knn.predict_proba(custom_input))
'''


print("\n************************************************\nTest predictions on daily data\n************************************************\n")
CSV_FILE_PATH = utils.CSV_GENERATED_DATA_FOLDER + "/" + utils.DATA_RECORD_CSV_FILE
content = []
with open(CSV_FILE_PATH) as f:
	content = f.read().splitlines()

entryData = []
rowIndex = 0
for dataRecord in content:
	elemIndex = 0
	entryDataRow = []
	for element in dataRecord.split(","):
		print(element)
		entryDataRow.append(element)
	entryData.append(entryDataRow)

print(entryData)

for entryRecord in entryData:
	print("Data for experiment : ", entryRecord)
	print("My predictions")
	custom_input = [entryRecord[2:6]]
	print("Input : ", custom_input)
	print("Actual label : ", utils.getDecisionLabel(entryRecord[6]))
	entryRecord.append(utils.getDecisionLabel(entryRecord[6]))
	predictions = knn.predict(custom_input)
	print(predictions)
	print(knn.predict_proba(custom_input))
	entryRecord.append(predictions[0])
	entryRecord.append(str(knn.predict_proba(custom_input)[0][0]) + ";" + str(knn.predict_proba(custom_input)[0][1]))
	
print(entryData)

CSV_FILE_PATH = utils.CSV_GENERATED_DATA_FOLDER + "/" + "ml_daily_analysys_genrated.csv"
with open(CSV_FILE_PATH, 'a') as datafile:
	for dataToWrite in entryData:
		txtData = ""
		for idx, val in enumerate(dataToWrite):
			txtData += val
			if (idx < (len(dataToWrite) - 1)):
				 txtData += ","

		
		#If not beginning of the file, add new line cusrsor move
		if os.stat(CSV_FILE_PATH).st_size != 0:
			txtData = "\n" + txtData

		print("txtData", txtData)
		datafile.write(txtData)

		
		


