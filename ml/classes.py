import re
import string

import joblib
import spacy
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer


class DataPreprocessor:
    def __init__(self):
        self.__stop_words = set(stopwords.words("english"))
        self.__stop_words.remove("not")
        self.__nlp = spacy.load("en_core_web_sm")
        self.__mapping_dictionary = {
            "ain't": "is not", "aren't": "are not", "can't": "cannot",
            "'cause": "because", "could've": "could have", "couldn't": "could not",
            "didn't": "did not", "doesn't": "does not", "don't": "do not", "hadn't": "had not",
            "hasn't": "has not", "haven't": "have not", "he'd": "he would", "he'll": "he will",
            "he's": "he is", "how'd": "how did", "how'd'y": "how do you", "how'll": "how will",
            "how's": "how is", "I'd": "I would", "I'd've": "I would have", "I'll": "I will",
            "I'll've": "I will have", "I'm": "I am", "I've": "I have", "i'd": "i would",
            "i'd've": "i would have", "i'll": "i will", "i'll've": "i will have",
            "i'm": "i am", "i've": "i have", "isn't": "is not", "it'd": "it would",
            "it'd've": "it would have", "it'll": "it will", "it'll've": "it will have",
            "it's": "it is", "let's": "let us", "ma'am": "madam", "mayn't": "may not",
            "might've": "might have", "mightn't": "might not", "mightn't've": "might not have",
            "must've": "must have", "mustn't": "must not", "mustn't've": "must not have",
            "needn't": "need not", "needn't've": "need not have", "o'clock": "of the clock",
            "oughtn't": "ought not", "oughtn't've": "ought not have", "shan't": "shall not",
            "sha'n't": "shall not", "shan't've": "shall not have", "she'd": "she would",
            "she'd've": "she would have", "she'll": "she will", "she'll've": "she will have",
            "she's": "she is", "should've": "should have", "shouldn't": "should not",
            "shouldn't've": "should not have", "so've": "so have", "so's": "so as", "this's": "this is",
            "that'd": "that would", "that'd've": "that would have", "that's": "that is",
            "there'd": "there would", "there'd've": "there would have", "there's": "there is",
            "here's": "here is", "they'd": "they would", "they'd've": "they would have",
            "they'll": "they will", "they'll've": "they will have", "they're": "they are",
            "they've": "they have", "to've": "to have", "wasn't": "was not", "we'd": "we would",
            "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have",
            "we're": "we are", "we've": "we have", "weren't": "were not",
            "what'll": "what will", "what'll've": "what will have", "what're": "what are",
            "what's": "what is", "what've": "what have", "when's": "when is", "when've": "when have",
            "where'd": "where did", "where's": "where is", "where've": "where have", "who'll": "who will",
            "who'll've": "who will have", "who's": "who is", "who've": "who have", "why's": "why is",
            "why've": "why have", "will've": "will have", "won't": "will not", "won't've": "will not have",
            "would've": "would have", "wouldn't": "would not", "wouldn't've": "would not have",
            "y'all": "you all", "y'all'd": "you all would", "y'all'd've": "you all would have",
            "y'all're": "you all are", "y'all've": "you all have", "you'd": "you would",
            "you'd've": "you would have", "you'll": "you will", "you'll've": "you will have",
            "you're": "you are", "you've": "you have", "'ll": "will", "'d": "would"
        }

    def preprocess_review(self, review: str, lemmatize: bool = False) -> str:
        review = BeautifulSoup(review, "html.parser").get_text().lower()
        review = re.sub(r"http\S+|www\S+|https\S+|@[^\s]+", "", review)
        review = re.sub(r"\s+", " ", review)
        review = re.sub(r"\.{2,}", ".", review)
        review = re.sub(r"\d+", "", review)

        words = word_tokenize(review)
        words = [self.__mapping_dictionary[word] if word in self.__mapping_dictionary else word for word in words]
        words = [word for word in words if word not in string.punctuation]
        words = [word for word in words if word not in self.__stop_words]

        if lemmatize:
            words = [self.__nlp(word)[0].lemma_ for word in words]

        return " ".join(words)


class Model:
    def __init__(
        self,
        datapreprocessor: DataPreprocessor,
        vectorizer: TfidfVectorizer,
        random_forest: RandomForestClassifier
    ):
        self.datapreprocessor = datapreprocessor
        self.__vectorizer = vectorizer
        self.__random_forest = random_forest

    @property
    def datapreprocessor(self) -> DataPreprocessor:
        return self.__datapreprocessor

    @datapreprocessor.setter
    def datapreprocessor(self, datapreprocessor: DataPreprocessor) -> None:
        if not isinstance(datapreprocessor, DataPreprocessor):
            raise TypeError("L'argument datapreprocessor doit être de type \"DataPreprocessor\"")

        self.__datapreprocessor = datapreprocessor

    @property
    def vectorizer(self) -> TfidfVectorizer:
        return self.__vectorizer

    @vectorizer.setter
    def vectorizer(self, vectorizer: TfidfVectorizer) -> None:
        if not isinstance(vectorizer, TfidfVectorizer):
            raise TypeError("L'argument vectorizer doit être de type \"TfidfVectorizer\"")

        self.__vectorizer = vectorizer

    @property
    def random_forest(self) -> RandomForestClassifier:
        return self.__random_forest

    @random_forest.setter
    def random_forest(self, random_forest: RandomForestClassifier) -> None:
        if not isinstance(random_forest, RandomForestClassifier):
            raise TypeError("L'argument random_forest doit être de type \"RandomForestClassifier\"")

        self.__random_forest = random_forest

    def predict(self, new_review: str) -> int:
        if self.datapreprocessor is None or self.vectorizer is None or self.random_forest is None:
            raise RuntimeError("Le modèle n'est pas dans un état valide pour effectuer des prédictions")

        prediction = self.random_forest.predict(
            self.vectorizer.transform([self.datapreprocessor.preprocess_review(new_review, lemmatize=True)])
        )
        return int(prediction[0])

    def save(self, file_path: str) -> None:
        Model.__validate_file_path(file_path)
        joblib.dump(self, file_path)

    @staticmethod
    def load(file_path: str) -> "Model":
        Model.__validate_file_path(file_path)

        result = joblib.load(file_path)
        if not isinstance(result, Model):
            raise TypeError(f"Le modèle dans le fichier \"{file_path}\" n'est pas de type \"Model\"")

        return result

    @staticmethod
    def __validate_file_path(file_path: str) -> None:
        if not isinstance(file_path, str):
            raise TypeError("L'argument file_path doit être de type \"string\"")
        if file_path.strip() == "":
            raise ValueError("L'argument file_path ne peut pas être vide")
