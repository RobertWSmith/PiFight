from nltk.corpus import wordnet

"""
See NLTK Book page 42
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
example use case:

from TextSimplifier import AntonymReplacer
replacer = AntonymReplacer()
replacer.replace('good')
replacer.replace('uglify')
sent = ["let's", "not", "uglify", "our", "code"]
replacer.replace_negations(sent)
"""