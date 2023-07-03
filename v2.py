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

def preprocess_intent(df, intent_name, stop_words):
    # Preprocess the text data for a specific intent
    translator = Translator()
    texts = []
    for document in df.loc[df['intent_name'] == intent_name, 'userExpression']:
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

def apply_lda_to_intent(texts, intent_name):
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
    
    # Print the intent name and main topic and associated keywords in English, Chinese, and Traditional Chinese
    print("\nIntent:", intent_name)
    print("en:", ' '.join(word_en_list))
    print("hk:", ' '.join(word_hk_list))
    print("cn:", ' '.join(word_cn_list))

    # Return the intent name and main topic and associated keywords in English, Chinese, and Traditional Chinese as a tuple
    return (intent_name, ' '.join(word_en_list), ' '.join(word_hk_list), ' '.join(word_cn_list))

# Read the data from the Excel file
df = read_excel('exported_training_set.xlsx')

# Download the stopwords for English
stop_words = download_stopwords('english')

# Apply LDA to each intent and store the results in a list of tuples
lda_results = []
for intent_name, group_df in df.groupby('intent_name'):
    # Preprocess the text data for the current intent
    texts = preprocess_intent(group_df, intent_name, stop_words)

    # Apply the LDA topic modeling algorithm and store the results as a tuple
    lda_result = apply_lda_to_intent(texts, intent_name)
    lda_results.append(lda_result)

# Convert the list of tuples to a pandas DataFrame and write it to an Excel file
df_lda_results = pd.DataFrame(lda_results, columns=['Intent Name', 'English', 'Traditional Chinese', 'Simplified Chinese'])
df_lda_results.to_excel('lda_results.xlsx', index=False)
