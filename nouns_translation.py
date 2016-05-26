mm = '      <e><p><l>SICILIAN<s n="n"/><s n="m"/></l><r>SPANISH<s n="n"/><s n="m"/></r></p></e>'
mf = '      <e><p><l>SICILIAN<s n="n"/><s n="m"/></l><r>SPANISH<s n="n"/><s n="f"/></r></p></e>'
fm = '      <e><p><l>SICILIAN<s n="n"/><s n="f"/></l><r>SPANISH<s n="n"/><s n="m"/></r></p></e>'
ff = '      <e><p><l>SICILIAN<s n="n"/><s n="f"/></l><r>SPANISH<s n="n"/><s n="f"/></r></p></e>'


nouns = []
with open("nouns_to_translate.txt", 'r', encoding="utf-8") as nouns_file:
    for noun in nouns_file:
        noun = noun.strip()
        nouns.append(noun)

nouns = list(set(nouns))

entries = []
unmatched = []
with open("nouns_translations.txt", 'r', encoding="utf-8") as translations:
    for line in translations:
        line = line.split("\t")
        noun = line[0].strip()
        translation = line[1].strip().split(",")
        grammar = translation[:3]
        if noun in nouns:
            # print(noun, translation)

            ita_ind = translation.index("talianu")
            italian = translation[ita_ind + 1]
            # print(noun, italian)

            other_languages = ["francisi", "purtughisi", "nurviggisi", "polaccu", "maltisi", "afrikaans", "svidisi", "catalanu", "spagnolu", "tudiscu", "asturianu", "aragunisi", "chickasaw","ngrisi", "francupruvinzali", "còrsu", "occitanu", "calabbrisi centru-miridiunali", "*", 'Palori n sicilianu']
            try:
                spa_index = translation.index("spagnolu")
                ind = spa_index + 1
                spanish = []
                while True:
                    try:
                        if translation[ind] in other_languages:
                            ind += 1
                            break
                        else:
                            spanish.append(translation[ind])
                            ind += 1
                    except IndexError:
                        break
            except ValueError:
                pass
            if spanish:
                if len(spanish) == 1 and len(spanish[0].split()) == 1:
                    spanish = spanish[0]
                    if "f" in grammar:
                        if (spanish.endswith("a") or spanish.endswith("ión") or spanish.endswith("ad") or
                                spanish.endswith("én") or spanish.endswith("ez")):
                            entry = ff.replace("SICILIAN", noun)
                            entry = entry.replace("SPANISH", spanish)
                            # entries.append(entry)
                        else:
                            if not spanish.endswith("s"):
                                entry = fm.replace("SICILIAN", noun)
                                entry = entry.replace("SPANISH", spanish)
                                # entries.append(entry)
                            else:
                                unmatched.append((noun, spanish))
                    else:
                        if (spanish.endswith("a") or spanish.endswith("ión") or spanish.endswith("ad") or
                                spanish.endswith("én") or spanish.endswith("ez")):
                            entry = mf.replace("SICILIAN", noun)
                            entry = entry.replace("SPANISH", spanish)
                            # entries.append(entry)
                        else:
                            if not spanish.endswith("s"):
                                entry = mm.replace("SICILIAN", noun)
                                entry = entry.replace("SPANISH", spanish)
                                # entries.append(entry)
                            else:
                                unmatched.append((noun, spanish))
                else:
                    if type(spanish) == str:
                        spanish = [spanish]
                    if len(spanish[0].split()) == 1:
                        spanish = spanish[0]
                        if "f" in grammar:
                            if (spanish.endswith("a") or spanish.endswith("ión") or spanish.endswith("ad") or
                                    spanish.endswith("én") or spanish.endswith("ez")):
                                entry = ff.replace("SICILIAN", noun)
                                entry = entry.replace("SPANISH", spanish)
                                # entries.append(entry)
                            else:
                                if not spanish.endswith("s"):
                                    entry = fm.replace("SICILIAN", noun)
                                    entry = entry.replace("SPANISH", spanish)
                                    # entries.append(entry)
                                else:
                                    unmatched.append((noun, spanish))
                        else:
                            if (spanish.endswith("a") or spanish.endswith("ión") or spanish.endswith("ad") or
                                    spanish.endswith("én") or spanish.endswith("ez")):
                                entry = mf.replace("SICILIAN", noun)
                                entry = entry.replace("SPANISH", spanish)
                                # entries.append(entry)
                            else:
                                if not spanish.endswith("s"):
                                    entry = mm.replace("SICILIAN", noun)
                                    entry = entry.replace("SPANISH", spanish)
                                    # entries.append(entry)
                                else:
                                    unmatched.append((noun, spanish))
            else:
                # print(noun, italian)
                if len(italian.split(" ")) == 1:
                    if "f" in grammar:
                        entry = fm.replace("SICILIAN", noun)
                        # print(entry, italian)
                else:
                    print(noun, '-',  italian)



# entries = sorted(list(set(entries)))
# for e in entries:
#     print(e)
#
# print("--------")
#
# for u in unmatched:
#     print(u)
