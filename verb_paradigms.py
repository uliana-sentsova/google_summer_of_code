import os
import re

parrari = '    <e lm="LEMMA"><i>ROOT</i><par n="parr/ari__vblex"/></e>'
battiri = '    <e lm="LEMMA"><i>ROOT</i><par n="batt/iri__vblex"/></e>'
mancari = '    <e lm="LEMMA"><i>ROOT</i><par n="manc/ari__vblex"/></e>'
abbintari = '\n    <e lm="LEMMA"><p><l>ROOT</l><r>ROOT</r></p><par n="abbint/ari__vblex"/></e>\n\
    <e lm="LEMMA"><p><l>FIRST</l><r>ROOT</r></p><par n="abbent/u__vblex"/></e>\n\
    <e lm="LEMMA"><p><l>SECOND</l><r>ROOT</r></p><par n="abbènt/anu__vblex"/></e>\n'
nvocari = '\n    <e lm="LEMMA"><p><l>ROOT</l><r>ROOT</r></p><par n="abbint/ari__vblex"/></e>\n\
    <e lm="LEMMA"><p><l>FIRST</l><r>ROOT</r></p><par n="nvoc/u__vblex"/></e>\n\
    <e lm="LEMMA"><p><l>SECOND</l><r>ROOT</r></p><par n="abbènt/anu__vblex"/></e>\n'


parrari_form = '    <e lm="LEMMA" r="LR"><p><l>FORM</l><r>ROOT</r></p><par n="parr/ari__vblex"/></e>'
battiri_form = '    <e lm="LEMMA" r="LR"><p><l>FORM</l><r>ROOT</r></p><par n="batt/iri__vblex"/></e>'
mancari_form = '    <e lm="LEMMA" r="LR"><p><l>FORM</l><r>ROOT</r></p><par n="manc/ari__vblex"/></e>'


parrari_group = [parrari, parrari_form, "ari"]
battiri_group = [battiri, battiri_form, "iri"]
mancari_group = [mancari, mancari_form, "ari"]



def is_cons(letter):
    for voc in ["i", "a", "o", "u", "e", "ù", "à", "ò", "ì", "è"]:
        if letter == voc:
            return True
    return False


def find_root_voc(verb):
    root = verb[:-3]
    if is_cons(root[-1]):
        return root[-1]
    elif len(root) >= 2 and is_cons(root[-2]):
        return(root[-2])
    elif len(root) >= 3 and is_cons(root[-3]):
        return root[-3]
    elif len(root) >= 4 and is_cons(root[-4]):
        return root[-4]
    else:
        return False


def replace_voc(verb, search=True):
    if find_root_voc(verb):
        voc = find_root_voc(verb)
        root = verb[:-3]
        suffix = verb[-3:]
        inversed = root[::-1]
        if search:
            if voc == "i":
                inversed = inversed.replace("i", "e", 1)
            elif voc == "ì":
                inversed = inversed.replace("ì", "e", 1)
            elif voc == "ù":
                inversed = inversed.replace("ù", "o", 1)
            elif voc == "u":
                inversed = inversed.replace("u", "o", 1)
            else:
                return False
            verb = inversed[::-1] + suffix[:1]
        else:
            if voc == "i":
                inversed = inversed.replace("i", "è", 1)
            elif voc == "ì":
                inversed = inversed.replace("ì", "è", 1)
            elif voc == "ù":
                inversed = inversed.replace("ù", "ò", 1)
            elif voc == "u":
                inversed = inversed.replace("u", "ò", 1)
            else:
                return False
            verb = inversed[::-1]
    return verb


def build_paradigm(verb, paradigm, suffix, form=None):
    root = verb[:-len(suffix)]
    if form:
        lemma = form
        if not suffix:
            root = lemma
            form_root = verb
        else:
            root = lemma[:-len(suffix)]
            form_root = verb[:-len(suffix)]
        verb_par = paradigm.replace("ROOT", root)
        verb_par = verb_par.replace("LEMMA", lemma)
        verb_par = verb_par.replace("FORM", form_root)
        return verb_par

    verb_par = paradigm.replace("ROOT", root)
    verb_par = verb_par.replace("LEMMA", verb)
    return verb_par

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

                if len(list_of_words[i][0]) > 9 and len(list_of_words[j][0]) > 9:
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


