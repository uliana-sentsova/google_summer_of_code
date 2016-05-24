import requests
from lxml import html

count = 0
with open("nouns_list_2.txt", "a") as nouns_file, open("nouns_translations.txt", "a") as translation_file:

    next_link = "https://scn.wiktionary.org/w/index.php?title=Catigur%C3%ACa:Sustantivi_siciliani&pagefrom=palpitazzioni&subcatfrom=A&filefrom=A#mw-pages"

    while next_link:

        try:

            previous_link = next_link

            response = requests.get(next_link)
            parsed_body = html.fromstring(response.text)

            # Find words on the page
            sicilian = parsed_body.xpath('//ul/li/a/@href')
            for i in range(0, 200):
                url = "https://scn.wiktionary.org" + sicilian[i]
                response = requests.get(url)
                parsed = html.fromstring(response.text)
                first_section = parsed.xpath("//ul/li/a/text()")
                second_section = parsed.xpath("//dl/dd/a/text()")
                grammar = parsed.xpath("//div/p/i/text()")
                if second_section:
                    for part in second_section:
                        first_section.append(part)
                for s in first_section:
                    grammar.append(s)
                word = sicilian[i].split("i/")[1].strip()

                # if not word.endswith("ri") or word.endswith("si"):
                #     continue

                # Replace UTF
                word = word.replace("%C3%AC", "ì")
                word = word.replace("%C3%B2", "ò")
                word = word.replace("%C3%A0", "à")
                word = word.replace("%C3%A8", "è")
                word = word.replace("%C3%B9", "ù")
                word = word.replace("%C3%A7", "ç")
                word = word.replace("%C3%AE", "î")

                # print(word)

                nouns_file.write(word + "\n")
                translation_file.write(word + "\t" + ",".join(grammar) + "\n")
                count += 1
                if count%50 == 0:
                    print(count, "Words extracted. Last word:", word)

            # Look for the next page:
            hrefs_list = parsed_body.xpath('//div/a/@href')
            hrefs_list = list(set(hrefs_list))
            for link in hrefs_list:
                if "pagefrom" in link:
                    next_link = "https://scn.wiktionary.org" + link

            print(next_link)
            print("NEXT PAGE")

            # If there is no next page, break
            if next_link == previous_link:
                break

        # It is a terrible exception handler, but still, I need it.
        except Exception as err:
            print(err)
            pass