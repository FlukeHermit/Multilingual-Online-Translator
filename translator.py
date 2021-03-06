from requests import Session
from bs4 import BeautifulSoup
import argparse
import sys  # first, we import the module


args = sys.argv  # we get the list of arguments


session = Session()

languages = ["All",
             "Arabic",
             "German",
             "English",
             "Spanish",
             "French",
             "Hebrew",
             "Japanese",
             "Dutch",
             "Polish",
             "Portuguese",
             "Romanian",
             "Russian",
             "Turkish"]


def to_lang(word, lang_in, lang_out):
    url = f"https://context.reverso.net/translation/{lang_in.lower()}-{lang_out.lower()}/{word}"

    r = session.get(url, headers={'user-agent': 'Mozilla/5.0'})

    if r.status_code == 404:
        output = f"Sorry, unable to find {word}"
    elif not r:
        output='Something wrong with your internet connection'
    # created a parse for the page
    else:
        soup = BeautifulSoup(r.content, 'html.parser')

        translations = [i.text.strip()
                        for i in soup.find_all("a", {'class': 'translation'})][1::]

        src_examples = [i.text.strip()
                        for i in soup.find_all("div", {'class': 'src ltr'})]

        trg_examples = [i.text.strip()
                        for i in soup.find_all("div", {'class': ['trg ltr', 'trg rtl arabic', 'trg rtl']})]

        output = ""

        output += f"{lang_out.title()} Translations:\n"

        output += "\n".join(translations[:1])
        output += "\n"
        output += f"\n{lang_out.title()} Example:\n"

        for src, trg in zip(src_examples[:1], trg_examples[:1]):
            output += src+":\n"+trg+"\n"

        output += "\n\n"

    return output


src_lang = args[1]
trg_lang = args[2]
word = args[3]

if src_lang.title() not in languages:
    print(f"Sorry, the program doesn't support {src_lang}")
elif trg_lang.title() not in languages:
    print(f"Sorry, the program doesn't support {trg_lang}")

elif trg_lang == "all":
    output = ""
    for language in languages:
        if language != src_lang:
            output += to_lang(word, src_lang, language)
    print(output)
    with open(f'{word}.txt', 'w', encoding="utf-8") as file:
        file.write(output)

else:
    output = to_lang(word, src_lang, trg_lang)
    print(output)
    with open(f'{word}.txt', 'w', encoding="utf-8") as file:
        file.write(output)
