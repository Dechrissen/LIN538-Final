import nltk
from nltk.corpus import reuters
from nltk import bigrams, trigrams
from collections import Counter, defaultdict
import random
from pathlib import Path
import os

#nltk.download('reuters')

#first_sentence = reuters.sents()[0]
#print(first_sentence)

# Get the trigrams
#print(list(trigrams(first_sentence)))

# Get the padded trigrams
#print(list(trigrams(first_sentence, pad_left=True, pad_right=True)))

model = defaultdict(lambda: defaultdict(lambda: 0))

#for sentence in reuters.sents():
    #for w1, w2, w3 in trigrams(sentence, pad_right=True, pad_left=True):
        #model[(w1, w2)][w3] += 1
wsj = Path("C:/Users/Derek/Documents/wsj_corpus")

for file in os.listdir(wsj):
    with open(wsj / file, 'r') as current:
        sents = current.readlines()
        for sentence in sents:
            if ('.START' in sentence) or (sentence[0] == ''):
                continue
            else:
                sentence = sentence.split()
            for w1, w2, w3 in trigrams(sentence, pad_right=True, pad_left=True):
                model[(w1, w2)][w3] += 1




#print(model["what", "the"]["economists"]) # "economists" follows "what the" 2 times
#print(model["what", "the"]["nonexistingword"]) # 0 times
#print(model[None, None]["The"]) # 8839 sentences start with "The"

# Let's transform the counts to probabilities
for w1_w2 in model:
    total_count = float(sum(model[w1_w2].values()))
    for w3 in model[w1_w2]:
        model[w1_w2][w3] /= total_count

#print(model["what", "the"]["economists"]) # 0.0434782608696
#print(model["what", "the"]["nonexistingword"]) # 0.0
#print(model[None, None]["The"]) # 0.161543241465


text = [None, None]

sentence_finished = False

while not sentence_finished:
    r = random.random()
    accumulator = .0

    for word in model[tuple(text[-2:])].keys():
        accumulator += model[tuple(text[-2:])][word]

        if accumulator >= r:
            text.append(word)
            break

    if text[-2:] == [None, None]:
        sentence_finished = True

print(' '.join([t for t in text if t]))
