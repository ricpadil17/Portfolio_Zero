import os
from argparse import ArgumentParser
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from random import randint


  
lemmatizer = WordNetLemmatizer()


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


parser = ArgumentParser(description="This is a guessing game!")
parser.add_argument("--filename", dest="filename", required=True,
                    help="input file with two matrices", metavar="FILE",
                    type=lambda x: is_valid_file(parser, x))
args = parser.parse_args()


def calculate_lexical_diversity():
    tokens = []
    unique_tokens = []
    with open(args.filename, 'r') as f:
        text = f.read()
    tokens = word_tokenize(text)
    print("token length is: ", len(tokens))

    for token in tokens:
        if token not in unique_tokens:
            unique_tokens.append(token)
    print("unique token length is: ", len(unique_tokens))

    lex_div = len(unique_tokens)/len(tokens)
    format_lex_div = "{:.2f}".format(lex_div)

    print("lexical diversity is:" , format_lex_div)



def lemmatize(tokens):
    lemmas = set()
    for token in tokens:
        lem = lemmatizer.lemmatize(token)
        lemmas.add(lem)
    return lemmas


def preprocess_raw_text():
    no_stop = ""
    lemmas = []
    with open(args.filename, 'r') as f:
        text = f.read()

    nonum = re.sub(r'\d+', '', text)
    nopunct = "".join([char.lower() for char in nonum if char not in string.punctuation]) 
    single_space = re.sub('\s+', ' ', nopunct).strip()
    lower = single_space.lower()
    tokens = word_tokenize(lower)

    for token in tokens:
        if token not in stopwords.words('english') and len(token) > 5:
            no_stop = no_stop + " " + token
    
    processed_tokens = word_tokenize(no_stop)    
    lemmas = lemmatize(processed_tokens)

    # do pos tagging on the unique lemmas and print the first 20 tagged
    tags = pos_tag(lemmas)
    top_20 = tags[:20]
    print("top 20 lemmas are: ", top_20)

    # create a list of only those lemmas that are nouns
    nouns = []
    for tag in tags:
        if tag[1].startswith("NN"):
            nouns.append(tag)

    # print the number of tokens (from step a) and the number of nouns (step d)
    print("Number of tokens from step a. is: ", len(processed_tokens))
    print("Number of  nouns from step d. is: ", len(nouns))

    # return tokens (not unique tokens) from step a, and nouns from the function
    return processed_tokens, nouns
    

def create_dictionary(tuple):
    tokens = tuple[0]
    # noun_tuple_list is a list of tuples [(word,POS)]
    noun_tuple_list = tuple[1]
    nouns = []
    
    # Make a dictionary of {noun:count of noun in tokens}
    for tuple in noun_tuple_list: 
        nouns.append(tuple[0])

    dictionary = dict.fromkeys(nouns, 0)

    for token in tokens:
        if token in dictionary:
            dictionary[token]+=1
    
    # sort the dict by count and print the 50 most common words and their counts
    top_fifty_nouns = sorted(dictionary.items(), key=lambda x:x[1], reverse=True)[:50]
    sorted_dict = dict(top_fifty_nouns)
    print("Top 50 words and their counts: ", sorted_dict)

    # Save these words to a list because they will be used in the guessing game.
    word_list = []
    for word in sorted_dict:
        word_list.append(word)
    return word_list


def print_word(word):
    print(*word, sep = " ") 

def play_game(word_list):
    points = 5
    guess = ""
    print("Let's play a word guessing game!")

    while points > -1 and guess != '!':
        solved = False
        guesses = []
        random_word = word_list[randint(0,49)]
        game_screen = []
        for i in range(len(random_word)):
            game_screen.append("_")

        while solved != True and guess != '!' and points > -1:
            print_word(game_screen)
            guess = input("Guess a letter: ")
            if guess != '!':
                if guess in guesses:
                    print("You already guessed", guess)
                    print("You have also tried ", guesses)
                    print("Try another letter.")
                else:
                    if guess in random_word:
                        points+= 1
                        guesses.append(guess)
                        for idx, letter in enumerate(random_word):
                            if guess == letter:
                                game_screen[idx] = letter
                        if "_" not in game_screen:
                            print(random_word)
                            print("You solved it!\n\nCurrent score is:", points)
                            print("\n\nGuess another word\n")
                            solved = True
                        else:
                            print("Right! Score is", points)
                    else:
                        points -= 1
                        if points >=0:
                            guesses.append(guess)
                            print("Sorry, guess again. Score is: ", points)
                        else:
                            print("The word was: ", random_word)
                            print("Better luck next time!")

    print("Thanks for playing!")

    

calculate_lexical_diversity()
results = preprocess_raw_text()
play_game(create_dictionary(results))