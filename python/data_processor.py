import gzip
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import re
from nltk import FreqDist
from nltk import word_tokenize         
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from scipy.sparse import coo_matrix, hstack
from nltk.util import ngrams
from sklearn.preprocessing import StandardScaler
import random
from sklearn.feature_extraction.text import TfidfTransformer
import langdetect
import newspaper
import os.path


class LemmaTokenizer(object):
     def __init__(self):
         self.wordnet_lemmatizer = WordNetLemmatizer()
     def __call__(self, doc):
         return [self.wordnet_lemmatizer.lemmatize(t) for t in word_tokenize(doc)]

class StemTokenizer(object):
     def __init__(self):
         self.lancaster_stemmer = LancasterStemmer()
     def __call__(self, doc):
         return [self.lancaster_stemmer.stem(t) for t in word_tokenize(doc)]

# get adj when tokenize
# is not called in the code right now jsut for experiment
class adjTokenizer(object):
     def __init__(self):
        pass

     def __call__(self, doc):
        text = word_tokenize(doc)
        pos = nltk.pos_tag(text,tagset='universal')
        result = []
        for a,b in pos:
            if b=='ADJ':
                result.append(a)
        return result

class keyword_generator(object):
     def __init__(self):
         self.wordnet_lemmatizer = WordNetLemmatizer()
         self.lancaster_stemmer = LancasterStemmer()

     def __call__(self, doc):
        text = word_tokenize(doc)
        pos = nltk.pos_tag(text,tagset='universal')
        result = []

        for i in range(len(pos)):
            word,tag = pos[i]
            # if tag in ["NOUN"]:
            #     result.append(word)

            #stop 
            if(i==len(pos)-1):
                # result = [self.wordnet_lemmatizer.lemmatize(t) for t in result]

                # return [self.lancaster_stemmer.stem(t) for t in result]
                return result
            
            word_next,tag_next = pos[i+1]
            if (tag=='NOUN' and tag_next =='NOUN'):
                result.append(word+" "+word_next)
            # if (tag=='ADV' and tag_next =='ADJ'):
            #     result.append(word+" "+word_next)
            # if (tag=='ADJ' and tag_next =='ADJ'):
            #     result.append(word+" "+word_next)


class bigrams_Tokenizer(object):
     def __init__(self):
         self.wordnet_lemmatizer = WordNetLemmatizer()
         self.lancaster_stemmer = LancasterStemmer()

     def __call__(self, doc):
        text = word_tokenize(doc)
        pos = nltk.pos_tag(text,tagset='universal')
        result = []

        if(len(pos) == 0):
            result = [self.wordnet_lemmatizer.lemmatize(t) for t in result]
            return [self.lancaster_stemmer.stem(t) for t in result]

        for i in range(len(pos)):
            word,tag = pos[i]
            if tag in ["NOUN", "ADV", "ADJ"]:
                result.append(word)

            #stop 
            if(i==len(pos)-1):
                result = [self.wordnet_lemmatizer.lemmatize(t) for t in result]
                return [self.lancaster_stemmer.stem(t) for t in result]
                # return result
            
            word_next,tag_next = pos[i+1]
            if (tag=='NOUN' and tag_next =='NOUN'):
                result.append(word+" "+word_next)
            if (tag=='ADV' and tag_next =='ADJ'):
                result.append(word+" "+word_next)
            if (tag=='ADJ' and tag_next =='ADJ'):
                result.append(word+" "+word_next)


def _parse(path):
    '''
        get the data from gzip file
    '''
    g = open(path, 'r')
    return g.readlines()

