import re
from typing import Dict, Optional


class TextUtils:
    """Utility functions for handling text data"""

    @staticmethod
    def noise_removal(
        input_text: str, noise_list=["is", "a", "this", "the", "an"]
    ) -> str:
        """
        Remove noise from the input text.
        This function can be use to remove common english
        words like "is, a , the".
        You can add your own noise words in the optional
        parameters "noise_list"
        default noise_list = ["is", "a", "this", "the" , "an"]

        :param input_text: Input text to remove noise from
        :type input_text: str
        :param noise_list: (Optional) List of words that you
        want to remove from the input text
        :type noise_list: list
        :returns: Clean text with no noise

        :Example:

        from omdenalore.natural_language_processing.utils import
        TextUtils
        >>> input = "Hello, the chicken crossed the street"
        >>> TextUtils.noise_removal(input)
        "Hello, chicken crossed the street"
        """

        words = input_text.split()
        noise_free_words = [word for word in words if word not in noise_list]
        noise_free_text = " ".join(noise_free_words)
        return noise_free_text

    @staticmethod
    def remove_regex_pattern(input_text: str, regex_pattern: str) -> str:
        """
        Remove any regular expressions from the input text

        :param input_text: Input text to remove regex from
        :type input_text: str
        :param noise_list: string of regex that you want to
        remove from the input text
        :type noise_list: string
        :returns: Clean text with removed regex

        :Example:

        from omdenalore.natural_language_processing.utils import
        remove_regex_pattern

        >>> regex_pattern = r"#[\\w]*"
        >>> input = "remove this #hastag"
        >>> TextUtils.remove_regex_pattern(input, regex_pattern)
        "remove this  hastag"
        """

        urls = re.finditer(regex_pattern, input_text)
        for i in urls:
            input_text = re.sub(i.group().strip(), "", input_text)

        return input_text

    @staticmethod
    def remove_hashtags(text: str) -> str:
        """
        Removing hastags from the input text
        :param text: Input text to remove hastags from
        :type input_text: str
        :returns: output text without hastags

        :Example:

        from omdenalore.natural_language_processing.utls import
        TextUtils
        >>> TextUtils.remove_hashtags("I love #hashtags")
        "I love "
        """
        return TextUtils.remove_regex_pattern(text, r"(#\w+)")

    @staticmethod
    def remove_url(text: str) -> str:
        """
        Removing urls from the input text
        :param text: Input text to remove urls from
        :type input_text: str
        :returns: text with standard words

        :Example:

        from omdenalore.natural_language_processing.utisl import
        TextUtils
        >>> TextUtils.remove_url('I like urls http://www.google.com')
        'I like urls '
        """
        return TextUtils.remove_regex_pattern(text, r"(#\w+)")

    @staticmethod
    def standardize_words(
        input_text: str,
        lookup_dictionary: Dict[str, str],
    ) -> Optional[str]:
        """
        Replace acronyms, hastags, colloquial slangs etc with standard words

        Text data often contains words or phrases which are not present in
        any standard lexical dictionaries.
        These pieces are not recognized by search engines and models.

        :param input_text: Input text to remove regex from
        :type input_text: str
        :param lookup_dictionary: Dictionary with slang as index and
        standard word as item or value
        :type lookup_dictionary: dict
        :returns: text with standard words

        :Example:

        from omdenalore.natural_language_processing.utils import
        TextUtils
        >>> lookup_dict = {'rt':'Retweet', 'dm':'direct message',
        "awsm" : "awesome", "luv" :"love"}
        >>> TextUtils.standardize_words("rt I luv to dm, it's awsm")
        Retweet I love to direct message, it's awesome
        """
        words = input_text.split()
        new_words = []
        new_text = None
        for word in words:
            if word.lower() in lookup_dictionary:
                word = lookup_dictionary[word.lower()]
            new_words.append(word)
            new_text = " ".join(new_words)
        return new_text
