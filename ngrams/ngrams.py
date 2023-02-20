from nltk import ngrams
from nltk import word_tokenize
import pickle
from pprint import pprint

# Build separate language models for 3 languages as follows.
# a. create a function with a filename as argument
def build_language_model(filename):
    # b. read in the text and remove newlines
    with open(filename, 'r') as file:
        text = file.read().replace('\n', ' ')

    # c. tokenize the text
    tokens = word_tokenize(text)

    # d. use nltk to create a bigrams list
    bigrams = list(ngrams(tokens, 2))

    # e. use nltk to create a unigrams list
    unigrams = list(ngrams(tokens, 1))
    print(unigrams[0][0])

    # f. use the bigram list to create a bigram dictionary of bigrams and counts, [‘token1 token2’] -> count
    bigram_dict = {b:bigrams.count(b) for b in set(bigrams)}

    #pprint(bigram_dict)
    # g. use the unigram list to create a unigram dictionary of unigrams and counts, [‘token’] -> count
    unigram_dict = {t:unigrams.count(t) for t in set(unigrams)}

    #pprint(unigram_dict)
    # h. return the unigram dictionary and bigram dictionary from the function
    return unigram_dict, bigram_dict


# i. in the main body of code, call the function 3 times for each training file, pickle the 6
# dictionaries, and save to files with appropriate names.

# create english unigrams and bigrams, pickle and save to file
english_unigram, english_bigram = build_language_model('LangId.train.English')
with open('english_unigram.pickle', 'wb') as file:
    pickle.dump(english_unigram, file)
with open('english_unigram.txt', 'w') as file:
    file.write(str(english_unigram))

with open('english_bigram.pickle', 'wb') as file:
    pickle.dump(english_bigram, file)
with open('english_bigram.txt', 'w') as file:
    file.write(str(english_bigram))

# create french unigrams and bigrams, pickle and save to file
french_unigram, french_bigram = build_language_model('LangId.train.French')
with open('french_unigram.pickle', 'wb') as file:
    pickle.dump(french_unigram, file)
with open('french_unigram.txt', 'w') as file:
    file.write(str(french_unigram))

with open('french_bigram.pickle', 'wb') as file:
    pickle.dump(french_bigram, file)
with open('french_bigram.txt', 'w') as file:
    file.write(str(french_bigram))

# create italian unigrams and bigrams, pickle and save to file
italian_unigram, italian_bigram = build_language_model('LangId.train.Italian')
with open('italian_unigram.pickle', 'wb') as file:
    pickle.dump(italian_unigram, file, protocol=pickle.HIGHEST_PROTOCOL)
    
with open('italian_unigram.txt', 'w') as file:
    file.write(str(italian_unigram))

with open('italian_bigram.pickle', 'wb') as file:
    pickle.dump(italian_bigram, file)
with open('italian_bigram.txt', 'w') as file:
    file.write(str(italian_bigram))
