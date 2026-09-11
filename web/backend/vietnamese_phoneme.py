# =====================================================
# vietnamese_phoneme.py
# Vietnamese ASR Phoneme Analyzer V9.2
# Dictionary First + Unicode Normalization
# =====================================================


import unicodedata

from vietnamese_dictionary import lookup_word





# =====================================================
# NORMALIZE UNICODE
# =====================================================


def normalize_text(text):


    return unicodedata.normalize(
        "NFC",
        str(text)
        .lower()
        .strip()
    )








# =====================================================
# TONE MAP
# =====================================================


TONE_MAP = {


    "á":"s?c",
    "à":"huy?n",
    "?":"h?i",
    "ã":"ngã",
    "?":"n?ng",


    "?":"s?c",
    "?":"huy?n",
    "?":"h?i",
    "?":"ngã",
    "?":"n?ng",


    "?":"s?c",
    "?":"huy?n",
    "?":"h?i",
    "?":"ngã",
    "?":"n?ng",


    "é":"s?c",
    "è":"huy?n",
    "?":"h?i",
    "?":"ngã",
    "?":"n?ng",


    "?":"s?c",
    "?":"huy?n",
    "?":"h?i",
    "?":"ngã",
    "?":"n?ng",


    "í":"s?c",
    "ì":"huy?n",
    "?":"h?i",
    "i":"ngã",
    "?":"n?ng",


    "ó":"s?c",
    "ò":"huy?n",
    "?":"h?i",
    "õ":"ngã",
    "?":"n?ng",


    "?":"s?c",
    "?":"huy?n",
    "?":"h?i",
    "?":"ngã",
    "?":"n?ng",


    "?":"s?c",
    "?":"huy?n",
    "?":"h?i",
    "?":"ngã",
    "?":"n?ng",


    "ú":"s?c",
    "ù":"huy?n",
    "?":"h?i",
    "u":"ngã",
    "?":"n?ng",


    "?":"s?c",
    "?":"huy?n",
    "?":"h?i",
    "?":"ngã",
    "?":"n?ng",


    "ý":"s?c",
    "?":"huy?n",
    "?":"h?i",
    "?":"ngã",
    "?":"n?ng"

}








# =====================================================
# GET TONE
# =====================================================


def get_tone(word):


    word = normalize_text(word)


    for c in word:


        if c in TONE_MAP:

            return TONE_MAP[c]



    return "ngang"








# =====================================================
# REMOVE TONE
# =====================================================


def remove_tone(word):


    word = normalize_text(word)



    table = str.maketrans(


        "áà?ã?"
        "?????"
        "?????"
        "éè???"
        "?????"
        "íì?i?"
        "óò?õ?"
        "?????"
        "?????"
        "úù?u?"
        "?????"
        "ý????",



        "aaaaa"
        "aaaaa"
        "âââââ"
        "eeeee"
        "êêêêê"
        "iiiii"
        "ooooo"
        "ôôôôô"
        "ooooo"
        "uuuuu"
        "uuuuu"
        "yyyyy"

    )


    return word.translate(table)










# =====================================================
# RULE FALLBACK
# =====================================================


INITIALS = [


    "ngh",
    "ch",
    "gh",
    "nh",
    "th",
    "tr",
    "ph",
    "kh",
    "qu",
    "gi",
    "ng",

    "d",

    "b",
    "c",
    "d",
    "g",
    "h",
    "k",
    "l",
    "m",
    "n",
    "p",
    "r",
    "s",
    "t",
    "v",
    "x"

]




FINALS = [

    "ng",
    "nh",
    "ch",
    "m",
    "n",
    "p",
    "t",
    "c"

]









def split_syllable(word):


    clean = remove_tone(word)



    result = {


        "initial":"",
        "nucleus":"",
        "final":"",
        "tone":get_tone(word)

    }



    for i in INITIALS:


        if clean.startswith(i):


            result["initial"] = i


            clean = clean[len(i):]


            break





    for f in FINALS:


        if clean.endswith(f):


            result["final"] = f


            clean = clean[:-len(f)]


            break





    result["nucleus"] = clean



    return result









# =====================================================
# DICTIONARY FIRST
# =====================================================


def get_word_phoneme(word):


    word = normalize_text(word)



    data = lookup_word(word)



    if data is not None:


        return {


            "initial":
            normalize_text(
                data["initial"]
            ),



            "nucleus":
            normalize_text(
                data["nucleus"]
            ),



            "final":
            normalize_text(
                data["final"]
            ),



            "tone":
            data["tone"]

        }




    return split_syllable(word)









# =====================================================
# ANALYZE WORD
# =====================================================


def analyze_word(reference, prediction):


    reference = normalize_text(reference)

    prediction = normalize_text(prediction)



    ref = get_word_phoneme(reference)


    hyp = get_word_phoneme(prediction)





    return {



        "word":

        reference,



        "prediction":

        prediction,



        "initial":{


            "reference":

            ref["initial"],


            "prediction":

            hyp["initial"],


            "correct":

            ref["initial"]

            ==

            hyp["initial"]

        },



        "nucleus":{


            "reference":

            ref["nucleus"],


            "prediction":

            hyp["nucleus"],


            "correct":

            ref["nucleus"]

            ==

            hyp["nucleus"]

        },



        "final":{


            "reference":

            ref["final"],


            "prediction":

            hyp["final"],


            "correct":

            ref["final"]

            ==

            hyp["final"]

        },



        "tone":{


            "reference":

            ref["tone"],


            "prediction":

            hyp["tone"],


            "correct":

            ref["tone"]

            ==

            hyp["tone"]

        }


    }