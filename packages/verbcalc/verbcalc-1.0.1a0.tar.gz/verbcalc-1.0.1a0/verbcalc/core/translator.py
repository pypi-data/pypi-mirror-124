"""
Translator module allows to change natural language to mathematical notation.
"""


class Translator:
    """
    Allows to translate words that mean mathematical actions into their symbols
    ('plus' will become '+',
    'minus' will become '-', etc).
    """

    def __init__(self):
        self._additions = ['plus']

    def _translate_additions(self, sentence: str) -> str:
        result = ''
        buffer = sentence.split()

        for word in buffer:
            if word in self._additions:
                new_word = ' + '
            else:
                new_word = word

            result += new_word

        return result

    def translate(self, sentence: str) -> str:
        """
          Translates maths related words into their symbols.

          Args:
              sentence: Sentence to be converted.

          Returns:
              Converted sentence.

          """
        sentence_lowered = sentence.lower()
        return self._translate_additions(sentence_lowered)
