import nltk
import re
from nltk import Tree, PCFG, treetransforms, induce_pcfg, Nonterminal
from nltk.corpus import treebank
from nltk.parse import pchart, ViterbiParser

def make_PCFG_grammar():
    '''
    Forms a PCFG grammar utilizing the first 1963 files
    in the WSJ treebank
    '''
    # Save a list of all produced PCFG rules given the tested data
    PCFG_rules = []
    # We'll utilize the treebank that is already itemized into the NKTL toolkit as
    for item in treebank.fileids()[:1963]:
        # We want to first get rid of all non-binary branchings of the tree
        for tree in treebank.parsed_sents(item):
            tree.collapse_unary(collapsePOS = False)
            tree.chomsky_normal_form(horzMarkov = 2)
            PCFG_rules += tree.productions()

    # Induce the PCFG grammar
    S = Nonterminal('S')
    PCFG_grammar = induce_pcfg(S, PCFG_rules)

    return PCFG_grammar

def CKY_parser():
    '''
    Given the PCFG, we use the built in CKY praser function
    to get a sentence's most probable parse
    '''
    PCFG_grammar = make_PCFG_grammar()
    # Utilize the ViertabiParser given the PCFG grammar induction rules
    parser = ViterbiParser(PCFG_grammar)

    # Sample sentence parse
    sentences = treebank.parsed_sents('wsj_1964.mrg')

    skipped_sentences = 0

    # A for loop to print out the full parse
    for sentence in sentences:
        sentence = sentence.leaves()
        try:
            PCFG_grammar.check_coverage(sentence)
            for parse in parser.parse(sentence):
                print(parse)
        except:
            skipped_sentences += 1
            continue

    print("Total skipped sentences:", skipped_sentences)


def perplexity():
    '''
    Give the PCFG and the parser used, run the parser on
    the rest of the treebank and calculates the perplexity
    of the model given the testing sentences.
    '''

    PCFG_grammar = make_PCFG_grammar()
    parser = ViterbiParser(PCFG_grammar)
    all_p = []
    skipped_sentence = 0

    for item in treebank.fileids()[1964:]:
        trees = treebank.parsed_sents(item)
        for tree in trees:
            tree = tree.leaves()
            try:
                PCFG_grammar.check_coverage(tree)
                for parse in parser.parse(tree):
                    parse_string = str(parse)
                    p = re.search(r"p=([^/]+)", parse_string).group(1)
                    p = p[:-1]
                    all_p.append(float(p))
            except:
                skipped_sentence += 1
                continue

    perplexity = 1
    N = float(len(all_p))
    for p in all_p:
        perplexity = perplexity * (1/p)
    perplexity = pow(perplexity, 1/float(N))

    print("Perplexity:", perplexity)
    print("All parse probabilities:", all_p)
    print("Skipped sentences:", skipped_sentence)
    print("PCFG grammar:", PCFG_grammar)

perplexity()
