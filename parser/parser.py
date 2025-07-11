import nltk
import sys
from nltk.tokenize import word_tokenize

nltk.data.path.append('./nltk_data')  # <--- ADD THIS LINE

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
    S -> NP VP | S Conj S | S Conj VP 

    Prem -> Det | Det Adj | Det Adj Adj | Det Adj Adj Adj | Adj | Adj Adj | Adj Adj Adj 
    Postm -> P NP
    NP -> Prem N | N | N Postm | Prem N Postm
    VP -> V | V NP | VP Adv | Adv VP | V VP | V Postm  
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
    word_list = word_tokenize(sentence.lower())
    for word in word_list:
        if not word.islower():
            word_list.remove(word)

    return word_list

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    trees = []
    for a in tree.subtrees():
        if a.label() == "NP":
            counter = 0
            for b in a.subtrees():
                if b.label() == "NP":
                    counter += 1
            if counter == 1:
                trees.append(a)


    return trees


if __name__ == "__main__":
    main()