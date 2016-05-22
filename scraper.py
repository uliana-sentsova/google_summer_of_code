from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from lxml import html
from urllib.request import urlopen
import os
import re

count = 0
with open("sicilian_verbs.txt", "w") as verbs_file, open("translation.txt", "w") as translation_file:
    next_link = "https://scn.wiktionary.org/w/index.php?title=Catigur%C3%ACa:Verbi_siciliani&pageuntil=acc%C3%B2gliri#mw-pages"
    while next_link:

        previous_link = next_link

        response = requests.get(next_link)
        parsed_body = html.fromstring(response.text)

        # Looking for verbs on the page
        sicilian = parsed_body.xpath('//ul/li/a/@href')
        for i in range(0, 200):
            url = "https://scn.wiktionary.org" + sicilian[i]
            response = requests.get(url)
            parsed = html.fromstring(response.text)
            first_section = parsed.xpath("//ul/li/a/text()")
            second_section = parsed.xpath("//dl/dd/a/text()")
            if second_section:
                for part in second_section:
                    first_section.append(part)
            verb = sicilian[i].split("i/")[1].strip()
            verb = verb.replace("%C3%AC", "ì")
            verb = verb.replace("%C3%B2", "ò")
            verb = verb.replace("%C3%A0", "à")
            verb = verb.replace("%C3%A8", "è")
            verb = verb.replace("%C3%B9", "ù")
            # print(verb, first_section)
            verbs_file.write(verb + "\n")
            translation_file.write(verb + "\t" + ",".join(first_section) + "\n")
            count += 1
            if count%50 == 0:
                print(count, "verbs extracted.")


        # Looking for a next page:
        potential = parsed_body.xpath('//div/a/@href')
        potential = list(set(potential))
        for link in potential:
            if "pagefrom" in link:
                next_link =  "https://scn.wiktionary.org" + link
        print(next_link)
        print("NEXT PAGE")
        if next_link == previous_link:
            break