import os
import re

# Building a paradigm with given noun, paradigm and the suffix of the noun which changes during the declination
def build_paradigm(noun, paradigm, suffix, form=None):

    if suffix != "":
        root = noun[:-len(suffix)]
    else:
        root = noun

    if form:
        lemma = form
        if not suffix:
            root = lemma
            form_root = noun
        else:
            root = lemma[:-len(suffix)]
            form_root = noun[:-len(suffix)]
        noun_par = paradigm.replace("ROOT", root)
        noun_par = noun_par.replace("LEMMA", lemma)
        noun_par = noun_par.replace("FORM", form_root)
        return noun_par

    noun_par = paradigm.replace("ROOT", root)
    noun_par = noun_par.replace("LEMMA", noun)
    return noun_par


# Calculating Levenstein distance in order to find similar forms of nouns:
def distance(a, b):
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n+1) # Keep current and previous row, not entire matrix
    for i in range(1, m+1):
        previous_row, current_row = current_row, [i]+[0]*n
        for j in range(1,n+1):
            add, delete, change = previous_row[j]+1, current_row[j-1]+1, previous_row[j-1]
            if a[j-1] != b[i-1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


# Добавить возможность смотреть на итальянский перевод
def merge_similar(list_of_words, distance_value=3, without_italian=True):
    checked_j = []
    checked_i = []
    words_forms = dict()
    list_of_words = list(set(list_of_words))
    for i in range(0, len(list_of_words) - 1):
        for j in range(0, len(list_of_words) - 1):
            if i != j and list_of_words[j] not in checked_j and list_of_words[j] not in checked_i:
                # print(list_of_words[i], list_of_words[j])

                try:
                    italian_i = list_of_words[i][1]
                    italian_j = list_of_words[j][1]
                except IndexError as err:
                    print(err, "HERE IT IS", list_of_words[j], j, i)

                if len(list_of_words[i][0]) > 7 and len(list_of_words[j][0]) > 7:
                    distance_value = 4
                if len(list_of_words[i][0]) < 5 and len(list_of_words[j]) < 5:
                    distance_value = 2

                if distance(list_of_words[i][0], list_of_words[j][0]) <= distance_value and italian_i == italian_j:
                    if list_of_words[i] not in checked_i:
                        words_forms[list_of_words[i]] = []
                    words_forms[list_of_words[i]].append(list_of_words[j])

                    checked_j.append(list_of_words[j])
                    checked_i.append(list_of_words[i])
    groups = []
    for key in words_forms:
        group = []
        group.append(key)
        for form in words_forms[key]:
            group.append(form)
        groups.append(group)

    groups = sorted(groups)

    for word in list_of_words:
        if word not in checked_i and word not in checked_j:
            groups.append([word])

    if without_italian:
        new_group = []
        for line in groups:
            temp = []
            for word in line:
                if type(word) == tuple:
                    temp.append(word[0])
                else:
                    temp.append(word)
            new_group.append(temp)
        return sorted(new_group)

    return sorted(groups)


# Looking for the frequency of word in the corpus:
def find_frequency(word):
    try:
        return freq_dictionary[word]
    except KeyError:
        return 0



# Most common noun paradigms
annu = '    <e lm="LEMMA"><i>ROOT</i><par n="ann/u__n"/></e>'
tirritoriu = '    <e lm="LEMMA"><i>ROOT</i><par n="tirritori/u__n"/></e>'
casa = '    <e lm="LEMMA"><i>ROOT</i><par n="cas/a__n"/></e>'
oricchia = '    <e lm="LEMMA"><i>ROOT</i><par n="oricch/ia__n"/></e>'
citati = '    <e lm="LEMMA"><i>ROOT</i><par n="cit/ati__n"/></e>'
pupulazzioni = '    <e lm="LEMMA"><i>ROOT</i><par n="pupulaz/zioni__n"/></e>'
parcu = '    <e lm="LEMMA"><i>ROOT</i><par n="parc/u__n"/></e>'
ripubrica = '    <e lm="LEMMA"><i>ROOT</i><par n="ripùbbric/a__n"/></e>'
culonia = '    <e lm="LEMMA"><i>ROOT</i><par n="culoni/a__n"/></e>'
sucialismu = '    <e lm="LEMMA"><i>ROOT</i><par n="sucialism/u__n"/></e>'
patri = '    <e lm="LEMMA"><i>ROOT</i><par n="patri__n"/></e>'
matri = '    <e lm="LEMMA"><i>ROOT</i><par n="matri__n"/></e>'
chitarrista = '    <e lm="LEMMA"><i>ROOT</i><par n="chitarrist/a__n"/></e>'
pianeta = '    <e lm="LEMMA"><i>ROOT</i><par n="pianet/a__n"/></e>'

annu_form = '    <e lm="LEMMA" r="LR"><p><l>FORM</l><r>ROOT</r></p><par n="ann/u__n"/></e>'
tirritoriu_form = '    <e lm="LEMMA" r="LR"><p><l>FORM</l><r>ROOT</r></p><par n="tirritori/u__n"/></e>'
casa_form = '    <e lm="LEMMA" r="LR"><p><l>FORM</l><r>ROOT</r></p><par n="cas/a__n"/></e>'
oricchia_form = '    <e lm="LEMMA" r="LR"><p><l>FORM</l><r>ROOT</r></p><par n="oricch/ia__n"/></e>'
citati_form = '    <e lm="LEMMA" r="LR"><p><l>FORM</l><r>ROOT</r></p><par n="cit/ati__n"/></e>'
pupulazzioni_form = '    <e lm="LEMMA" r="LR"><p><l>FORM</l><r>ROOT</r></p><par n="pupulaz/zioni__n"/></e>'
parcu_form = '    <e lm="LEMMA" r="LR"><p><l>FORM</l><r>ROOT</r></p><par n="parc/u__n"/></e>'
ripubrica_form = '    <e lm="LEMMA" r="LR"><p><l>FORM</l><r>ROOT</r></p><par n="ripùbbric/a__n"/></e>'
culonia_form = '    <e lm="LEMMA" r="LR"><p><l>FORM</l><r>ROOT</r></p><par n="culoni/a__n"/></e>'
sucialismu_form = '    <e lm="LEMMA" r="LR"><p><l>FORM</l><r>ROOT</r></p><par n="sucialism/u__n"/></e>'
patri_form = '    <e lm="LEMMA" r="LR"><p><l>FORM</l><r>ROOT</r></p><par n="patri__n"/></e>'
matri_form = '    <e lm="LEMMA" r="LR"><p><l>FORM</l><r>ROOT</r></p><par n="matri__n"/></e>'
chitarrista_form = '    <e lm="LEMMA" r="LR"><p><l>FORM</l><r>ROOT</r></p><par n="chitarrist/a__n"/></e>'
pianeta_form = '    <e lm="LEMMA" r="LR"><p><l>FORM</l><r>ROOT</r></p><par n="pianet/a__n"/></e>'


annu_group = [annu, annu_form, "u"]
tirritoriu_group = [tirritoriu, tirritoriu_form, "u"]
casa_group = [casa, casa_form, "a"]
oricchia_group = [oricchia, oricchia_form, "ia"]
citati_group = [citati, citati_form, "ati"]
pupulazzioni_group = [pupulazzioni, pupulazzioni_form, "zioni"]
parcu_group = [parcu, parcu_form, "u"]
ripubrica_group = [ripubrica, ripubrica_form, "u"]
culonia_group = [culonia, culonia_form, "ìa"]
sucialismu_group = [sucialismu, sucialismu_form, "u"]
patri_group = [patri, patri_form, ""]
matri_group = [matri, matri_form, ""]
chitarrista_group = [chitarrista, chitarrista_form, "a"]
pianeta_group = [pianeta, pianeta_form, "a"]




# Create tf-idf dictionary
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


with open("nouns_translations.txt", 'r', encoding="utf-8") as nouns, open("dictionary.txt", 'r', encoding="utf-8") as dictionary, open("nouns_without_paradigm.txt", "w") as other:
    dictionary = dictionary.read()
    for line in nouns:
        line = line.strip().split("\t")
        noun = line[0].strip()

        translation = line[1].split(",")
        grammar = translation[0:3]

        # Find italian translation:

        if len(noun) > 2 and "lm=\"" + noun not in dictionary and grammar[0] != "pl":

            try:
                ita_ind = translation.index("talianu")
                italian = translation[ita_ind + 1]
            except ValueError:
                continue

            if noun.endswith("gu"):
                # entry = build_paradigm(noun, parcu, suffix="u")
                parcu_group.append((noun, italian))
                # print(entry)
            elif noun.endswith("iu"):
                # entry = build_paradigm(noun, tirritoriu, suffix = "u")
                tirritoriu_group.append((noun, italian))
                # print(entry)
            elif noun.endswith("ia"):
                # entry = build_paradigm(noun, oricchia, suffix="ia")
                oricchia_group.append((noun, italian))
                # print(entry)
            elif noun.endswith("ati"):
                # entry = build_paradigm(noun, citati, suffix="ati")
                citati_group.append((noun, italian))
                # print(entry)
            elif noun.endswith("zioni"):
                # entry = build_paradigm(noun, pupulazzioni, suffix="zioni")
                pupulazzioni_group.append((noun, italian))
                # print(entry)
            elif noun.endswith("ca"):
                # entry = build_paradigm(noun, ripubrica, suffix="a")
                ripubrica_group.append((noun, italian))
                # print(entry)
            elif noun.endswith("ìa"):
                # entry = build_paradigm(noun, culonia, suffix="a")
                culonia_group.append((noun, italian))
            elif noun.endswith("ismu"):
                sucialismu_group.append((noun, italian))
                # print(entry)
            elif noun.endswith("a") and "f" in grammar and "m" not in grammar:
                casa_group.append((noun, italian))
            # elif noun.endswith("u") and "m" in grammar and "f" not in grammar:
            # elif noun.endswith("u") and "m" in grammar:
            #     annu_group.append(noun)
            elif noun.endswith("mentu") or noun.endswith("ddu") or noun.endswith("ttu"):
                # print(noun)
                annu_group.append((noun, italian))
                # print(noun, italian)
            elif noun.endswith("u") and "f" not in grammar and len(noun) > 4 and not noun.endswith("gu"):
                pass
                # print(noun, italian)
                # annu_group.append((noun, italian))
            elif noun.endswith("i") and "m" in grammar and "f" not in grammar:
                pass
                # patri_group.append((noun, italian))
            elif noun.endswith("i") and "f" in grammar and "m" not in grammar:
                pass
                # matri_group.append((noun, italian))
            elif noun.endswith("ista"):
                chitarrista_group.append((noun, italian))
            elif (noun.endswith("ma") or noun.endswith("ta")) and "m" in grammar:
                pianeta_group.append((noun, italian))
            elif noun.endswith("tà") and "f" in grammar:
                matri_group.append((noun, italian))
            elif "lingua" in italian:
                patri_group.append((noun, italian))
            else:
                other.write(noun + "\t" + ",".join(translation) + "\n")
                print(noun, italian)



all_groups = [patri_group]
# other = [chitarrista_group, pianeta_group, sucialismu_group, casa_group, pupulazzioni_group, parcu_group, ripubrica_group,
#               citati_group, oricchia_group, culonia_group, tirritoriu_group]
#
# #
# with open("nouns_paradigms_patr.txt", "w") as target_file, open("nouns_to_translate_patri.txt", 'w') as translation_list:
#     gr_count = 0
#     for group in all_groups:
#         count = 0
#         merged = merge_similar(group[3:])
#
#         main_paradium = group[0]
#         form_paradigm = group[1]
#         suffix = group[2]
#
#         for line in merged:
#
#             if len(line) == 1:
#                 entry = build_paradigm(line[0], main_paradium, suffix)
#                 # print()
#                 target_file.write(entry + "\n")
#                 translation_list.write(line[0] + "\n")
#
#             else:
#                 frequencies = []
#                 for word in line:
#                     frequencies.append(find_frequency(word))
#                 maximum = max(frequencies)
#                 max_ind = frequencies.index(maximum)
#                 word = line[max_ind]
#
#                 entry = build_paradigm(word, main_paradium, suffix)
#                 target_file.write(entry + "\n")
#                 translation_list.write(word + "\n")
#
#                 del line[max_ind]
#
#                 for l in line:
#                     entry = build_paradigm(l, form_paradigm, suffix, form=word)
#                     target_file.write(entry + "\n")
#                 count += 1
#                 if count%10 == 0:
#                     print("Обработано", count, "слов из группы", gr_count)
#         gr_count += 1