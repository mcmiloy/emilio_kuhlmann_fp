from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import pandas as pd
from datetime import timedelta

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# NLTK stopwords
from nltk.corpus import stopwords

# spacy for lemmatization
import spacy

# sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

def print_time(t1, t2):
    tm = t2 - t1
    if tm > 3600:
        print('Complete. Elapsed time: {}'.
              format(timedelta(seconds=tm).__str__()[:-4]))
    elif tm > 60:
        print('Complete. Elapsed time: {}'.
              format(timedelta(seconds=tm).__str__()[2:-4]))
    elif tm > 10:
        print('Complete. Elapsed time: {}'.
              format(timedelta(seconds=tm).__str__()[5:-4]))
    else:
        print('Complete. Elapsed time: {}'.
              format(timedelta(seconds=tm).__str__()[6:-4]))


def sent_to_words(sentences):
    '''

    '''
    for sentence in sentences:
        # deacc=True removes punctuations
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))


def text_to_words(texts):
    '''

    '''
    return list(sent_to_words(texts))


# Define functions for stopwords, bigrams, trigrams and lemmatization
def remove_stopwords(texts):
    stop_words = stopwords.words('english')
    return ([[word for word
            in simple_preprocess(str(doc))
            if word not in stop_words] for doc in texts])


def make_bigrams(texts):
    data_words = text_to_words(texts)
    # higher threshold fewer phrases.
    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    return [bigram_mod[doc] for doc in texts]


def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    texts_out = []
    #
    # import en_core_web_sm
    # nlp = en_core_web_sm.load()
    #
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc
                         if token.pos_ in allowed_postags])
    return texts_out


def create_id2word(data):

    return corpora.Dictionary(data)


def create_corpus(id2word, data):

    return [id2word.doc2bow(text) for text in data]


def compute_coherence_values(texts, start=2, stop=30, step=3):

    coherence_values = []
    model_list = []

    id2word = create_id2word(texts)
    corpus = create_corpus(id2word, texts)

    for num_topics in range(start, stop, step):
        print('Calculating {}-topic model'.format(num_topics))
        model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                    id2word=id2word,
                                                    num_topics=20,
                                                    random_state=100,
                                                    update_every=1,
                                                    chunksize=100,
                                                    passes=10,
                                                    alpha='auto',
                                                    per_word_topics=True)
        model_list.append((num_topics, model))
        coherencemodel = CoherenceModel(model=model,
                                        texts=texts,
                                        dictionary=id2word,
                                        coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values, id2word, corpus


def format_topics_sentences(ldamodel, corpus, texts):
    '''

    '''
    # Init output
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row in enumerate(ldamodel[corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['dominant_topic', 'percent_contribution', 'topic_keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return(sent_topics_df)

