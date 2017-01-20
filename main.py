from __future__ import division
import nltk, re, pprint
from nltk import word_tokenize
from nltk.collocations import *
from bottle import route, run, template
from bottle import static_file
import json
import urllib2

swears = ['fuck', 'fucking', 'motherfucker', 'motherfucking', 'shit', 'niggas', 'nigga', 'motherfuckers']

def unusual(text):
  text_vocab = set(w.lower() for w in text if w.isalpha())
  english_vocab = set(w.lower() for w in nltk.corpus.words.words())
  unusual = text_vocab.difference(english_vocab)
  return unusual

def loadwordlist(filename):
	raw = open(filename).read()
	tokens = word_tokenize(raw)
	wordlist = [w.lower() for w in tokens]
	return wordlist

def findkeywords(wordlist):
	vocabulary = sorted(set(wordlist))
	keywords = unusual(vocabulary)
	return set(keywords) - set(swears)

def findbigrams(wordlist):
	trigram_measures = nltk.collocations.TrigramAssocMeasures()
	finder = BigramCollocationFinder.from_words(wordlist)
	bigrams = finder.nbest(trigram_measures.pmi, 30)
	return bigrams

@route('/')
def root():
    return '''
    <h1>Speech-Influenced Playlists, hon</h1>
    <table>
    	<tr>
    		<td><a href="/playlists/kanye.txt"><img src="images/kanye.jpg" style="width:250px;height:250px;"></a></td>
    		<td><a href="/playlists/obama.txt"><img src="images/obama.jpg" style="width:250px;height:250px;"></a></td>
    		<td><a href="/playlists/trump.txt"><img src="images/trump.jpg" style="width:250px;height:250px;"></a></td>
    		<td><a href="/playlists/iggy.txt"><img src="images/iggy.jpg" style="width:250px;height:250px;"></a></td>
    	</tr>
    	<tr>
    		<td><a href="/texts/kanye.txt">Text</a>&nbsp;|&nbsp;<a href="/keywords/kanye.txt">Keywords</a>&nbsp;|&nbsp;<a href="/bigrams/kanye.txt">Bigrams</a></td>
    		<td><a href="/texts/obama.txt">Text</a>&nbsp;|&nbsp;<a href="/keywords/obama.txt">Keywords</a>&nbsp;|&nbsp;<a href="/bigrams/obama.txt">Bigrams</a></td>
    		<td><a href="/texts/trump.txt">Text</a>&nbsp;|&nbsp;<a href="/keywords/trump.txt">Keywords</a>&nbsp;|&nbsp;<a href="/bigrams/trump.txt">Bigrams</a></td>
    		<td><a href="/texts/iggy.txt">Text</a>&nbsp;|&nbsp;<a href="/keywords/iggy.txt">Keywords</a>&nbsp;|&nbsp;<a href="/bigrams/iggy.txt">Bigrams</a></td>
    	</tr>
    </table>
    '''

@route('/keywords/<name>')
def index(name):
  wordlist = loadwordlist('/Users/beth/Projects/siphon/text/' + name)
  keywords = findkeywords(wordlist)
  bigrams = findbigrams(wordlist)
  response = ", ".join(keywords)

  return template('<p>{{response}}</p>', response=response)


@route('/bigrams/<name>')
def index(name):
  wordlist = loadwordlist('/Users/beth/Projects/siphon/text/' + name)
  bigrams = findbigrams(wordlist)
  response = ""

  for bigram in bigrams:
  	response = response + "[" + " ".join(bigram) + "]"

  return template('<p>{{response}}</p>', response=response)

@route('/playlists/<filename>')
def index(filename):
	playlist = open('/Users/beth/Projects/siphon/playlists/' + filename).read()
	return playlist

@route('/images/<filename>')
def server_static(filename):
    return static_file(filename, root='/Users/beth/Projects/siphon/images')

@route('/texts/<filename>')
def server_static(filename):
    return static_file(filename, root='/Users/beth/Projects/siphon/text')

run(host='localhost', port=1337)
