
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

pupulazzioni = '    <e lm="LEMMA"><i>ROOT</i><par n="pupulaz/zioni__n"/></e>'
annu = '    <e lm="LEMMA"><i>ROOT</i><par n="ann/u__n"/></e>'
casa = '    <e lm="LEMMA"><i>ROOT</i><par n="cas/a__n"/></e>'
mancari = '    <e lm="LEMMA"><i>ROOT</i><par n="manc/ari__vblex"/></e>'
parrari = '    <e lm="LEMMA"><i>ROOT</i><par n="parr/ari__vblex"/></e>'
battiri = '    <e lm="LEMMA"><i>ROOT</i><par n="batt/iri__vblex"/></e>'

freq_dictionary = dict()

with open("scn.crp.txt", 'r', encoding="utf-8") as corpus:
    for line in corpus:
        line = line.strip()
        line = line.split(" ")
        for word in line:
            if "'" in word:
                word = word.split("'")[1]
            elif "’" in word:
                word = word.split("’")[1]
            if word.isalpha():
                word = word.lower()
                word = word.strip()
                for symbol in [".", ',','"', "'", ":", "\"", ";", "\"", "!", "?", "=", "-", ")", '(']:
                    word = word.strip(symbol)
                freq_dictionary[word] = freq_dictionary.get(word, 0) + 1

with open("scn_dix.txt", 'r', encoding="utf-8") as dictionary:
    dictionary = dictionary.read()
    for key in freq_dictionary:
        if key.endswith("eddu") and "lm=\"" + key not in dictionary and ">" + key[:-len("a")] + "<" not in dictionary:
            if freq_dictionary[key] > 2:
                print(build_paradigm(key, casa, "a"))