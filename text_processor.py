from file_reader import raw_read
from random import shuffle, randint
from urllib.request import urlopen
from urllib.error import HTTPError
from math import ceil
import re


def is_a_vowel(l) -> bool:
    return (
        (l == "A" or l == "a")
        or (l == "O" or l == "o")
        or (l == "I" or l == "i")
        or (l == "E" or l == "e")
        or (l == "U" or l == "u")
        or (l == "ʌ")
    )


def starts_with_a_vowel(word) -> bool:
    f = 0
    if word == "":
        return False
    elif word[0] == "/":
        f = 1
    l = word[f]  # l stands for letter
    if (l == "U" or l == "u") or (l == "h" or l == "H"):
        url = "https://www.dictionary.com/browse/" + word[f:]
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        sound_id = html.find(
            '<span class="LgvbRZvyfgILDYMd8Lq6" data-type="pronunciation-text">'
        )  # first sound is on +68 position
        html_cut = html[sound_id : sound_id + 175]
        pronunciation_string = re.sub("<.*?>", "", html_cut)
        try:
            return is_a_vowel(pronunciation_string[2])
        except IndexError as index:
            print(f"No word found: {index}")
            try:
                sound_id = html.find('<span class="pron">')
                html_cut = html[sound_id : sound_id + 35]
                pronunciation_string = re.sub("<.*?>", "", html_cut)
                return is_a_vowel(pronunciation_string[0])
            except IndexError as index:
                print(f"No word transcription found: {index}")
            except Exception as e:
                print(f"Other error occurred: {e}")
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as e:
            print(f"Other error occurred: {e}")
    else:
        return is_a_vowel(word[f])


def article_corrector(words) -> list:
    for i in range(len(words)):
        if words[i] == "a" and starts_with_a_vowel(words[i + 1]):
            words[i] = "an"
        elif words[i] == "an" and not starts_with_a_vowel(words[i + 1]):
            words[i] = "a"
    return words


def memory_shuffle(words: list, epithets, places) -> str:
    global generation
    forget()
    shuffle(places)
    for i in range(len(places)):
        words[places[i]] = epithets[i]
    # -----This part is to stop words from doubling, after shuffling-----#
    new_string = [words[0]]
    for i in range(1, len(words)):
        if words[i] != words[i - 1][1:] and words[i][1:] != words[i - 1]:
            new_string.append(words[i])
    words = new_string.copy()
    # -------------------------------------------------------------------#
    words = check_ands(words)
    words = article_corrector(words)
    generation += 1
    return words


def join(given_list, separator) -> str:
    joined_list = ""
    for i in given_list:
        if i == ".":
            joined_list += i
        else:
            joined_list += i + separator
    return joined_list


def make_up(text: str) -> str:
    text = text.replace("/", "")
    text = text.replace(" .", ". ")
    text = text.replace("  ", " ")
    return text


words = []
epithets = []
epithets_places = []
sentences = []
ands_places = []
generation = 0
filename = ""

for line in raw_read(filename):
    line = line.replace(".", " .")
    words.extend(line.split())

for i in range(len(words)):
    if words[i].startswith("/"):
        epithets.append(words[i])
        epithets_places.append(i)

for i in range(len(words)):
    if words[i] == "and" and words[i - 1][0] == "/" and words[i + 1][0] == "/":
        ands_places.append(i)


def get_final_text() -> str:
    final_text = make_up(join(memory_shuffle(words, epithets, epithets_places), " "))
    return final_text


def get_raw_text() -> str:
    return raw_read(filename, mode="pure_raw")


def get_highlighted_text(text: str) -> str:
    for i in epithets:
        text = text.replace(" " + i[1:], " " + i)
    return text


def save_epithets():
    epithets_file = open("epithets.txt", "w")
    for i in epithets:
        epithets_file.write(i)
    for i in epithets_places:
        epithets_file.write(str(i))
    epithets_file.close()


def separate(text: str) -> list:
    global sentences
    sent_end = text.find(".")
    while len(text) > sent_end + 3:
        sent_end = text.find(".")
        if text[sent_end + 1].isspace() and (
            text[sent_end + 2].isupper() or text[sent_end + 2].isnumeric()
        ):
            sentences.append(text[: sent_end + 1])
            text = text[sent_end + 1 :].strip()
            print(text)


def forget():
    global epithets, epithets_places, ands_places, words
    chance = randint(0, 10) + (generation / 10)
    if chance > 7:
        for j in range(ceil(chance / 10)):
            i = randint(0, len(epithets) - 1)
            pos = epithets_places[i]
            epithets[i] = ""


def check_ands(words: list) -> list:
    global ands_places
    for i in range(len(ands_places)):
        check = words[ands_places[i]]
        while check != "and":
            for j in range(3):
                if words[ands_places[i] + j] == "and":
                    ands_places[i] += j
                    check = words[ands_places[i]]
                elif words[ands_places[i] - j] == "and":
                    ands_places[i] -= j
                    check = words[ands_places[i]]
        if words[ands_places[i] + 1] == "" or words[ands_places[i] - 1] == "":
            words[ands_places[i]] = ""
        elif (
            words[ands_places[i] + 1][0] == "/" and words[ands_places[i] - 1][0] == "/"
        ):
            words[ands_places[i]] = "and"
        else:
            words[ands_places[i]] = ""
    return words


def get_generation():
    return generation


def get_epithets_amount():
    return len(epithets) - epithets.count("")
