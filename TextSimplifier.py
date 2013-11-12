import re
import enchant
import csv
from nltk.corpus import wordnet
from nltk.metrics import edit_distance

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

class RepeatReplacer(object):
    def __init__(self):
        self.repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
        self.repl = r'\1\2\3'

    def replace(self, word):
        if wordnet.synsets(word): 
            return word
        repl_word = self.repeat_regexp.sub(self.repl, word)
        if repl_word != word:
            return self.replace(repl_word)
        else:
            return repl_word

"""
See NLTK book Ch.2 p.36

Spell Check / replacer -- utilizes 'enchant' spelling dictionary

from TextSimplifier import SpellingReplacer
replacer = SpellingReplacer()
replacer.replace('cookbok')

"""

class SpellingReplacer(object):
    def __init__(self, dict_name = 'en', max_distance = 2):
        self.spell_dict = enchant.Dict(dict_name)
        self.max_dist = max_distance
    def replace(self, word):
        if self.spell_dict.check(word):
            return word
        suggestions = self.spell_dict.suggest(word)
        if suggestions and edit_distance(word, suggestions[0]) <= self.max_dist:
            return suggestions[0]
        else:
            return word


"""
See NLTK book Ch.2 p.39

Synonym Replacer -- helps reduce overall vocabulary

from TextSimplifier import SynonymReplacer
replacer = SynonymReplacer({'bday', 'birthday'})
replacer.replace('bday')
replacer.replace('happy')

"""

class SynonymReplacer(object):
    def __init__(self, word_map):
        self.word_map = word_map
    def replace(self, word):
        return self.word_map.get(word, word)
    

