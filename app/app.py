from flask import Flask, render_template, url_for, request, redirect
import pandas as pd
import pickle
import numpy as np
from sklearn.externals import joblib
import scraper
import train

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/update')
def update():
	return render_template('loading.html')

@app.route('/summary')
def validate():
	scraper.check()

	df = train.clean()
	accuracy = train.trainNewData(df)

	return render_template('summary.html', len = len(df['description']), values = df.label.value_counts(), accuracy = accuracy)


@app.route('/results', methods=['POST'])
def predict():

	if request.method == 'POST':

		svm_model = open("models/svm_model.pkl","rb")
		svm_clf = pickle.load(svm_model)

		logreg_model = open("models/logreg_model.pkl","rb")
		logreg_clf = pickle.load(logreg_model)

		data = request.form['comment']

		data = [train.cleanString(data)]

		print(data)

		svm_prediction = svm_clf.predict(data)
		logreg_prediction = logreg_clf.predict(data)
		top_predictions = logreg_clf.predict_proba(data)
		top_predictions_list = top_predictions[0,:].tolist()

		names = ["CloudFront", "EC2", "Elastic Beanstalk", "Lambda", "RDS", "S3", "SNS", "VPC"]

		df = pd.Series(top_predictions_list, index = names)

		df = df.sort_values(ascending = False)
		df = df.apply(lambda x: 100*x)
		print(df.index[:5])

		return render_template('result.html', svm_prediction = svm_prediction, logreg_prediction = logreg_prediction, top_predictions = df[:5], data = data)

if __name__ == '__main__':
	app.run(debug = True)
