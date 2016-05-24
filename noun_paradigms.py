import os
import re

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


# Building a paradigm with given noun, paradigm and the suffix of the noun which changes during the declination
def build_paradigm(noun, paradigm, suffix):
    root = noun[:-len(suffix)]
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

nouns_list = []


with open("nouns_translations.txt", 'r', encoding="utf-8") as nouns, open("nouns_paradigms.txt", "w") as target_file:
    with open("dictionary.txt", 'r', encoding="utf-8") as dictionary:
        dictionary = dictionary.read()
        for line in nouns:
            line = line.strip().split("\t")
            noun = line[0].strip()

            translation = line[1].split(",")
            grammar = translation[0:2]
            if len(noun) > 2 and "lm=\"" + noun not in dictionary and grammar[0] != "pl":
                if noun.endswith("cu"):
                    entry = build_paradigm(noun, parcu, suffix="u")
                    # print(entry)
                elif noun.endswith("iu"):
                    entry = build_paradigm(noun, tirritoriu, suffix = "u")
                    # print(entry)
                elif noun.endswith("ia"):
                    entry = build_paradigm(noun, oricchia, suffix="ia")
                    # print(entry)
                elif noun.endswith("ati"):
                    entry = build_paradigm(noun, citati, suffix="ati")
                    # print(entry)
                elif noun.endswith("zioni"):
                    entry = build_paradigm(noun, pupulazzioni, suffix="zioni")
                    # print(entry)
                elif noun.endswith("ca"):
                    entry = build_paradigm(noun, ripubrica, suffix="a")
                    # print(entry)
                elif noun.endswith("ìa"):
                    # entry = build_paradigm(noun, culonia, suffix="a")
                    # print(entry)
                    nouns_list.append(noun)
                elif noun.endswith("a"):
                    pass
matched = []
done = []
nouns_forms = dict()

for i in range(0, len(nouns_list) - 1):
    for j in range(0, len(nouns_list) - 1):
        if i != j and nouns_list[j] not in matched:
            if distance(nouns_list[i], nouns_list[j]) < 2:

                print(nouns_list[i], nouns_list[j])
                matched.append(nouns_list[i])

                if nouns_list[i] not in done:
                    nouns_forms[nouns_list[i]] = []
                try:
                    nouns_forms[nouns_list[i]].append((nouns_list[j], freq_dictionary[nouns_list[j]]))
                except KeyError:
                    nouns_forms[nouns_list[i]].append((nouns_list[j], 0))
                done.append(nouns_list[i])

for key in nouns_forms:
    print(key, nouns_forms[key])