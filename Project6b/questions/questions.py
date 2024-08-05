import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    fl_colln=dict()
    location=os.path.join(".",f"{str(directory)}")
    word_files=os.listdir(location)
    for val in word_files:
        val_path=os.path.join(location,val)
        with open(val_path,"r",encoding="utf8") as f:
            item=f.read()
        fl_colln[val]=item
    return fl_colln



def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words=list()
    order_words=list()
    document=document.lower()
    words=nltk.word_tokenize(document)
    punctuation=string.punctuation
    mainwords=set(nltk.corpus.stopwords.words("english"))
    for wrd in words:
        if wrd not in punctuation and wrd not in mainwords:
            order_words.append(wrd)
    return order_words 


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    wrd_presence=set()
    wrd_idfs=dict()
    total=0
    for document in documents:
        wrd_presence.update(set(documents[document]))
    
    for wrd in wrd_presence:
        total=sum(wrd in documents[document] for document in documents)
        wrd_idfs[wrd]=math.log(len(documents)/total)
    return wrd_idfs



def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    filenames=list()
    tfidfvalues=dict()
    for file in files:
        tfidfvalues[file]=0
        wrd_idf=0
        term_freq=0
        for wrd in query:
            if wrd in files[file]:
                term_freq=files[file].count(wrd)+1
            if wrd in idfs.keys():
                wrd_idf=idfs[wrd]
            tfidfvalues[file]+=wrd_idf*term_freq
    filenames=sorted(tfidfvalues,key=tfidfvalues.get,reverse=True)
    return filenames[:n]




def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    imp_sentences=list()
    detail_sentence=dict()
    for sentence in sentences:
        detail_sentence[sentence]={}
        detail_sentence[sentence]['idf']=0
        detail_sentence[sentence]['query_term_density']=0.0
        detail_sentence[sentence]['query_term_frequency']=0
        for wrd in query:
            if wrd in sentences[sentence]:
                detail_sentence[sentence]['query_term_frequency']+=1
                detail_sentence[sentence]['idf']+=idfs[wrd]
        detail_sentence[sentence]['query_term_density']=float(detail_sentence[sentence]['query_term_frequency']/len(sentences[sentence]))
    imp_sentences=sorted(detail_sentence,key=lambda sentence: (detail_sentence[sentence]['idf'],detail_sentence[sentence]['query_term_density']))
    imp_sentences.reverse()
    return imp_sentences[:n]



if __name__ == "__main__":
    main()
