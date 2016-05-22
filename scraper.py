from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from lxml import html
from urllib.request import urlopen
import os
import re

link = "https://scn.wiktionary.org/w/index.php?title=Catigur%C3%ACa:Verbi_siciliani&pagefrom=attargiari#mw-pages"
response = requests.get(link)
parsed_body = html.fromstring(response.text)
italian = parsed_body.xpath('//ul/li/a/@href')
for i in range(0, 200):
    url = "https://scn.wiktionary.org" + italian[i]
    response = requests.get(url)
    parsed = html.fromstring(response.text)
    x = parsed.xpath("//ul/li/a/text()")
    y = parsed.xpath("//dl/dd/a/text()")
    if y:
        for ye in y:
            x.append(ye)
    verb = italian[i].split("i/")[1]
    verb = verb.replace("%C3%AC", "ì")
    verb = verb.replace("%C3%B2", "ò")
    verb = verb.replace("%C3%A0", "à")
    verb = verb.replace("%C3%A8", "è")
    verb = verb.replace("%C3%B9", "ù")
    print(verb, x)