from urllib.request import urlopen
import re


class Epythet:
    word = ""
    uses_an = False

    def is_a_vowel(l) -> bool:
        if (
            (l == "A" or l == "a")
            or (l == "O" or l == "o")
            or (l == "I" or l == "i")
            or (l == "E" or l == "e")
            or (l == "U" or l == "u")
        ):
            return True

    def __init__(self, word: str):
        self.word = word
        f = 0
        if word[0] == "/":
            f = 1
        l = word[f]  # l stands for letter
        if (
            (l == "A" or l == "a")
            or (l == "O" or l == "o")
            or (l == "I" or l == "i")
            or (l == "E" or l == "e")
        ):
            self.uses_an = True
        elif not self.is_a_vowel(l):
            self.uses_an = False
        elif (l == "U" or l == "u") or (l == "h" or l == "H"):
            url = "https://www.dictionary.com/browse/" + word[f:]
            page = urlopen(url)
            html_bytes = page.read()
            html = html_bytes.decode("utf-8")
            sound_id = html.find(
                '<span class="LgvbRZvyfgILDYMd8Lq6" data-type="pronunciation-text">'
            )  # first sound is on +68 position
            html_cut = html[sound_id : sound_id + 175]
            pronunciation_string = re.sub("<.*?>", "", html_cut)
            print(pronunciation_string)
            self.uses_an = self.is_a_vowel(pronunciation_string[2])
        else:
            self.uses_an = False

    def get(self):
        return self.word

    def does_use_an(self):
        return self.uses_an
