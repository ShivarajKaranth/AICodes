import nltk
import sys


TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP NP | NP VP NP VP | NP VP NP PP | NP VP NP VP NP | NP VP | VP Conj NP | NP VP PP VP NP
NP -> N | Det N | Adj NP | NP Conj NP | Det Adj NP | N Adj | Conj N | Det N Adv | N Adv | N AdvP Conj | N PP | NP NP
VP -> V | V PP | Det VP | VP Conj VP | AdvP V | Conj V
PP -> P | P NP | N PP NP | P Det Adj
AdvP -> V Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    sentence=sentence.lower()
    wrd_list=list()
    wrd_list=nltk.word_tokenize(sentence)
    for wrd in wrd_list:
        if wrd.isalpha()==False:
            for tkn in range(len(wrd)):
                if wrd[tkn].isalpha()==True:
                    break
            wrd_list.remove(wrd[tkn])
    return wrd_list



def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_list=list()
    for branch in tree.subtrees(filter=lambda t: t.label()=='NP'):
        valid=True
        for branch1 in branch.subtrees(filter=lambda t: t.label()=='NP'):
            if branch!=branch1:
                valid=False
        if valid:
            np_list.append(branch)
    return np_list 


if __name__ == "__main__":
    main()
