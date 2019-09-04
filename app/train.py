import pandas as pd
import csv
import string
import re
import nltk
import pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

nltk.download('stopwords')
nltk.download('names')
from nltk.corpus import stopwords
from nltk.corpus import names
from nltk import word_tokenize

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix


def clean():

    df = pd.read_csv("input/newdata.csv")

    STOPWORDS = stopwords.words('english')
    my_stop_words = ["hi", "hello", "regards", "thank", "thanks", "regard", "best", "wishes", "hey", "amazon", "aws", "s3",
    "elastic", "beanstalk", "rds", "ec2", "lambda", "cloudfront", "cloud", "front", "vpc", "sns", "me",
    "january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
    "november", "december", "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "sept", "oct", "nov",
    "dec", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "mon", "tue",
    "wed", "thu", "fri", "sat", "sun", "ain't", "aren't", "can't", "can't've", "'cause", "could've", "couldn't",
    "couldn't've", "didn't", "doesn't", "don't", "hadn't", "hadn't've", "hasn't", "haven't", "he'd", "he'd've",
    "he'll", "he'll've", "he's", "how'd", "how'd'y", "how'll", "how's", "i'd", "i'd've", "i'll", "i'll've", "i'm",
    "i've", "isn't", "it'd", "it'd've", "it'll", "it'll've", "it's", "let's", "mayn't", "might've", "mightn't",
    "mightn't've", "must've", "mustn't", "mustn't've", "needn't", "needn't've", "oughtn't", "oughtn't've", "shan't",
    "sha'n't", "shan't've", "she'd", "she'd've", "she'll", "she'll've", "she's", "should've", "shouldn't", "shouldn't've",
    "so've", "so's", "that'd", "that'd've", "that's", "there'd", "there'd've", "there's", "they'd", "they'd've", "they'll",
    "they'll've", "they're", "they've", "to've", "wasn't", "we'd", "we'd've", "we'll", "we'll've", "we're", "we've",
    "weren't", "what'll", "what'll've", "what're", "what's", "what've", "when's", "when've", "where'd", "where's",
    "where've", "who'll", "who'll've", "who's", "who've", "why's", "why've", "will've", "won't", "won't've", "would've",
    "wouldn't", "wouldn't've", "yall", "yalld", "yalldve", "yallre", "yallve", "youd", "youdve", "youll",
    "youllve", "youre", "youve", "do", "did", "does", "had", "have", "has", "could", "can", "as", "is",
    "shall", "should", "would", "will", "you", "me", "please", "know", "who", "we", "was", "were", "edited", "by", "pm"]

    name = names.words()
    STOPWORDS.extend(my_stop_words)
    STOPWORDS.extend(name)

    REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,:;#+?]')
    BAD_SYMBOLS_RE = re.compile('[^0-9a-z - _.]+')
    REMOVE_HTML_RE = re.compile(r'<.*?>')

    STOPWORDS = [BAD_SYMBOLS_RE.sub('', x) for x in STOPWORDS]

    df['description'] = df['description'].apply(lambda x: " ".join(x.lower() for x in str(x).split(" "))) # convert to lowercase
    df['description'] = df['description'].apply(lambda x: " ".join(REMOVE_HTML_RE.sub(' ', x) for x in str(x).split())) # remove html tags
    df['description'] = df['description'].apply(lambda x: " ".join(x.strip('(') for x in str(x).split())) # remove open brackets
    df['description'] = df['description'].apply(lambda x: " ".join(x.strip(')') for x in str(x).split())) # remove closed brackets
    df['description'] = df['description'].apply(lambda x: " ".join(x if (x.startswith("http://") or x.startswith("https://")) else REPLACE_BY_SPACE_RE.sub(' ', x) for x in str(x).split()))
    # replace certain characters by space
    df['description'] = df['description'].apply(lambda x: " ".join(x if (x.startswith("http://") or x.startswith("https://")) else BAD_SYMBOLS_RE.sub('', x) for x in str(x).split()))
    # remove special characters
    df['description'] = df['description'].apply(lambda x: " ".join(x.strip('.') for x in str(x).split())) # remove any patterns
    df['description'] = df['description'].apply(lambda x: " ".join(x.strip('-') for x in str(x).split()))
    df['description'] = df['description'].apply(lambda x: " ".join(x.strip('_') for x in str(x).split()))
    df['description'] = df['description'].apply(lambda x: " ".join(x for x in str(x).split() if not x.isdigit())) # remove numbers
    df['description'] = df['description'].apply(lambda x: " ".join(x for x in str(x).split() if x not in STOPWORDS and len(x) > 1)) # remove stop words

    # print(df['description'].head(10))

    with open('input/clean.csv', 'w', encoding='utf-8', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter=',')

        for i in range(0, len(df['description'])):
            if len(df['description'][i]) > 0:
                writer.writerow([df['id'], df['label'], df['description'][i]])

    '''open('input/cleanv8.csv', 'a', encoding='utf-8', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter=',')

        for i in range(0, len(df['description'])):
            if len(df['description'][i]) > 0:
                writer.writerow([df['id'], df['label'], df['description'][i]])
    '''
    return df

