# Write your code here

import xml.etree.ElementTree as ET
import string
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

file = open('news.xml')
xml_file = ET.parse(file)
root = xml_file.getroot()
lemmatizer = WordNetLemmatizer()
vectorizer = TfidfVectorizer()

header_list = []
texts_list = []
cleaned_texts = []
string_list = []

stop_words = list(stopwords.words('english'))
punctuation_stop = list(string.punctuation)

corpus = root.find('corpus')

for i in range(0, len(corpus)):
    header = corpus[i][0].text
    text = corpus[i][1].text
    header_list.append(header)
    texts_list.append(text)
    i += 1


def texts_cleaning(text_list):
    lemmed_word = []
    cleaned_words = []
    word_list = word_tokenize(text.lower())
    for word in word_list:
        lemmed_word.append(lemmatizer.lemmatize(word, pos='n'))
    for word in lemmed_word:
        if (nltk.pos_tag([word])[0][1] == "NN") & (word not in stop_words) & (word not in punctuation_stop):
            cleaned_words.append(word)
    return cleaned_words


for text in texts_list:
    cleaned_texts.append(texts_cleaning(text))

for i in range(0, len(cleaned_texts)):
    new_string = ', '.join(cleaned_texts[i])
    string_list.append(new_string)

tfidf_matrix = vectorizer.fit_transform(string_list)
terms = vectorizer.get_feature_names()

for i in range(len(header_list)):
    list_of_words = []
    print(header_list[i]+':')
    df = pd.DataFrame(tfidf_matrix[i].toarray())
    df2 = df.transpose().reset_index()
    for l in range(0, len(df2)):
        k = terms[df2['index'][l]]
        list_of_words.append(k)
    df2['words'] = list_of_words
    df2 = df2.sort_values(by=[0, 'words'], ascending=[False, False])
    string_to_print = ''
    for n in range(0, 5):
       part = df2.iloc[n]['words']
       string_to_print += part + ' '
    print(string_to_print + '\n')








