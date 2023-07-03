# Chat Transcripts LDA Topic Modeling
# Developed by [Leslie Ng] on Jul 03, 2023

# Credit:
# - Pandas library: https://pandas.pydata.org/
# - NLTK library: https://www.nltk.org/
# - Gensim library: https://radimrehurek.com/gensim/
# - Googletrans library: https://pypi.org/project/googletrans/

import re
import string
import pandas as pd
import nltk
from nltk.corpus import stopwords
from gensim import corpora, models
from googletrans import Translator

def read_excel(file_path):
    # Read data from an Excel file
    df = pd.read_excel(file_path)
    return df

def download_stopwords(language):
    # Download stopwords for a specific language
    nltk.download('stopwords')
    stop_words = stopwords.words(language)
    return stop_words

def translate_text(text, target_language):
    # Translate text to a target language
    translator = Translator()
    lang = translator.detect(text).lang
    if lang != target_language:
        translated_text = translator.translate(text, dest=target_language).text
        return translated_text
    else:
        return text

def preprocess_text(df, stop_words):
    # Preprocess the text data
    translator = Translator()
    texts = []
    for document in df['chats']:
        # Detect language and translate non-English text to English
        lang = translator.detect(document).lang
        if lang != 'en':
            translated_text = translator.translate(document, dest='en').text
            document = translated_text
        # Tokenize, remove stop words, and remove punctuation marks
        words = [word for word in document.lower().split() if word not in stop_words]
        words = [word.translate(str.maketrans('', '', string.punctuation)) for word in words]
        words = [word for word in words if word]
        texts.append(words)
    return texts

def apply_lda(texts):
    # Create a dictionary and corpus from the preprocessed text
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    # Apply the LDA topic modeling algorithm
    lda_model = models.ldamodel.LdaModel(corpus, num_topics=1, id2word=dictionary)

    # Translate the topic keywords from English to Chinese and Traditional Chinese
    topic_keywords = lda_model.print_topics()[0][1]
    topic_keywords_hk = translate_text(topic_keywords, 'zh-TW')
    topic_keywords_cn = translate_text(topic_keywords, 'zh-CN')
    
    word_en_list = re.findall(r'"([^"]*)"', topic_keywords)
    word_hk_list = re.findall(r'[\u4e00-\u9fa5]+', topic_keywords_hk)
    word_cn_list = re.findall(r'[\u4e00-\u9fa5]+', topic_keywords_cn)

    # Print the main topic and associated keywords in English, Chinese, and Traditional Chinese
    print("en:", ' '.join(word_en_list))
    print("hk:", ' '.join(word_hk_list))
    print("cn:", ' '.join(word_cn_list))

# Read the data from the Excel file
df = read_excel('chat_transcripts.xlsx')

# Download the stopwords for English
stop_words = download_stopwords('english')

# Preprocess the text data
texts = preprocess_text(df, stop_words)

# Apply the LDA topic modeling algorithm and print the results
apply_lda(texts)