def _getData_pos_neg(data, num, haveTarget = False):
    '''
    input:
        data, num (num of data points we want to use)
    output:
        feature: 
            get review text from the data
            then remove punctuation and convert to lowercase
        target:
            positive and negative for each data point (good, bad)
    '''
    feature = []
    target = []
    count = 0
    import collections
    addedUrls = collections.OrderedDict()
    random.shuffle(data)
    while count < num and count < len(data):
        d = data[count]
        count+=1
        try:
            if haveTarget:
                url, t = d.split(',')
            else:
                url = d
            url = url.strip()
            if not os.path.exists(encode_url(url)):
                # print("downloading data...")
                article = newspaper.Article(url, language='en')
                article.download()
                article.parse()
                f = open(encode_url(url), 'w')
                f.write(article.title + '\n')
                f.write(article.text)
                f.close()
            f = open(encode_url(url), 'r')
            content = f.read()
            if not haveTarget and len(content) < 350:
                # print("content lens too short skipping...")
                num+=1
                continue
            feature.append(content)
            addedUrls[url] = content
            if haveTarget:
                if t.strip() == "1":
                    target.append("good")
                else:
                    target.append("bad")

        except:
            pass
    if haveTarget:
        c = list(zip(feature, target))
        random.shuffle(c)
        feature, target = zip(*c)
        return feature,target
    else:
        return feature, addedUrls

        
def encode_url(url, prefix = "testData/"):
    import hashlib
    return prefix + hashlib.md5(url.encode('utf-8')).hexdigest()


def normalize(lst):
    s = sum(lst)
    res = map(lambda x: float(x)/s, lst)
    return [int(i * 10000) for i in res]

def getKeywords(model, data):
    print("generating keywords")

    vectorizer = CountVectorizer(min_df=1)

    vectorizer.stop_words = stopwords.words('english')

    vectorizer.tokenizer = keyword_generator()
    # vectorizer.tokenizer = RegexpTokenizer(r'\w+')
    feature_matrix = vectorizer.fit_transform(data)

    # transformer = TfidfTransformer().fit(feature_matrix)
    # feature_matrix = transformer.transform(feature_matrix)

    vocab = list(vectorizer.get_feature_names())

    counts = normalize(feature_matrix.sum(axis=0).A1)
    from collections import Counter
    freq_distribution = Counter(dict(zip(vocab, counts)))
    res = dict(freq_distribution.most_common(500))
    badwords = open("bad-words.txt", "r").readlines()
    badwords = set(word.strip() for word in badwords)
    nres = dict()
    for words in res:
        for word in words.split():
            if word in badwords:
                nres[words] = res[words]
                print(words , nres[words])
                continue
    import json
    json_str = json.dumps(nres)
    # print(json_str)
    f = open(model + "_keywords.json", "w")
    f.write(json_str)
    f.close()
    return freq_distribution


def pipeline_process_data(paths, haveTarget = False, dataNum = 500):
    '''
        input:

        output:
    '''
    memoize=True

    if not haveTarget:
        for path in paths:
            if not os.path.exists(encode_url(path)):
                memoize = False
            else:
                memoize = True
            print("\nloading news from ", path)
            paper = newspaper.build(path, memoize_articles = memoize)
            urls = []
            f = open(encode_url(path, "URLData/"), 'w')
            for article in paper.articles:
                urls.append(article.url)
                f.write(article.url + "\n")
            f.close()


    if haveTarget:
        feature, target = _getData_pos_neg(_parse(paths), dataNum, haveTarget = True)
    else:
        urls = []
        for path in paths:
            f = open(encode_url(path, "URLData/"), 'r')
            urls.extend(f.readlines())
        feature, data =_getData_pos_neg(urls, dataNum, haveTarget = False)

    vectorizer = CountVectorizer(min_df=1)

    vectorizer.stop_words = stopwords.words('english')

    vectorizer.tokenizer = bigrams_Tokenizer()
    # vectorizer.tokenizer = RegexpTokenizer(r'\w+')
    vectorizer.max_features = 2000
    feature_matrix = vectorizer.fit_transform(feature)

    transformer = TfidfTransformer().fit(feature_matrix)
    feature_matrix = transformer.transform(feature_matrix)

    if haveTarget:
        return feature_matrix, target   
    else:
        return feature_matrix, data
    

# ##test code
# if __name__ == "__main__":
    # X,Y = pipeline_process_data('/Users/gaoqin/Downloads/reviews_Video_Games.json.gz')
    # X = pipeline_process_data('https://www.huffingtonpost.com/')
    # count = [0,0,0,0,0]
    # for i in Y[400:]:
    #   count[int(i - 1)] += 1
    # print (count)