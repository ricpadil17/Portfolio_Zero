import requests
from bs4 import BeautifulSoup
from queue import Queue
from pprint import pprint
import urllib.request
import random
import re
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import numpy as np



#Possible Starter Urls
#https://time.com/6103335/seinfeld-netflix-business/
#http://jerryseinfeld.com/
#https://seinfeld.fandom.com/wiki/WikiSein

starter_url = "https://seinfeld.fandom.com/wiki/WikiSein"

q = Queue(maxsize = 0)
visited = []



user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
]

def gather_soup_ingredients(page):
    r = requests.get(page)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    return soup

def clean_up_url(link_str):
    if link_str.startswith('/url?q='):
        link_str = link_str[7:]
        print('MOD:', link_str)
    if '&' in link_str:
        i = link_str.find('&')
        link_str = link_str[:i]
    return link_str


def link_Is_Relevant(link_str):
    if 'Seinfeld' in link_str or 'seinfeld' in link_str:
        if link_str.startswith('http') and \
            'google' not in link_str and \
            'Special:' not in link_str and \
            'Category:' not in link_str and \
            '.jpg'  not in link_str:
            return True
        else:
            return False
    else: 
        return False


def crawl_single_page(page, f):
    visited.append(page)
    soup = gather_soup_ingredients(page)
    f.write("\n\n\nHERE ARE THE LINKS FROM PAGE: "+ page + "\n")

    for link in soup.find_all('a'):
        raw_link = str(link.get('href'))
        link_str = clean_up_url(raw_link)
        if link_Is_Relevant(link_str):
            if link_str not in visited:
                q.put(link_str)
                f.write(link_str + '\n')



def crawl(link_threshold):
    with open('urls.txt', 'w') as f:
        while (len(visited) < link_threshold) and not q.empty():
            link = q.get()
            crawl_single_page(link, f)

        
def print_queue():
    print(list(q.queue))

def print_visited():
    print("\n\nVISITED LINKS WERE AS FOLLOWS: \n")
    pprint(visited)

def read_urls():
    with open('urls.txt', 'r') as f:
        urls = f.read().splitlines()
        for u in urls:
            print(u)
                



# function to determine if an element is visible
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

#2. Write a function to loop through your URLs and scrape all text off each page. Store each
#page’s text in its own file.
def download_raw_corpus(): 

    for idx, url in enumerate(visited): 
        try:
            filename = str(idx) + ".txt"
            with open( filename, 'w') as f:
                html = requests.get(url, headers={'User-Agent': random.choice(user_agents_list)})
                #print(html.text)
                #html = urllib.request.urlopen(url)
                soup = BeautifulSoup(html.text, 'html.parser')
                data = soup.findAll(text=True)
                result = filter(visible, data)
                temp_list = list(result)      # list from filter
                temp_str = ' '.join(temp_list)
                print(temp_str)
                f.write(temp_str)
        except urllib.error.HTTPError: 
            print("Unable to access " + url + "\nAccess is forbidden.\n")
        except TypeError as e: 
            print(e)



#3. Write a function to clean up the text from each file. You might need to delete newlines
#and tabs first. Extract sentences with NLTK’s sentence tokenizer. Write the sentences for
#each file to a new file. That is, if you have 15 files in, you have 15 files out.

def clean_file(file):
    cleaned = file.replace('\n', '')
    cleaned = cleaned.replace('\t', '')
    cleaned = cleaned.replace('\r','')
    cleaned = " ".join(cleaned.split())
    return cleaned


def clean_up_corpus():
    cleaned_file = ''
    sentences = ''

    for idx, url in enumerate(visited): 
        unclean_filename = str(idx) + ".txt"
        clean_filename = str(idx) + "_clean.txt"
        with open(unclean_filename, 'r') as f: 
            data = f.read()
            #print(data)
            cleaned_file = clean_file(data)
            try:
                sentences = sent_tokenize(cleaned_file)
            except TypeError as e:
             print(e)
            #print(sentences)

        with open (clean_filename, 'w') as f:
            for sentence in sentences:
                f.write(sentence + '\n')
        

# 4. Write a function to extract at least 25 important terms from the pages using an
# importance measure such as term frequency, or tf-idf. 

# First, it’s a good idea to lowercase everything, remove stopwords and punctuation. 
# Print the top 25-40 terms.

def remove_aposterphe(data):
    return np.char.replace(data, "'", "").tolist()


def remove_punctuation(data):
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n•"
    for i in symbols:
        data = np.char.replace(data, i, ' ')
    return_string = np.array2string(data)
    return return_string

def remove_stop_words(data):
    filtered = ""
    words = data.split()
    for word in words: 
        if word not in stopwords.words('english'):
            filtered = filtered + " " + word
    return filtered

def remove_single_characters(data):
    words = data.split()
    new_text = ""
    for w in words:
        if len(w) > 1:
            new_text = new_text + " " + w
    return new_text

def preprocess_data(file):
    data = file.lower()
    data = remove_punctuation(data)
    data = remove_aposterphe(data)
    data = remove_single_characters(data)
    data = remove_stop_words(data)
    #data = stemming(data)
    #data = lemming(data)
    #print(data)
    return data

def extract_important_terms():
    documents = []
    corpus = []
    # get all the sentences from all the files
    for idx in range(15):
        filename = str(idx) + "_clean.txt"
        with open (filename, 'r') as f:
            data = f.read()
        documents.append(data)

    # preprocess the data
    for idx in range(15):
        corpus.append(preprocess_data(documents[idx]))
    
    tf_idf(corpus)




#given a corpus of documents, compute the tf-idf
def tf_idf(corpus: list) -> list:

    DF = {}
    for i in range(len(corpus)):
        tokens = corpus[i].split()
        for w in tokens:
            try:
                DF[w].add(i)
            except:
                DF[w] = {i}

    for i in DF: 
        DF[i] = len(DF[i])
    print(DF)
    return tf(corpus)*idf(corpus)

def tf(corpus):
    tfDict = {}
    bagOfWordsCount = len(bagOfWords)
    for word, count in wordDict.items():
        tfDict[word] = count / float(bagOfWordsCount)
    return tfDict

def idf(corpus):
    import math
    N = len(corpus)
    
    idfDict = dict.fromkeys(corpus[0].keys(), 0)
    for document in corpus:
        for word, val in document.items():
            if val > 0:
                idfDict[word] += 1
    
    for word, val in idfDict.items():
        idfDict[word] = math.log(N / float(val))
    return idfDict

    
    # order the results by tf-idf score
    # print the top 40 results
    # write top 40 results to a file


# DO NOT DELETE - GETS URLS
# q.put(starter_url)
# crawl(15)
# print_visited()
# download_raw_corpus()
# clean_up_corpus()
extract_important_terms()

#5. Manually determine the top 10 terms from step 4, based on your domain knowledge.

def print_top_ten():
    pass

#6. Build a searchable knowledge base of facts that a chatbot (to be developed later) can
#share related to the 10 terms. The “knowledge base” can be as simple as a Python dict
#which you can pickle. More points for something more sophisticated like sql.

def build_knowledge_base():
    pass


#7. In a doc: (1) describe how you created your knowledge base, include screen shots of the
#knowledge base, and indicate your top 10 terms; (2) write up a sample dialog you would
#like to create with a chatbot based on your knowledge base

#8. Create a link to the report and code on your index page
