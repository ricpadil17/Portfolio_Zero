import pickle
from pprint import pprint
import os
from nltk import word_tokenize
from nltk import ngrams

# a. Read in your pickled dictionaries.
# load in english unigram and bigram dictionaries
with open('english_unigram.pickle', 'rb') as file:
    english_unigram = pickle.load(file)
with open('english_bigram.pickle', 'rb') as file:
    english_bigram = pickle.load(file)

# load in french unigram and bigram dictionaries
with open('french_unigram.pickle', 'rb') as file:
    french_unigram = pickle.load(file)
with open('french_bigram.pickle', 'rb') as file:
    french_bigram = pickle.load(file)

# load in italian unigram and bigram dictionaries
with open('italian_unigram.pickle', 'rb') as file:
    italian_unigram = pickle.load(file)
with open('italian_bigram.pickle', 'rb') as file:
    italian_bigram = pickle.load(file)

V = len(english_unigram) + len(french_unigram) + len(italian_unigram)

def calculate_probability(line, unigram, bigram):
    #for each word in the line
    #calculate the probability of the bigram
    unigrams_test = word_tokenize(line)
    bigrams_test = list(ngrams(unigrams_test, 2))

    p_laplace = 1

    for bg in bigrams_test:
        b = bigram[bg] if bg in bigram else 0
        u = unigram[bg[0]] if bg[0] in unigram else 0
        p_laplace = p_laplace * ((b + 1) / (u + V))
    return p_laplace
        

# b. For each line in the test file, calculate a probability for each language and
# write the language with the highest probability to a file.
def guess_the_language():
    with open('LangId.test', 'r') as file:
        test = file.readlines()

    for idx, line in enumerate(test, start=1): 
        # calculate probability of english
        english_probability = calculate_probability(line, english_unigram, english_bigram)
        #print("english_probability: ", english_probability)

        # calculate probability of french
        french_probability = calculate_probability(line, french_unigram, french_bigram)
        #print("french_probability: ", french_probability)

        # calculate probability of italian
        italian_probability = calculate_probability(line, italian_unigram, italian_bigram)
        #print("italian_probability: ", italian_probability)

        highest = max(english_probability, french_probability, italian_probability)


        # write the language with the highest probability to a file
        if highest == english_probability:
            with open('results.txt', 'a') as file:
                file.write(str(idx) + ' English' + '\n')
        elif highest == french_probability:
            with open('results.txt', 'a') as file:
                file.write(str(idx) + ' French' + '\n')
        else:
            with open('results.txt', 'a') as file:
                file.write(str(idx) + ' Italian' + '\n')


def check_accuracy():
    incorrect = 0
# read in langId.sol
    with open('LangId.sol', 'r') as file:
        sol = file.readlines()    
    # compare results.txt to langId.sol
    with open('results.txt', 'r') as file:
        results = file.readlines() 
    # output the line numbers of the incorrectly classified items
    for i in range(len(sol)):
        if sol[i] != results[i]:
            incorrect+=1
            print("incorrect line: " + str(i+1))
    print("incorrect %: " + str(incorrect/len(sol)*100) + "%")

def reset_files():
    if os.path.exists('results.txt'):
        os.remove('results.txt')
    else:
        print('The file does not exist')



reset_files()
guess_the_language()
check_accuracy()

# c. Compute and output your accuracy as the percentage of correctly classified instances in the
# test set. The file LangId.sol holds the correct classifications.


# d. output your accuracy, as well as the line numbers of the incorrectly classified items