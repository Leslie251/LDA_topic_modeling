# LDA Topic Modeling on Intent Data

This is a Python script that applies Latent Dirichlet Allocation (LDA) topic modeling to intent data and outputs the main topic and associated keywords for each intent in English, Simplified Chinese, and Traditional Chinese. The data is read in from an Excel file and the LDA results are written to a new Excel file.

## Requirements

To run the script, you will need the following Python packages:

- pandas
- nltk
- gensim
- googletrans

You will also need NLTK's stopwords data. You can download it by running `nltk.download('stopwords')` in your Python environment.

## Usage

1. Install the required packages and download the stopwords data as described above.
2. Place your intent data in an Excel file named `exported_training_set.xlsx` in the same directory as the script.
3. Run the script using `python lda_topic_modeling.py`.
4. The script will output the main topic and associated keywords for each intent in English, Simplified Chinese, and Traditional Chinese to the console and write the results to an Excel file named `lda_results.xlsx` in the same directory as the script.

## Notes

- The code assumes that the intent data is in an Excel file named `exported_training_set.xlsx` with columns named `intent_name` and `userExpression`.
- The code currently applies LDA with a fixed number of topics of 1, which means it will only output the main topic and associated keywords for each intent.
- The code uses the Google Translate API to translate non-English text to English and then to Simplified Chinese and Traditional Chinese. You will need to provide your own API key if you wish to use this feature.
- The code removes stopwords and punctuation marks from the text data before applying LDA. You can modify the `download_stopwords` and `preprocess_intent` functions to use different stopwords data or apply different text preprocessing steps if desired.
