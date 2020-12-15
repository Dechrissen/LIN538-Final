import nltk
from nltk import trigrams
from collections import Counter, defaultdict
import random
from pathlib import Path
import os


# Path to wsj corpus
corpus_path = Path("C:/Users/Derek/Documents/wsj_corpus")

def trigram_model(corpus_path):
    """Builds a trigram model trained on a training corpus."""
    # Smoothing of 0.01 to handle unattested words in test data
    model = defaultdict(lambda: defaultdict(lambda: 0.01))
    # Training set of 80% of the Wall Street Journal corpus (first 1963 files)
    for file in os.listdir(corpus_path)[:1964]:
        with open(corpus_path / file, 'r') as current:
            sents = current.readlines()
            for sentence in sents:
                if ('.START' in sentence) or (sentence == '\n'):
                    continue
                else:
                    sentence = sentence.split()
                for w1, w2, w3 in trigrams(sentence, pad_right=True, pad_left=True):
                    model[(w1, w2)][w3] += 1

    # Transform the counts into probabilities
    for w1_w2 in model:
        total_count = float(sum(model[w1_w2].values()))
        for w3 in model[w1_w2]:
            model[w1_w2][w3] /= total_count

    return model

def generate_sentence(model):
    """Generates a sentence according to a trigram model."""
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

def perplexity(test_sent, model):
    """Computes the perplexity of a trigram model on a test sentence."""
    test_sent = test_sent.split()
    perplexity = 1
    N = 0
    for w1, w2, w3 in trigrams(test_sent, pad_right=True, pad_left=True):
        N += 1
        perplexity = perplexity * (1/model[(w1, w2)][w3])
    perplexity = pow(perplexity, 1/float(N))
    return perplexity

# Create a trigram model according to wsj corpus
model = trigram_model(corpus_path)

# Print the probability of sentences that start with 'The'
print(model[None, None]["The"])



# Construct a test set of 20% of the Wall Street Journal corpus (files 1964 - 2454)
testset = []
for file in os.listdir(corpus_path)[1964:2455]:
    with open(corpus_path / file, 'r') as current:
        sents = current.readlines()
        for sentence in sents:
            if ('.START' in sentence) or (sentence == '\n'):
                continue
            else:
                testset.append(sentence)




# Calculate the perplexity of the model with the entire test set
PP = 0
perplexities = []
i = 0
for sentence in testset:
    # handle inf cases
    try:
        p = int(perplexity(sentence, model))
    except OverflowError:
        continue
    i += 1
    PP += p
# average of perplexities
PP = PP / i


generate_sentence(model)
print('Model perplexity on test set:', PP)
