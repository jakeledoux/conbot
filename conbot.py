""" ConBot (Jake Ledoux, 2020)

    Library for loading and interacting with Microsoft Personality Chat
    datasets in TSV form.

    You can find those here:
    https://github.com/microsoft/BotBuilder-PersonalityChat

    You can also write your own datasets. Just write a file where each line
    starts with a prompt, then a tab, then the response. You can add further
    information separated by another tab since this code ignores everything
    after the first two columns.
"""
from fuzzywuzzy import process as fwproc
import random
from typing import Dict, Tuple, Union


class ConBot(object):
    """ Handles bot personality and responses.

        :param personality_file: Filename of TSV Question/Answer file.
        :param fallback_messages: Tuple of messages to choose from and
            return when a response doesn't meet the confidence threshold.
    """

    def __init__(self, personality_file: str,
                 fallback_messages: Union[Tuple[str, ...], None] = None):
        """ Constructor method
        """
        self.dataset = ConBot.load_personality(personality_file)
        if fallback_messages:
            self.fallback_messages = fallback_messages
        else:
            self.fallback_messages = ("Sorry, I didn't understand that.",
                                      "Could you rephrase that?",
                                      "I'm not sure what you mean.")

    def get_response(self, query: str, threshold=90, debug=False) -> str:
        """ Returns a message in response to `query` using the personality
            dataset loaded.

            :param query: The message for the bot to respond to.
            :param threshold: The confidence value in percents (0-100) that a
                response must meet or exceed in order to be displayed.
            :param debug: If True, the best match and its confidence value will
                be printed in addition to normal operation.

            :returns: The response string.
        """
        selection, confidence = fwproc.extractOne(query, self.dataset.keys())
        if debug:
            print(f'Best match: {selection} (Confidence: {confidence})')
        if confidence >= threshold:
            return self.dataset.get(selection)
        else:
            return random.choice(self.fallback_messages)

    @staticmethod
    def load_personality(filename: str) -> Dict[str, str]:
        """ Parse .tsv conversation dataset into dictionary.

            :param filename: Filename of TSV Question/Answer file.

            :returns: Dictionary with {Question: Answer} structure.
        """
        with open(filename, 'r', encoding='utf-8') as f:
            contents = f.read()

        temp_dataset = dict()
        for line in contents.splitlines():
            if line:
                if not line.startswith('Question\tAnswer'):
                    question, answer, *_ = line.split('\t')
                    temp_dataset[question.strip()] = answer.strip()

        return temp_dataset


if __name__ == '__main__':
    """ A little interactive demo with one of the default personalities.
    """
    import os

    kayla = ConBot(os.path.join('personalities', 'qna_chitchat_friendly.tsv'))

    query = ''
    while query.strip().lower() not in ('quit', 'exit', 'bye', 'goodbye'):
        query = input('> ')
        response = kayla.get_response(query)
        print(response)