def trainNewData(df):
    print("Validating accuracy of model...")
    X_test = df['description'].values
    y_test = df['label'].values

    svm_model = open("models/svm_model.pkl","rb")
    svm_clf = pickle.load(svm_model)

    y_predict_svm = svm_clf.predict(X_test)

    print(classification_report(y_test, y_predict_svm))
    print('svm accuracy:', accuracy_score(y_predict_svm, y_test))

    array = confusion_matrix(y_test, y_predict_svm)
    names = ["Cloudfront", "EC2", "Elastic Beanstalk", "Lambda", "RDS", "S3", "SNS", "VPC"]

    df_cm = pd.DataFrame(array, index = [i for i in names], columns = [i for i in names])

    plt.figure(figsize = (10,7))
    sns_plot = sns.heatmap(df_cm, annot=True, cmap="Blues")
    sns_plot.figure.savefig("static/res/svm_confusion.png")

    logreg_model = open("models/warm_logreg_model.pkl","rb")
    logreg_clf = pickle.load(logreg_model)

    y_predict_logreg = logreg_clf.predict(X_test)

    print(classification_report(y_test, y_predict_logreg))
    print('logistic regression accuracy:', accuracy_score(y_predict_logreg, y_test))

    array = confusion_matrix(y_test, y_predict_logreg)
    names = ["Cloudfront", "EC2", "Elastic Beanstalk", "Lambda", "RDS", "S3", "SNS", "VPC"]

    df_cm = pd.DataFrame(array, index = [i for i in names], columns = [i for i in names])

    plt.figure(figsize = (10,7))
    sns_plot = sns.heatmap(df_cm, annot=True, cmap="Blues")
    sns_plot.figure.savefig("static/res/logreg_confusion.png")

    print("Started training the data!")

    #df1 = pd.read_csv("input/cleanv8.csv")

    # X = v.fit_transform(df['description'].apply(lambda x: np.str_(x)))

    # X = df1['description']
    #y = df1['label']

    #logreg = Pipeline([('vect', TfidfVectorizer()), ('clf', LogisticRegression(warm_start = True, max_iter = 10000, n_jobs = 1, solver = "lbfgs", multi_class="multinomial"))])
    #logreg.fit(X, y)


    with open('input/clean.csv', 'w', encoding='utf-8', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter=',')

    return [accuracy_score(y_predict_svm, y_test), accuracy_score(y_predict_logreg, y_test)]


def cleanString(text):

    STOPWORDS = stopwords.words('english')
    my_stop_words = ["hi", "hello", "regards", "thank", "thanks", "regard", "best", "wishes", "hey", "amazon", "aws", "s3",
    "elastic", "beanstalk", "rds", "ec2", "lambda", "cloudfront", "cloud", "front", "vpc", "sns", "me",
    "january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
    "november", "december", "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "sept", "oct", "nov",
    "dec", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "mon", "tue",
    "wed", "thu", "fri", "sat", "sun", "ain't", "aren't", "can't", "can't've", "'cause", "could've", "couldn't",
    "couldn't've", "didn't", "doesn't", "don't", "hadn't", "hadn't've", "hasn't", "haven't", "he'd", "he'd've",
    "he'll", "he'll've", "he's", "how'd", "how'd'y", "how'll", "how's", "i'd", "i'd've", "i'll", "i'll've", "i'm",
    "i've", "isn't", "it'd", "it'd've", "it'll", "it'll've", "it's", "let's", "mayn't", "might've", "mightn't",
    "mightn't've", "must've", "mustn't", "mustn't've", "needn't", "needn't've", "oughtn't", "oughtn't've", "shan't",
    "sha'n't", "shan't've", "she'd", "she'd've", "she'll", "she'll've", "she's", "should've", "shouldn't", "shouldn't've",
    "so've", "so's", "that'd", "that'd've", "that's", "there'd", "there'd've", "there's", "they'd", "they'd've", "they'll",
    "they'll've", "they're", "they've", "to've", "wasn't", "we'd", "we'd've", "we'll", "we'll've", "we're", "we've",
    "weren't", "what'll", "what'll've", "what're", "what's", "what've", "when's", "when've", "where'd", "where's",
    "where've", "who'll", "who'll've", "who's", "who've", "why's", "why've", "will've", "won't", "won't've", "would've",
    "wouldn't", "wouldn't've", "yall", "yalld", "yalldve", "yallre", "yallve", "youd", "youdve", "youll",
    "youllve", "youre", "youve", "do", "did", "does", "had", "have", "has", "could", "can", "as", "is",
    "shall", "should", "would", "will", "you", "me", "please", "know", "who", "we", "was", "were", "edited", "by", "pm"]

    name = names.words()
    STOPWORDS.extend(my_stop_words)
    STOPWORDS.extend(name)

    REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,:;#+?]')
    BAD_SYMBOLS_RE = re.compile('[^0-9a-z - _.]+')
    REMOVE_HTML_RE = re.compile(r'<.*?>')

    STOPWORDS = [BAD_SYMBOLS_RE.sub('', x) for x in STOPWORDS]

    words = text.split(" ")
    newtext = "";

    for w in words:
        w = w.lower()
        w = REMOVE_HTML_RE.sub(' ', w)
        w = w.strip('(')
        w = w.strip(')')

        if w.startswith("http://") or w.startswith("https://"):
            w = w
        else:
            w = REPLACE_BY_SPACE_RE.sub(' ', w)

        if w.startswith("http://") or w.startswith("https://"):
            w = w
        else:
            w = BAD_SYMBOLS_RE.sub(' ', w)

        w = w.strip('.')
        w = w.strip('-')
        w = w.strip('_')

        if w.isdigit():
            w = ""

        if w in STOPWORDS:
            w = ""

        if len(w) <= 1:
            w = ""

        newtext = newtext + " " + w

    return newtext
