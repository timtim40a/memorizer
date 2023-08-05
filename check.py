from urllib.request import urlopen
import re

f = open("epithets.txt", "r")

epithets = f.readline().split("/")
epithets[0] = "default"
for word in epithets:
    url = "https://www.dictionary.com/browse/" + word
    print(url)
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    sound_id = html.find(
        '<span class="LgvbRZvyfgILDYMd8Lq6" data-type="pronunciation-text">'
    )  # first sound is on +68 position
    html_cut = html[sound_id : sound_id + 175]
    try:
        pronunciation_string = re.sub("<.*?>", "", html_cut)
        print(pronunciation_string)
    except HTTPError as http_err:
        print("#################################")


f.close()
