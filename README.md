# Speech-Influenced Playlists, hon

Siphon is an experiment to analyse text using the Python Natural Language Toolkit looking for bigrams and uncommon words. These words and bigrams are used to find tracks played on the BBC and create a playlist.

![Siphon](https://github.com/betandr/siphon/blob/master/images/siphon.png)

## Running

Run:

`python main.py`

Then visit:

`http://localhost:1337`

## Routes

```
http://localhost:1337/ - Root
http://localhost:1337/keywords/{person}.txt - Keywords for person's speech (Zipf-Mandelbrot Power)
http://localhost:1337/bigrams/{person}.txt - Bigrams for person's speech
http://localhost:1337/playlists/{person}.txt - The playlist for that person's speech
```

## Approach

### Keywords

Siphon uses the Python Natural Language Toolkit (NLTK) to analyse the text, firstly finding keywords by using a sort of Zipf-Mandelbrot Power curve to find uncommon words. This is done by finding the vocablary of the text then comparing it against the `nltk.corpus.words` wordlist. This finds uncommon words in the person's speech; which I'm assuming are the 'interesting' bits like bands or slang words.

```python
def unusual(text):
  text_vocab = set(w.lower() for w in text if w.isalpha())
  english_vocab = set(w.lower() for w in nltk.corpus.words.words())
  unusual = text_vocab.difference(english_vocab)
  return unusual
```

### Bigrams

Siphon also finds Bigrams (a pair of consecutive words) which could be a person's name, so we're using this to find artists.

## TODO

Live requests were problematic during the hack day so for expediency I did them offline using Curl. I'll fix this.

Also I'm going to turn this into a service. :)