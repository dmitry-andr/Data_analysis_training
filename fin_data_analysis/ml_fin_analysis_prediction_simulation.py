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
# reshape as has only 1 entry
predictions = knn.predict(custom_input)
print(predictions)
print(knn.predict_proba(custom_input))
'''





