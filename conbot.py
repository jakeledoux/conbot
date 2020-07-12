""" Library for loading and interacting with Microsoft Personality Chat
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
from typing import Dict


class ConBot(object):
    """ Handles bot personality and responses.
    """

    def __init__(self, personality_file, fallback_messages=None):
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
        """ Load .tsv conversation dataset as dict.
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
    import os

    kayla = ConBot(os.path.join('personalities', 'qna_chitchat_friendly.tsv'))

    query = ''
    while query.strip().lower() not in ('quit', 'exit', 'bye', 'goodbye'):
        query = input('> ')
        response = kayla.get_response(query)
        print(response)