all_verbs = []
with open("verbs_translations.txt", "r", encoding="utf-8") as verbs_file, open("scn_dix.txt", 'r', encoding="utf-8") as dictionary:
    dictionary = dictionary.read()
    with open("scn.crp.txt", "r", encoding="utf-8") as corpus, open("verbs_without_paradigm.txt", 'w') as other:
        # corpus = corpus.read()
        for line in verbs_file:
            line = line.strip().split("\t")
            verb = line[0].strip()
            translation = line[1].split(",")

            if len(verb) > 3 and "lm\"" + verb not in dictionary and ">" + verb[:-3] + "<" not in dictionary:

                try:
                    ita_ind = translation.index("talianu")
                    italian = translation[ita_ind + 1]
                except ValueError:
                    # print("NONE", verb)
                    continue

                if verb.endswith("si"):
                    verb = verb[:-2]
                verb = verb.replace("ì", "i")
                verb = verb.replace("ò", "o")
                verb = verb.replace("à", "a")
                verb = verb.replace("è", "e")
                verb = verb.replace("ù", "u")

                if replace_voc(verb):
                    form = replace_voc(verb)
                    try:
                        x = freq_dictionary[form]
                        regular = False
                    except KeyError:
                        regular = True
                    except ValueError:
                        regular = True

                    if regular:
                        if verb.endswith("cari"):
                            mancari_group.append((verb, italian))
                        elif verb.endswith("ari"):
                            parrari_group.append((verb, italian))
                        elif verb.endswith("iri"):
                            battiri_group.append((verb, italian))
                        else:
                            other.write(verb + "\t" + ",".join(translation) + "\n")
                    else:
                        if x > 0:
                            print(verb, x)
                        pass
                else:
                    if verb.endswith("cari"):
                        mancari_group.append((verb, italian))
                    elif verb.endswith("ari"):
                        parrari_group.append((verb, italian))
                    elif verb.endswith("iri"):
                        battiri_group.append((verb, italian))
                    else:
                        other.write(verb + "\t" + ",".join(translation) + "\n")

all_groups = [parrari_group, mancari_group, battiri_group]
#
# with open("verb_paradigms.txt", "w") as target_file, open("verbs_to_translate.txt", 'w') as translation_list:
#     print("Calculating edit distance.")
#     gr_count = 0
#     for group in all_groups:
#         count = 0
#         merged = merge_similar(group[3:])
#
#         main_paradigm = group[0]
#         form_paradigm = group[1]
#         suffix = group[2]
#
#         print("Building paradigms.")
#
#         for line in merged:
#
#             if len(line) == 1:
#                 entry = build_paradigm(line[0], main_paradigm, suffix)
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
#                 entry = build_paradigm(word, main_paradigm, suffix)
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

#
#
#
# all_verbs = list(set(all_verbs))
#
#
# count = 0
# with open("scn.crp.txt", "r", encoding="utf-8") as corpus, open("scn_dix.txt", 'r', encoding="utf-8") as dictionary, open("entries.txt", 'w') as entries_file:
#         corpus = corpus.read()
#         dictionary = dictionary.read()
#         for verb in all_verbs:
#             # check if word is not in the sicilian dictionary:
#             try:
#                 if len(verb) > 4 and "lm=\"" + verb not in dictionary:
#                     verb = verb.strip()
#                     if verb.endswith("si"):
#                         verb = verb[:-2]
#                         verb = verb.replace("ì", "i")
#                         verb = verb.replace("ò", "o")
#                         verb = verb.replace("à", "a")
#                         verb = verb.replace("è", "e")
#                         verb = verb.replace("ù", "u")
#                     entry = "NO ENTRY" + verb
#
#                     # check if the word is regular or not:
#                     if not verb.endswith("iari") and replace_voc(verb):
#                         form = replace_voc(verb)
#                         if re.search("\W"+form+"\W", corpus):
#
#                             # find root, first form (singular) and second form (plural)
#                             root = verb[:-3]
#                             first_form = form[:-1]
#                             second_form = replace_voc(verb, search=False)
#
#                             # check consonant
#                             if root.endswith("c") or root.endswith("g"):
#                                 entry = nvocari.replace("LEMMA", verb)
#                                 entry = entry.replace("ROOT", root)
#                                 entry = entry.replace("FIRST", first_form)
#                                 entry = entry.replace("SECOND", second_form)
#                             else:
#                                 entry = abbintari.replace("LEMMA", verb)
#                                 entry = entry.replace("ROOT", root)
#                                 entry = entry.replace("FIRST", first_form)
#                                 entry = entry.replace("SECOND", second_form)
#                             # READY!!!
#                             # print(entry)
#                         else:
#                             if verb.endswith("ari"):
#                                 if verb.endswith("cari"):
#                                     entry = build_paradigm(verb, mancari)
#                                 else:
#                                     entry = build_paradigm(verb, parrari)
#                             elif verb.endswith("iri"):
#                                 entry = build_paradigm(verb, battiri)
#                             else:
#                                 print("NO PARADIMG", verb)
#                     else:
#                         if verb.endswith("ari"):
#                             if verb.endswith("cari"):
#                                 entry = build_paradigm(verb, mancari)
#                             else:
#                                 entry = build_paradigm(verb, parrari)
#                         elif verb.endswith("iri"):
#                             entry = build_paradigm(verb, battiri)
#                         else:
#                             print("NO PARADIMG", verb)
#                     # print(entry)
#                     if "NO " not in entry:
#                         entries_file.write(entry + "\n")
#             except Exception as err:
#                 print(err, verb)
#             count += 1
#             if count%100 == 0:
#                 print("Analyzed", count, "verbs.")
#
# with open("entries.txt", 'r') as new_entries, open("scn_dix.txt", 'a', encoding="utf-8") as dictionary:
#     dictionary.write("\n")
#     for new_entry in new_entries:
#         if "NO " not in new_entry:
#             dictionary.write(new_entry.strip() + "\n")