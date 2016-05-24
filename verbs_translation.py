from Levenshtein import distance
entry = '      <e><p><l>SICILIAN<s n="vblex"/></l><r>SPANISH<s n="vblex"/></r></p></e>'


def build_paradigm(sicilian, spanish):
    line = entry.replace("SICILIAN", sicilian)
    line = line.replace("SPANISH", spanish)
    return line


freq_dictionary = dict()

with open("scn.crp.txt", 'r', encoding="utf-8") as corpus:
    for line in corpus:
        line = line.strip()
        line = line.split(" ")
        for word in line:
            if word.startswith("s'"):
                word = word[2:]
            word = word.lower()
            word = word.strip()
            for symbol in [".", ',','"', "'", ":", ";", "\"", "!", "?", "=", "-", ")", '(']:
                word = word.strip(symbol)
            freq_dictionary[word] = freq_dictionary.get(word, 0) + 1


equivalents = []
multiple = []

with open("translation.txt", 'r', encoding="utf-8") as translations, open("bilingual_dictionary.txt", "r", encoding="utf-8") as dictionary, open("unmatched.txt", 'w') as unmatched:
    dictionary = dictionary.read()
    for translation in translations:
        translation = translation.strip().split("\t")
        verb = translation[0].strip()

        # Check if the verb is already in the dictionary:
        if ">" + verb + "<" not in dictionary:
            translation = translation[1]
            translation = translation.split(",")
            if translation[0] != "talianu" and translation[1] == "talianu":
                translation = translation[1:]

            other_languages = ["francisi", "asturianu", "aragunisi", "chickasaw","ngrisi", "francupruvinzali", "còrsu", "occitanu", "calabbrisi centru-miridiunali", "*", 'Palori n sicilianu']
            try:
                spa_index = translation.index("spagnolu")
                ind = spa_index + 1
                spanish = []
                while True:
                    try:
                        if translation[ind] in other_languages:
                            unmatched.write(verb + '\t' + ",".join(translation) + "\n")
                            ind += 1
                            break
                        else:
                            spanish.append(translation[ind])
                            ind += 1
                    except IndexError:
                        break
                # print(verb, spanish, translation[spa_index: spa_index + 5])

                if not spanish:
                    unmatched.write(verb + '\t' + ",".join(translation))
                else:
                    if len(spanish) == 1:
                        if len(spanish[0].split()) == 1:
                            pair = (verb, spanish[0])
                            equivalents.append(pair)
                        else:
                            unmatched.write(verb + "\t" + ",".join(translation) + "\n")
                    else:
                        x = []
                        for var in spanish:
                            if len(var.split(" ")) == 1 and not var.endswith("se"):
                                x.append(var)
                        if len(x) == 1:
                            pair = (verb, x[0])
                        else:
                            if x:
                                pair = (verb, x)
                                multiple.append(pair)
                            else:
                                unmatched.write(verb + "\t" + ",".join(translation) + "\n")

                # if translation[spa_index + 1] in other_languages:
                #     unmatched.write(verb + '\t' + ",".join(translation))
                # else:
                #     if translation[spa_index + 2] in other_languages:
                #         spanish = translation[spa_index+1]
                #     else:
                #         print(translation[spa_index: spa_index + 4])

                    # Check if spanish equivalent is a verb and not an idiom:
                    # if spanish.endswith("r") and len(spanish.split(" ")) == 1:
                    #     pair = (verb, spanish)
                    #     equivalents.append(pair)
                        # print(pair)
            except ValueError:
                pass

equivalents = list(set(equivalents))

groups = {}
done = []
for i in range(0, len(equivalents) - 1):
    for j in range(0, len(equivalents) - 1):
        (sicilian1, spanish1) = equivalents[i]
        (sicilian2, spanish2) = equivalents[j]
        if i != j:
            if spanish1 == spanish2:
                if spanish1 not in done:
                    groups[spanish1] = []
                frequency1 = 0
                frequency2 = 0
                try:
                    frequency1 = freq_dictionary[sicilian1]
                except KeyError:
                    pass
                try:
                    frequency2 == freq_dictionary[sicilian2]
                except KeyError:
                    pass
                groups[spanish1].append((sicilian1, frequency1))
                groups[spanish2].append((sicilian2, frequency2))
                done.append(spanish1)

entries = []

for key in groups:
    gr = sorted(list(set(groups[key])), key = lambda sp: sp[1])
    # print(key, gr)
    entries.append(build_paradigm(gr[-1][0],  key))
    # print(build_paradigm(gr[-1][0],  key))
    if gr[-2][1] > 2:
        # print(build_paradigm(gr[-2][0],  key))
        entries.append(build_paradigm(gr[-2][0],  key))
for line in list(set(entries)):
    print(line)


# spanish_key = dict()
# for e in sorted(equivalents, key=lambda equiv: equiv[1]):
#     # print(e)
#     if e[0] in freq_dictionary.keys():
#         print(build_paradigm(e[0], e[1]))


# previous = equivalents[0]
# for (sicilian, spanish) in equivalents[1:]:
#     if spanish == previous[1]:
#         # print(previous[0], sicilian, spanish)
#         if previous[0] in freq_dictionary.keys() and sicilian in freq_dictionary.keys():
#             print(freq_dictionary[sicilian], freq_dictionary[previous[0]])
#     previous = (sicilian, spanish)


# variants = dict()
# for (sicilian, spanish) in equivalents:
#     variants[spanish] = variants.get(spanish, 0) + 1
#
# for key in variants:
#     if variants[key] > 1:
#         # print(key, variants[key])
#         for i in equivalents:
#             if key == i[1]:
#                 # print(key, i[0])
#                 if i[0] in freq_dictionary.keys():
#                     print(i[0], freq_dictionary[i[0]])

# for eq in equivalents:
#     if eq[1] in unique:
#         print(build_paradigm(eq[0], eq[1]))