import re
# import pandas as pd
# import string
# import emoji
# import contractions
# from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
# from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text  import  CountVectorizer 

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.model_selection import  train_test_split
from sklearn.metrics import accuracy_score
import pickle
from sklearn.metrics import accuracy_score


factory = StemmerFactory()
stemmer = factory.create_stemmer()

f = open("app/controllers/stopword_list_tala.txt", "r")
isi = f.read()

tempStoplist = []
for tempstp in isi.split():
  tempStoplist.append(tempstp.lower())

cleantext = "(@[A-Za-z0-9_-]+)|([^A-Za-z \t\n])|(\w+:\/\/\S+)|(x[A-Za-z0-9]+)|(X[A-Za-z0-9]+)" #regex untuk remove punctuation
# Preprocessing
def preprocess_data(text):
  text = text.rstrip("\n")
  text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
  text = re.sub('RT\s', '', text)
  text = re.sub('#+', '', text)
  # text = re.sub('emoji.demojize', text)

  text = re.sub(cleantext,' ',str(text).lower()).strip() #casefolding dan remove punctuation
  # text = re.sub(r'[0-9]+', '', text, flags=re.MULTILINE)
  tokens = []
  for token in text.split():
    #if token in templist:
    if token not in tempStoplist: #jika token tidak di stopword maka simpan
      token = stemmer.stem(token) #lakukan stemming
      if len(token) >= 2:
      #if token != 'b':
        if token != 'rt':
          tokens.append(token) 
          text = " ".join(tokens)
  return text
  

# NB
def result_nb(text):
  
    # Mengambil data teks dan label
  text['label'] = text['label'].map({'positif': 2, 'negatif': 1, 'netral': 0})
  X = text['Tweet'].fillna(' ')
  y = text['label']


  # Membagi data menjadi data latih dan data uji
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=123)

  # Membuat vektor fitur dengan CountVectorizer
  vectorizer = CountVectorizer()
  X_train_counts = vectorizer.fit_transform(X_train)
  pickle.dump(vectorizer, open('app/uploads/vector1.pkl', 'wb'))

  # Melakukan transformasi TF-IDF pada vektor fitur
  tfidf_transformer = TfidfTransformer()
  X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

  # Melatih model Naive Bayes Multinomial
  model = MultinomialNB()
  model.fit(X_train_tfidf, y_train)

  pickle.dump(model, open('app/uploads/sentiment1.pkl', 'wb'))

  # Menerapkan vektorisasi dan transformasi TF-IDF pada data uji
  X_test_counts = vectorizer.transform(X_test)
  X_test_tfidf = tfidf_transformer.transform(X_test_counts)

  # Melakukan prediksi pada data uji
  y_pred = model.predict(X_test_tfidf)

  # Menghitung akurasi
  accuracy = accuracy_score(y_test, y_pred)
  # print("Akurasi:", accuracy)

  return accuracy, y_test
