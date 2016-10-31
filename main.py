from flask import Flask, current_app, render_template
from flask import request
import sys
import nltk
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk import tokenize

app = Flask(__name__)


def _calculate_languages_ratios(text):
    languages_ratios = {}
    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]

    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)

        languages_ratios[language] = len(common_elements)

    return languages_ratios


@app.route('/')
def index():
    return current_app.send_static_file('index.html')


def language_detection(text):
    ratios = _calculate_languages_ratios(text)

    most_rated_language = max(ratios, key=ratios.get)

    return most_rated_language


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    if text=="":
        return render_template('lang.html',name="no text entered")
    elif len(tokenize.word_tokenize(text))<=5:
        return render_template("lang.html",name="Minimum 6 words required to identify the language")
    else:
        data = language_detection(text)
        return render_template('lang.html',name=data)


if __name__ == "__main__":
    app.run(debug=True)
