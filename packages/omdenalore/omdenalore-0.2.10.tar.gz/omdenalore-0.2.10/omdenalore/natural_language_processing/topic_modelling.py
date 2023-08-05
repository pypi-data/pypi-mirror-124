from enum import Enum
from pprint import pprint
from typing import Dict, List, Optional, Tuple

from colorama import Fore, init
import gensim
from gensim.corpora.dictionary import Dictionary
from gensim.models import CoherenceModel
from gensim.models.ldamodel import LdaModel
from gensim.models.phrases import FrozenPhrases
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from tqdm import tqdm

from omdenalore.natural_language_processing.preprocess_text import (
    TextPreprocessor,  # noqa: E501
)
from wordcloud import WordCloud

init()


class Coherence(Enum):
    """
    Enum containing the different coherence values that can be used to derive
    the coherence scores from an LDA model
    """

    C_V = "c_v"
    UMASS = "u_mass"


class TopicModelling:
    """
    TopicModelling is used to train an LDA model with minimal code necessary.
    """

    def __init__(
        self,
        csv_path: str,
        text_column: str,
        sample: bool = False,
        sample_size: int = 1000,
        min_count_phrases: float = 5.0,
        threshold_phrases: float = 10.0,
        model_max_length: int = 2000000,
        bins_displot: int = 100,
    ) -> None:
        """
        :param csv_path: path to the csv file to convert to a DataFrame
        :type csv_path: str
        :param text_column: name of the column in the csv that contains the
        text data
        :type text_column: str
        :param sample: whether to sample from the dataframe, useful if the file
        is quite large but just some initial quick topic modelling is required
        :type sample: bool
        :param sample_size: number of rows to use in the dataframe, applicable
        if testing out the model quickly on a small amount of data
        :type sample_size: int
        :param min_count_phrases: ignore all words and bigrams with total
        collected count lower than this value
        :type min_count_phrases: float :param threshold_phrases: represent a
        score threshold for forming the phrases (higher means fewer phrases) in
        bigrams/trigrams
        :type threshold_phrases: float
        :param model_max_length: update spaCy models max_length which is
        defaulted to 100_000, when working with large amounts of text increase
        this value
        :type model_max_length: int
        :param bins_displot: update the values used in bins for dis_plots
        :raises: ValueError

        :Example:
        >>> csv = "./abcnews-date-text.csv"
        >>> tm = TopicModelling(
        >>>     csv_path=csv,
        >>>     text_column="headline_text",
        >>>     sample=True,
        >>> )
        >>> tm.print_df()
               publish_date                                 headline_text
            0  20030219  aba decides against community broadcasting lic...
            1  20030219     act fire witnesses must be aware of defamation
            2  20030219     a g calls for infrastructure protection summit
            3  20030219           air nz staff in aust strike for pay rise
            4  20030219      air nz strike to affect australian travellers
            5  20030219                  ambitious olsson wins triple jump
            6  20030219         antic delighted with record breaking barca
            7  20030219  aussie qualifier stosur wastes four memphis match
            8  20030219       aust addresses un security council over iraq
            9  20030219         australia is locked into war timetable opp
        >>> processed_words = tm.process_words()
        >>> corpus_dict, freq_dict, id2word, bow = tm.configure_corpus(
        >>>     texts=processed_words,
        >>> )
        >>> tm.plot_freq(freq_dict, save_path="./freq.jpg")
        >>> tm.plot_top_n_frequent_words(
        >>>     freq_dict=freq_dict,
        >>> )
        >>> best_model = tm.train_lda(
        >>>     corpus=bow,
        >>>     id2word=id2word,
        >>>     texts=processed_words,
        >>> )
        >>> top_terms_per_topic = tm.get_top_terms_per_topic(
        >>>     best_model=best_model,
        >>> )
        >>> tm.plot_word_cloud(terms_per_topic_df=top_terms_per_topic)
        """
        self.csv_path = csv_path
        self.sample = sample
        self.sample_size = sample_size
        if self.sample:
            self.df = pd.read_csv(self.csv_path).sample(self.sample_size)
        else:
            self.df = pd.read_csv(self.csv_path)
        self.min_count_phrases = min_count_phrases
        self.threshold_phrases = threshold_phrases
        self.model_max_length = model_max_length
        self.bins_displot = bins_displot
        self.text_column = text_column
        if text_column not in self.df.columns:
            raise ValueError(
                Fore.RED
                + "Please pass a column name that exist in the dataframe",  # noqa: E501
            )
        self.corpus_list = self.df[self.text_column].tolist()  # type: ignore

    def print_df(self, rows: int = 10) -> None:
        """
        Prints a certain number of rows from the DataFrame
        :param rows: number of rows to print
        :type rows: int
        """
        print(self.df.head(rows))

    def process_words(self) -> List[List[str]]:
        """
        Processes the text data by removing numbers, unwanted tokens, empty
        tokens, lemmatizing, non-alphabetic characters, non-Unicode characters.
        :return: List[List[str]]
        """
        model = TextPreprocessor.load_model()
        # If the dataset is too big then modify the max_length parameter
        # from the spaCy model
        model.max_length = self.model_max_length
        preprocessor = TextPreprocessor(spacy_model=model)
        texts = preprocessor.preprocess_text_lists(self.corpus_list)
        bigram_mod, trigram_mod = self.__bigrams_trigrams(data=texts)
        texts = [bigram_mod[doc] for doc in texts]
        texts = [trigram_mod[bigram_mod[doc]] for doc in texts]
        return [["".join(text)] for text in texts]

    def configure_corpus(
        self, texts: List[List[str]]
    ) -> Tuple[
        Dict[str, int], pd.DataFrame, Dictionary, List[List[Tuple[int, int]]]
    ]:  # noqa: E501
        """
        Configures the necessary parts needed to perform Topic Modelling
        :param texts: processed text data from TopicModelling.process_words
        :type texts: List[List[str]]
        :return: Tuple containing the text corpus as a dictionary, DataFrame of
        the frequency counts for the corpus,
        gensim.corpora.dictionary.Dictionary, and bag-of-words
        """
        dict_corpus = {}
        split_text = [word.split() for sentence in texts for word in sentence]
        id2word = Dictionary(split_text)
        print(Fore.GREEN + f"Total vocabulary size: {len(id2word)}")
        bow = [id2word.doc2bow(text_) for text_ in split_text]
        for i in range(len(bow)):
            for idx, freq in bow[i]:
                if id2word[idx] in dict_corpus:
                    dict_corpus[id2word[idx]] += freq
                else:
                    dict_corpus[id2word[idx]] = freq
        corpus_freq_df = self.__dict_to_freq_df(
            dict_corpus=dict_corpus,
        )
        return dict_corpus, corpus_freq_df, id2word, bow  # type: ignore

    def plot_freq(
        self,
        freq_dict: pd.DataFrame,
        save_path: Optional[str] = None,
    ) -> None:
        """
        Plots the frequency distribution of the words in the corpus
        :param freq_dict: Frequency of the text corpus which is a DataFrame
        :type freq_dict: pd.DataFrame
        :param save_path: path to save the plot to
        """
        if "freq" not in freq_dict.columns:
            raise ValueError(
                Fore.RED + "Please pass a dataframe with a column 'freq'",
            )
        sns.displot(freq_dict["freq"], bins=self.bins_displot)
        plt.title("Frequency distribution of the words in the corpus")
        if save_path:
            plt.savefig(save_path)
        plt.show()

    def plot_top_n_frequent_words(
        self,
        freq_dict: pd.DataFrame,
        save_path: Optional[str] = None,
        n: int = 10,
    ) -> None:
        """
        Plots the top N most frequent words in the corpus
        :param freq_dict: Frequency of the text corpus which is a DataFrame
        :type freq_dict: pd.DataFrame
        :param n: the number of words to include
        :type n: int
        :param save_path: path to save the plot to
        :type save_path: str
        """
        if "freq" not in freq_dict.columns:
            raise ValueError(
                Fore.RED + "Please pass a dataframe with a column 'freq'"
            )  # noqa : E501
        top_n_words = freq_dict.sort_values(
            "freq",
            ascending=False,
        ).head(n)
        sns.barplot(x=top_n_words.index, y="freq", data=top_n_words)
        plt.xticks(rotation=90)
        plt.title(f"Top {n} most frequent words in the corpus")
        if save_path:
            plt.savefig(save_path)
        plt.show()

    def train_lda(
        self,
        corpus: List[List[Tuple[int, int]]],
        id2word: Dictionary,
        texts: List[List[str]],
        save_path: Optional[str] = None,
        num_topics: int = 20,
        coherence: Coherence = Coherence.UMASS.value,  # type: ignore
        plot_coherence_score: bool = True,
        **kwargs,
    ) -> CoherenceModel:
        """
        Trains a LDA model on the text data provided with the elbow method
        applied to find the best number of topics
        :param corpus: corpus in BoW format
        :type corpus: List[List[Tuple[int, int]]]
        :param id2word: Gensim dictionary mapping of id word to create corpus
        :type gensim.corpora.dictionary.Dictionary
        :param texts: preprocessed text
        :type texts: List[List[str]]
        :param save_path: path to save the plot to
        :type save_path: str
        :param num_topics: the range of topics to find the best model
        :type num_topics: int
        :param coherence: type of coherence value to use when determining the
        coherence score
        :type coherence: Coherence
        :param plot_coherence_score: plot the coherence scores or not
        :type plot_coherence_score: bool
        :return: best model found
        """
        if coherence == Coherence.C_V.value:
            print(
                Fore.RED
                + "Use of c_v for the coherence value might result in NaN coherence scores due to issues with Gensim that will be fixed in a future update"  # noqa: E501
            )
        (
            coherence_scores,
            _,
            best_model,
            best_model_coherence_score,
        ) = self.__train_lda_elbow(
            corpus=corpus,
            id2word=id2word,
            texts=texts,
            num_topics=num_topics,
            coherence=coherence,
            **kwargs,
        )
        print(Fore.GREEN + f"Coherence scores: {coherence_scores}")
        print(
            Fore.GREEN
            + f"Best model coherence score : {best_model_coherence_score}"  # noqa: E501
        )
        if plot_coherence_score:
            self.__plot_coherence_scores(
                coherence_scores=coherence_scores,
                coherence=coherence,
                num_topics=num_topics,
                save_path=save_path,
            )
        return best_model

    def display_topics(self, lda: LdaModel) -> None:
        """
        Prints the topics in the LDA model
        :param lda: LdaModel to view the topics
        :type lda: LdaModel
        """
        if isinstance(lda, LdaModel):
            pprint(Fore.GREEN + lda.show_topics(formatted=False))

    def __bigrams_trigrams(
        self,
        data: List[List[str]],
    ) -> Tuple[FrozenPhrases, FrozenPhrases]:
        """
        Extract common phrases from a corpus using Gensims Phraser class
        :param data: preprocessed text data
        :type data: List[List[str]]
        :return: tuple containing the bigram_mod and trigram_mod
        """
        bigram = gensim.models.Phrases(
            data,
            min_count=self.min_count_phrases,
            threshold=self.threshold_phrases,
        )
        trigram = gensim.models.Phrases(
            bigram[data],
            threshold=self.threshold_phrases,
        )
        bigram_mod = gensim.models.phrases.Phraser(bigram)
        trigram_mod = gensim.models.phrases.Phraser(trigram)
        return bigram_mod, trigram_mod

    def __train_lda_elbow(
        self,
        corpus: List[List[Tuple[int, int]]],
        id2word: Dictionary,
        texts: List[List[str]],
        num_topics: int,
        coherence: Coherence,
        **kwargs,
    ) -> Tuple[List[float], List[CoherenceModel], CoherenceModel, float]:
        """
        Trains an LDA model using the elbow method where a model with 1 to
        num_topics is trained to find the best num_topics to use
        :param corpus: Gensim corpus
        :type corpus: List[List[Tuple[int,int]]]
        :param id2word: Gensim Dictionary
        :type id2word: gensim.corpora.dictionary.Dictionary
        :param texts: preprocessed text data
        :type texts: List[List[str]]
        :param num_topics: the number of topics to try up until
        :type num_topics: int
        :param coherence: Coherence enum
        :type coherence: Coherence
        :return: tuple containing the list of coherence_scores, list of the
        models, and the best model based on the coherence_value set

        """
        coherence_scores = []
        model_list = []
        for topics in tqdm(
            range(1, num_topics + 1),
            desc="Finding the best model",
        ):
            lda = LdaModel(
                corpus=corpus,
                num_topics=topics,
                id2word=id2word,
                **kwargs,
            )
            model_list.append(lda)
            # c_v coherence values not working LOL
            if coherence == Coherence.C_V.value:
                coherence_lda = CoherenceModel(
                    model=lda,
                    texts=texts,
                    coherence=Coherence.C_V.value,
                    **kwargs,
                )
            elif coherence == Coherence.UMASS.value:
                coherence_lda = CoherenceModel(
                    model=lda,
                    corpus=corpus,
                    coherence=Coherence.UMASS.value,
                    **kwargs,
                )
            coherence_score = coherence_lda.get_coherence()
            if np.isnan(coherence_score):
                raise ValueError(
                    Fore.RED
                    + "There were NaN values in the coherence_scores, training aborted!"  # noqa: E501
                )
            coherence_scores.append(coherence_score)
        best_model, best_model_coherence_score = self.__get_best_model(
            coherence=coherence,
            coherence_scores=coherence_scores,
            model_list=model_list,
        )
        return (
            coherence_scores,
            model_list,
            best_model,
            best_model_coherence_score,
        )

    def __dict_to_freq_df(
        self,
        dict_corpus: Dict[str, int],
    ) -> pd.DataFrame:
        """
        Converts the text corpus in the form of a dictionary to a DataFrame for
        easy plotting
        :param dict_corpus: text corpus in the form of a dictionary
        :type dict_corpus: Dict[str,int]
        :return: Pandas DataFrame
        """
        return pd.DataFrame.from_dict(
            dict_corpus,
            orient="index",
            columns=["freq"],
        )

    def __get_best_model(
        self,
        coherence: Coherence,
        coherence_scores: List[float],
        model_list: List[CoherenceModel],
    ) -> Tuple[CoherenceModel, float]:
        """
        Finds the best model based on the coherence value selected.
        Currently supports use of c_v and u_mass.
        For faster results at the expense of less accurate score use u_mass.
        For slower results with a more accurate score use c_v.
        :param coherence: Coherence enum value
        :type coherence: Coherence
        :param coherence_scores: the list of coherence scores that are obtained
        from __train_lda_elbow()
        :type coherence_scores: List[float]
        :param model_list: the list of coherence models that are obtained from
        __train_lda_elbow()
        :type model_list: List[CoherenceModel]
        :return: the best coherence model
        """
        if coherence == Coherence.C_V.value:
            # Coherence scores returned by c_v coherence type exist in the
            # range 0 to 1 and the model with the score closer to 1 is the
            # best one
            best_model_idx = self.__take_closest_idx(
                input_list=coherence_scores,
                closest_to=1.0,
            )
            best_model = model_list[best_model_idx]
            best_model_coherence_score = coherence_scores[best_model_idx]
            return best_model, best_model_coherence_score

        elif coherence == Coherence.UMASS.value:
            # Coherence scores returned by u_mass coherence type exist in
            # the log scale and the best model is defined as the one with
            # a more negative value or the minimum value
            best_model_idx = coherence_scores.index(
                min(coherence_scores),
            )
            best_model = model_list[best_model_idx]
            best_model_coherence_score = coherence_scores[best_model_idx]
            return best_model, best_model_coherence_score

    def __take_closest_idx(
        self,
        input_list: List[float],
        closest_to: float,
    ) -> int:
        """
        Finds the index of the value in a list that is the closest to a certain
        value
        :param input_list: list of floats to find the closest value to a
        certain value
        :type input_list: List[float]
        :param closest_to: the value used to find the closest value to it
        :type closest_to: float
        :return: the index of the closest value to the argument closest_to
        """
        index = input_list.index(
            min(
                input_list,
                key=lambda x: abs(x - closest_to),
            )
        )
        return index

    def __plot_coherence_scores(
        self,
        coherence_scores: List[float],
        coherence: Coherence,
        save_path: Optional[str] = None,
        num_topics: int = 20,
    ) -> None:
        """
        Plots the coherence scores as they change depending on the number of
        topics used
        :param coherence_scores: list of the coherence scores
        :type coherence_scores: List[float]
        :param num_topics: the maximum number of topics used to train the LDA
        model
        :type: int
        """
        x = range(1, num_topics + 1)
        plt.plot(x, coherence_scores)
        plt.xlabel("Num Topics")
        plt.ylabel("Coherence score")
        plt.legend(("coherence_scores"), loc="best")
        plt.title(
            f"Plot of the best models coherence scores based on {coherence}",
        )
        if save_path:
            plt.savefig(save_path)
        plt.show()

    def __get_topics(self, best_model: LdaModel):
        """
        Gets the top 20 topics from the LdaModel
        :param best_model: the best LdaModel
        :type best_model: LdaModel
        """
        topics = [
            [
                (
                    term,
                    round(
                        wt,
                        3,
                    ),
                )
                for term, wt in best_model.show_topic(
                    n,
                    topn=20,
                )
            ]
            for n in range(0, best_model.num_topics)
        ]
        return topics

    def get_top_terms_per_topic(self, best_model: LdaModel) -> pd.DataFrame:
        """
        Get the top terms per a topic
        :param best_model: the best LdaModel
        :type best_model: LdaModel
        """
        topics = self.__get_topics(
            best_model=best_model,
        )
        top_terms_per_topic_df = pd.DataFrame(
            [", ".join([term for term, _ in topic]) for topic in topics],
            columns=["Terms per Topic"],
            index=[
                "Topic" + str(i)
                for i in range(
                    1,
                    best_model.num_topics + 1,
                )
            ],
        )
        return top_terms_per_topic_df

    def plot_word_cloud(
        self,
        terms_per_topic_df: pd.DataFrame,
        save_path: Optional[str] = None,
    ) -> None:
        """
        Plots the word cloud of the top terms in a topic
        :param terms_per_topic_df: DataFrame of the top terms per a topic
        :type terms_per_topic_df: pd.DataFrame
        :param save_path: path to save the plot
        :type save_path: str
        """
        wc = WordCloud(
            background_color="white",
            colormap="CMRmap",
            max_font_size=150,
            random_state=42,
        )
        plt.rcParams["figure.figsize"] = [20, 15]
        for i in range(len(terms_per_topic_df.index)):

            wc.generate(
                text=terms_per_topic_df["Terms per Topic"][i],
            )

            plt.subplot(5, 4, i + 1)
            plt.imshow(wc, interpolation="bilinear")
            plt.axis("off")
            plt.title(terms_per_topic_df.index[i])
        if save_path:
            plt.savefig(save_path)
        plt.show()
