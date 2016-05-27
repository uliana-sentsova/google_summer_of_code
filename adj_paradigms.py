

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

def find_frequency(word):
    try:
        return freq_dictionary[word]
    except KeyError:
        return 0


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
            assert type(list_of_words[i]) == tuple
            if i != j and list_of_words[j] not in checked_j and list_of_words[j] not in checked_i:
                # print(list_of_words[i], list_of_words[j])

                try:
                    italian_i = list_of_words[i][1]
                    italian_j = list_of_words[j][1]
                    assert len(italian_i) > 1
                    assert len(italian_j) > 1
                except IndexError as err:
                    print(err, "HERE IT IS", list_of_words[j], j, i)

                if len(list_of_words[i][0]) > 7 and len(list_of_words[j][0]) > 6:
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

beddu = '    <e lm="LEMMA"><i>ROOT</i><par n="bedd/u__adj"/></e>'
lariu = '    <e lm="LEMMA"><i>ROOT</i><par n="lar/iu__adj"/></e>'
magneticu = '    <e lm="LEMMA"><i>ROOT</i><par n="magnètic/u__adj"/></e>'
duci = '    <e lm="LEMMA"><par n="ø/i"/><i>ROOT</i><par n="duci__adj"/></e>'

beddu_form = '    <e lm="LEMMA" r="LR"><p><l>FORM</l><r>ROOT</r></p><par n="bedd/u__adj"/></e>'
lariu_form = '    <e lm="LEMMA" r="LR"><p><l>FORM</l><r>ROOT</r></p><par n="lar/iu__adj"/></e>'
magneticu_form = '    <e lm="LEMMA" r="LR"><p><l>FORM</l><r>ROOT</r></p><par n="magnètic/u__adj"/></e>'
duci_form = '    <e lm="LEMMA" r="LR"><p><l>FORM</l><r>ROOT</r></p><par n="duc/i__adj"/></e>'

beddu_group = [beddu, beddu_form, "u"]
lariu_group = [lariu, lariu_form, "iu"]
magneticu_group = [magneticu, magneticu_form, "u"]
duci_group = [duci, duci_form, ""]


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

unmatched = []
adjs = []
with open("adj_translations.txt", "r", encoding="utf-8") as adj_file, open("scn_dix.txt", 'r', encoding="utf-8") as dix:
    dix = dix.read()
    for line in adj_file:
        line = line.split("\t")
        adj = line[0]
        translation = line[1]
        translation = translation.split(",")
        grammar = translation[:4]
        if "lm=\"" + adj not in dix and "pl" not in grammar and "f" not in grammar:

            try:
                ita_ind = translation.index("talianu")
                italian = translation[ita_ind + 1]
            except ValueError:
                continue

            if adj.endswith("cu"):
                magneticu_group.append((adj, italian))
            elif adj.endswith("iu"):
                lariu_group.append((adj, italian))
            elif adj.endswith("u"):
                beddu_group.append((adj, italian))
            elif adj.endswith("i"):
                duci_group.append((adj, italian))
            else:
                unmatched.append([adj, translation])

all_groups = [beddu_group, duci_group, lariu_group, magneticu_group]

with open("adj_paradigms.txt", "w") as target_file:
    gr_count = 0
    for group in all_groups:
        count = 0
        merged = merge_similar(group[3:])

        main_paradium = group[0]
        form_paradigm = group[1]
        suffix = group[2]

        for line in merged:

            if len(line) == 1:
                entry = build_paradigm(line[0], main_paradium, suffix)
                target_file.write(entry + "\n")

            else:
                frequencies = []
                for word in line:
                    frequencies.append(find_frequency(word))
                maximum = max(frequencies)
                max_ind = frequencies.index(maximum)
                word = line[max_ind]

                entry = build_paradigm(word, main_paradium, suffix)
                target_file.write(entry + "\n")

                del line[max_ind]

                for l in line:
                    entry = build_paradigm(l, form_paradigm, suffix, form=word)
                    target_file.write(entry + "\n")
                count += 1
                if count%10 == 0:
                    print("Обработано", count, "слов из группы", gr_count)
        gr_count += 1

