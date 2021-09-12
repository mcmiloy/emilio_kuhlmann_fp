import pandas as pd
import time
import sys
import src.helper_functions as hf
import gensim

# Plotting tools
import pyLDAvis
import pyLDAvis.gensim_models
import matplotlib.pyplot as plt

# nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

# suppress deprecation warnings
import warnings
warnings.simplefilter("ignore", DeprecationWarning)


class BasicNLP(object):

    def __init__(self, texts, titles=False):
        '''
        Initializes documents and document names. Titles is optional.
        '''
        start = time.time()
        print('Loading corpus...     ', end=' '), sys.stdout.flush()
        self.documents = texts
        if not titles:
            self.doc_names = ['document_' + doc for doc in range(len(texts))]
        else:
            self.doc_names = titles
        self.number_of_topics = None
        self.model_list = []
        self.lda_model = None
        self.sentiments = [[] for doc in range(len(texts))]
        hf.print_time(start, time.time())
        self.prepare_texts(start)

    def prepare_texts(self, start):
        '''

        '''
        print('Splitting documents...', end=' ')
        texts = hf.text_to_words(self.documents)
        hf.print_time(start, time.time())
        print('Removing stopwords... ', end=' '), sys.stdout.flush()
        texts = hf.remove_stopwords(texts)
        hf.print_time(start, time.time())
        print('Building bigrams...   ', end=' '), sys.stdout.flush()
        texts = hf.make_bigrams(texts)
        hf.print_time(start, time.time())
        print('Lemmatizing text...   ', end=' '), sys.stdout.flush()
        texts = hf.lemmatization(texts, allowed_postags=['NOUN',
                                                         'ADJ',
                                                         'VERB',
                                                         'ADV'])
        hf.print_time(start, time.time())
        self.texts = texts

    def compute_coherence(self, start=2, stop=30, step=3):
        '''

        '''
        stop += 1
        texts = self.texts
        (self.model_list,
         coherence_values,
         self.id2word,
         self.corpus) = hf.compute_coherence_values(texts=texts,
                                                    start=start,
                                                    stop=stop,
                                                    step=step)

        # Show graph
        x = range(start, stop, step)
        plt.plot(x, coherence_values)
        plt.xlabel("Num Topics")
        plt.ylabel("Coherence score")
        # plt.legend(("coherence_values"), loc='best')
        plt.show()

        # Print the coherence scores
        for m, cv in zip(x, coherence_values):
            print("Num Topics =",
                  m,
                  " has Coherence Value of",
                  round(cv, 6))

    def set_number_of_topics(self, number):
        '''

        '''
        self.number_of_topics = number
        if self.model_list is not None:
            if number in self.model_list:
                for model in self.model_list:
                    if model[0] == self.number_of_topics:
                        self.lda_model = model[1]
                        self.model.append((number, model[1]))
            else:
                self._run_model(number)
        else:
            self._run_model(number)
        self.topic_sents_keywords = hf.format_topics_sentences(self.lda_model,
                                                               self.corpus,
                                                               self.documents)
        self.dominant_topic = self.topic_sents_keywords.reset_index()
        self.dominant_topic.columns = (['document_no',
                                        'dominant_topic',
                                        'topic_percent_contribution',
                                        'keywords',
                                        'text'])

    def _run_model(self, number):
        '''

        '''
        model = hf.compute_coherence_values(texts=self.texts,
                                            start=number,
                                            stop=number + 1,
                                            step=1)
        self.lda_model = model[0][0][1]
        self.id2word = model[2]
        self.corpus = model[3]
        self.model_list.append((number, model[0][0][1]))

    def view_clusters(self):
        '''
        
        '''
        if self.number_of_topics is None:
            print('Error: Number of topics not set.')
            print('Set number of topics with [object].set_number_of_topics(X)')
            return
        self.id2word = hf.create_id2word(self.texts)
        self.corpus = hf.create_corpus(self.id2word, self.texts)

        clusters = self.number_of_topics

        # Build LDA model
        lda_model = gensim.models.ldamodel.LdaModel(corpus=self.corpus,
                                                    id2word=self.id2word,
                                                    num_topics=clusters,
                                                    update_every=1,
                                                    chunksize=100,
                                                    passes=10,
                                                    alpha='auto',
                                                    per_word_topics=True)

        # Display clusters
        pyLDAvis.enable_notebook()
        vis = pyLDAvis.gensim_models.prepare(lda_model, self.corpus, self.id2word)
        pyLDAvis.display(vis)

        # import pyLDAvis
        # import pyLDAvis.gensim_models as gensimvis
        # pyLDAvis.enable_notebook()

        return vis

    def get_topic_vocabulary(self, topics='all', num_words=10):
        '''

        '''
        if topics == 'all':
            topics = list(range(self.number_of_topics))
        elif isinstance(topics, int):
            topics = [topics]
        for topic in sorted(self.lda_model.show_topics(num_topics=self.number_of_topics,
                                                       num_words=num_words,
                                                       formatted=False),
                            key=lambda x: x[0]):
            if topic[0] in topics:
                print('Topic {}: {}'.format(topic[0],
                                            [item[0] for item in topic[1]]))

    def get_representative_documents(self, topics='all', num_docs=1):
        '''

        '''
        if topics == 'all':
            topics = list(range(self.number_of_topics))
        elif isinstance(topics, int):
            topics = [topics]

        df2 = self._make_df(num_docs)

        for idx, row in df2.iterrows():
            if row['topic_num'] in topics:
                print(int(row['topic_num']))
                print(row['text'])
                print()

    def get_representative_sentences(self, topics='all', num_sentences=3):
        '''

        '''
        if topics == 'all':
            topics = list(range(self.number_of_topics))
        elif isinstance(topics, int):
            topics = [topics]

        df2 = self._make_df(1)

        data = df2[df2['topic_num'].isin(topics)]['keywords'].tolist()
        bonus_words = [text.split(', ') for text in data]

        for idx, topic in enumerate(topics):
            print('Topic: {}'.format(topic))
            words = bonus_words[idx]
            # split up bigrams used in LDA model
            words = ([item for sublist in
                     [item.split('_') for item in words] for item in sublist])

            text = df2[df2['topic_num'] == topic]['text'].iloc[0]
            summary = hf.summarize(text, num_sentences, words)
            for sentence in summary:
                print(sentence)
            print()

    def get_document_summaries(self, documents='all', num_sent=5):
        '''

        '''
        if documents == 'all':
            documents = list(range(len(self.documents)))
        elif isinstance(documents, int):
            documents = [documents]

        df = self.topic_sents_keywords

        data = df[df.index.isin(documents)]['topic_keywords'].tolist()
        bonus_words = [text.split(', ') for text in data]

        for document in documents:
            print(self.doc_names[document])
            words = bonus_words[document]
            words = ([item for sublist in
                     [item.split('_') for item in words] for item in sublist])
            words.extend(self.doc_names[document].lower().split())
            for sentence in hf.summarize(self.documents[document], num_sent, words):
                print(sentence)
            print()

    def _make_df(self, num):
        '''

        '''
        df = self.topic_sents_keywords.groupby('dominant_topic')
        df2 = pd.DataFrame()

        for i, grp in df:
            df2 = pd.concat([df2, grp.sort_values(['percent_contribution'],
                            ascending=[0]).head(num)],
                            axis=0)

        # Reset index
        df2.reset_index(drop=True, inplace=True)

        # Format
        df2.columns = ['topic_num',
                       'topic_percent_contribution',
                       'keywords',
                       'text']
        return df2

    def name_topic(self, topic_number, topic_name):
        '''

        '''
        self.topic_names[topic_number] = topic_name

    def get_sentiment(self, documents='all'):
        '''

        '''
        if documents == 'all':
            documents = list(range(len(self.documents)))
        elif isinstance(documents, int):
            documents = [documents]

        analyzer = SentimentIntensityAnalyzer()

        for doc in documents:
            text = self.documents[doc]
            sentence_list = tokenize.sent_tokenize(text)
            sentiments = {'compound': 0.0, 'neg': 0.0, 'neu': 0.0, 'pos': 0.0}

            for sentence in sentence_list:
                vs = analyzer.polarity_scores(sentence)
                sentiments['compound'] += vs['compound']
                sentiments['neg'] += vs['neg']
                sentiments['neu'] += vs['neu']
                sentiments['pos'] += vs['pos']

            cnt = len(sentence_list)
            sentiments['compound'] = sentiments['compound'] / cnt
            sentiments['neg'] = sentiments['neg'] / cnt
            sentiments['neu'] = sentiments['neu'] / cnt
            sentiments['pos'] = sentiments['pos'] / cnt

            print(self.doc_names[doc])
            print(sentiments)
            self.sentiments[doc] = sentiments
