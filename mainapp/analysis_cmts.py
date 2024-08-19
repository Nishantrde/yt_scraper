import json
import gensim
import gensim.corpora as corpora
import spacy
import pyLDAvis
import pyLDAvis.gensim

def analysis(data):
    data = data["texts"]

    def lemmatization(texts, allowed_postags=["NOUN", "ADJ", "VERB", "ADV"]):
        nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
        texts_out = []
        for text in texts:
            doc = nlp(text)
            new_text = []
            for token in doc:
                if token.pos_ in allowed_postags:
                    new_text.append(token.lemma_)
            final = " ".join(new_text)
            texts_out.append(final)
        return texts_out

    lemmatized_texts = lemmatization(data)

    def gen_words(texts):
        final = []
        for text in texts:
            new = gensim.utils.simple_preprocess(text, deacc=True)
            final.append(new)
        return final

    data_words = gen_words(lemmatized_texts)

    bigram_phrases = gensim.models.Phrases(data_words, min_count=5, threshold=100)
    trigram_phrases = gensim.models.Phrases(bigram_phrases[data_words], threshold=100)

    bigram = gensim.models.phrases.Phraser(bigram_phrases)
    trigram = gensim.models.phrases.Phraser(trigram_phrases)

    data_bigrams = [bigram[doc] for doc in data_words]
    data_bigrams_trigrams = [trigram[bigram[doc]] for doc in data_bigrams]

    id2word = corpora.Dictionary(data_bigrams_trigrams)
    corpus = [id2word.doc2bow(text) for text in data_bigrams_trigrams]


    lda_model = gensim.models.ldamodel.LdaModel(
        corpus=corpus,
        id2word=id2word,
        num_topics=50,
        random_state=100,
        update_every=1,
        chunksize=200,
        passes=15,
        alpha='auto',
        eta='auto'
    )

    vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word, mds="mmds", R=30)
    lda_html_content = pyLDAvis.prepared_data_to_html(vis)
    
    return lda_html_content
