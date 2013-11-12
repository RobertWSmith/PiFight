from nltk.corpus import wordnet

"""
See NLTK Book page 42

example use case:

from TextSimplifier import AntonymReplacer
replacer = AntonymReplacer()
replacer.replace('good')
replacer.replace('uglify')
sent = ["let's", "not", "uglify", "our", "code"]
replacer.replaceNegations(sent)
"""

class AntonymReplacer(object):
    def replace(self, word, pos = None):
        antonyms = set()
        for syn in wordnet.synsets(word, pos = pos):
            for lemma in syn.lemmas:
                for antonym in lemma.antonyms():
                    antonyms.add(antonym.name)
        if len(antonyms) == 1:
            return antonyms.pop()
        else:
            return None

    def replaceNegations(self, sent):
        i , l = 0, len(sent)
        words = []
        while i < l:
            word = sent[i]
            if word == 'not' and i+1 < l:
                ant = self.replace(sent[i+1])
                if ant:
                    words.append(ant)
                    i += 2
                    continue
            words.append(word)
            i += 1
        return words

"""
See NLTK book Ch. 2

Repeat Replacer use cases

from TextSimplifier import RepeatReplacer
replacer = RepeatReplacer()
replacer.replace('looooooooove')
replacer.replace('ooooooooooh')
replacer.replace('goose')

"""
import re

class RepeatReplacer(object):
    def __init__(self):
        self.repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
        self.repl = r'\1\2\3'

    def replace(self, word):
        repl_word = self.repeat_regexp.sub(self.repl, word)
        if repl_word != word:
            return self.replace(repl_word)
        else:
            return repl_word

from nltk.stem import PorterStemmer

class SynonymReplacer(object):
    

