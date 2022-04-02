import pandas as pd
import re
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk import WordNetLemmatizer
import nltk

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('omw-1.4')


def kaggle_strip_reviews(dfReviews):
    dfStrippedReviews = dfReviews[["Hotel_Name", "Review_Total_Negative_Word_Counts",
                                   "Review_Total_Positive_Word_Counts", "Reviewer_Score"]]

    # copy both Negative and Positive reviews into one collums and remove No Negative and No Positive statements
    dfStrippedReviews["Review"] = dfReviews["Negative_Review"].apply(lambda x: x.replace("No Negative", "")) + \
                                  dfReviews["Positive_Review"].apply(lambda x: x.replace("No Positive", ""))
    return dfStrippedReviews


def kaggle_label_data(dfReviews):
    dfReviewScore = dfReviews[["Review", "Review_Total_Negative_Word_Counts", "Review_Total_Positive_Word_Counts"]]
    dfReviewScore = dfReviewScore.rename(columns={"Review_Total_Negative_Word_Counts": "negative_word_count",
                                                  "Review_Total_Positive_Word_Counts": "positive_word_count"})

    # Score 5.5 means that there are ~8% negative(~40k). Score 5 means 6% negative(~30k). Do at max 8% split
    dfReviewScore["label"] = dfReviews['Reviewer_Score'].apply(lambda x: 1 if x > 5.5 else 0)

    return dfReviewScore


def own_label_data(dfReviews):
    dfReviewLabel = pd.DataFrame()
    dfReviewLabel["Review"] = dfReviews[['review']]
    dfReviewLabel["label"] = dfReviews['review_score'].apply(lambda x: 1 if x > 5.5 else 0)

    return dfReviewLabel


def preprocess_review(reviews):
    REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\d+)")
    REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
    NO_SPACE = ""
    SPACE = " "

    reviews = [REPLACE_NO_SPACE.sub(NO_SPACE, line.lower()) for line in reviews]
    reviews = [REPLACE_WITH_SPACE.sub(SPACE, line) for line in reviews]

    return reviews


def remove_stop_words(reviews):
    english_stop_words = stopwords.words('english')
    removed_stop_words = []
    addition_stop_words = ['hotel', 'room', 'breakfast', 'staff', 'rooms', 'location', 'u']
    for review in reviews:
        removed_stop_words.append(
            ' '.join([word for word in review.split()
                      if (word not in english_stop_words) and (word not in addition_stop_words)])
        )

    return removed_stop_words


def stem_text(reviews):
    stemmer = PorterStemmer()
    return [' '.join([stemmer.stem(word) for word in review.split()]) for review in reviews]


def lem_text(reviews):
    lemmatizer = WordNetLemmatizer()
    return [' '.join([lemmatizer.lemmatize(word) for word in review.split()]) for review in reviews]


def clean_data(dfReviews):
    dfReviews['processedReviews'] = preprocess_review(dfReviews['Review'])
    dfReviews['stopwordsReviews'] = remove_stop_words(dfReviews['processedReviews'])
    dfReviews['stemmedReviews'] = stem_text(dfReviews['stopwordsReviews'])
    dfReviews['lemReviews'] = lem_text(dfReviews['stemmedReviews'])

    return dfReviews
