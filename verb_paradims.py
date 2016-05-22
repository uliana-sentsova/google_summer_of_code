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


def is_cons(letter):
    for voc in ["i", "a", "o", "u", "e", "ù", "à", "ò", "ì", "è"]:
        if letter == voc:
            return True
    return False


def find_root_voc(verb):
    root = verb[:-3]
    if is_cons(root[-1]):
        return root[-1]
    elif is_cons(root[-2]):
        return(root[-2])
    elif is_cons(root[-3]):
        return root[-3]
    elif is_cons(root[-4]):
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


def build_paradigm(verb, paradigm):
    assert verb and verb.endswith("ri")
    root = verb[:-3]
    entry = paradigm.replace("LEMMA", verb)
    entry = entry.replace("ROOT", root)
    return entry



with open("verbs.txt", "r", encoding="utf-8") as verbs_file, open("scn.crp.txt", "r", encoding="utf-8") as corpus:
    with open("dictionary.txt", 'r', encoding="utf-8") as dictionary:
        corpus = corpus.read()
        dictionary = dictionary.read()
        for verb in verbs_file:
            # check if verb is not in the sicilian dictionary:
            if "lm=\"" + verb + "\"" not in dictionary:
                verb = verb.strip()
                if verb.endswith("si"):
                    verb = verb[:-2]
                    verb = verb.replace("ì", "i")
                    verb = verb.replace("ò", "o")
                    verb = verb.replace("à", "a")
                    verb = verb.replace("è", "e")
                    verb = verb.replace("ù", "u")
                entry = "NO ENTRY"

                # check if the verb is regular or not:
                if not verb.endswith("iari") and replace_voc(verb):
                    form = replace_voc(verb)
                    if re.search("\W"+form+"\W", corpus):

                        # find root, first form (singular) and second form (plural)
                        root = verb[:-3]
                        first_form = form[:-1]
                        second_form = replace_voc(verb, search=False)

                        # check consonant
                        if root.endswith("c") or root.endswith("g"):
                            entry = nvocari.replace("LEMMA", verb)
                            entry = entry.replace("ROOT", root)
                            entry = entry.replace("FIRST", first_form)
                            entry = entry.replace("SECOND", second_form)
                        else:
                            entry = abbintari.replace("LEMMA", verb)
                            entry = entry.replace("ROOT", root)
                            entry = entry.replace("FIRST", first_form)
                            entry = entry.replace("SECOND", second_form)
                        # READY!!!
                        # print(entry)
                    else:
                        if verb.endswith("ari"):
                            if verb.endswith("cari"):
                                entry = build_paradigm(verb, mancari)
                            else:
                                entry = build_paradigm(verb, parrari)
                        elif verb.endswith("iri"):
                            entry = build_paradigm(verb, battiri)
                        else:
                            raise ValueError("No such paradigm")
                else:
                    if verb.endswith("ari"):
                        if verb.endswith("cari"):
                            entry = build_paradigm(verb, mancari)
                        else:
                            entry = build_paradigm(verb, parrari)
                    elif verb.endswith("iri"):
                        entry = build_paradigm(verb, battiri)
                    else:
                        raise ValueError("No such paradigm")
                print(entry)
