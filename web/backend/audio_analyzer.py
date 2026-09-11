# -*- coding: utf-8 -*-

# =====================================================
# audio_analyzer.py
# Vietnamese ASR Error Analyzer V10.4
# Levenshtein Alignment + Phoneme Analysis
# =====================================================


import re
import unicodedata
import jiwer


from vietnamese_phoneme import analyze_word




# =====================================================
# NORMALIZATION
# =====================================================


def normalize_word(word):

    word = unicodedata.normalize(
        "NFC",
        str(word)
    )


    word = word.lower()



    word = re.sub(
        r"[^\wà-ỹđ]",
        "",
        word
    )


    return word





def normalize_sentence(text):

    result = []


    for word in text.split():

        clean = normalize_word(word)

        if clean:

            result.append(clean)



    return " ".join(result)







# =====================================================
# WER / CER
# =====================================================


def calculate_score(
        reference,
        prediction
):


    ref = normalize_sentence(
        reference
    )


    hyp = normalize_sentence(
        prediction
    )



    wer = jiwer.wer(
        ref,
        hyp
    )


    cer = jiwer.cer(
        ref,
        hyp
    )



    return {


        "wer":

        round(
            wer,
            4
        ),



        "cer":

        round(
            cer,
            4
        )

    }







# =====================================================
# WORD PHONEME ERROR
# =====================================================


def detect_word_error(
        reference,
        prediction
):


    detail = analyze_word(
        reference,
        prediction
    )


    errors = []



    if not detail["initial"]["correct"]:

        errors.append(
            "initial_consonant_error"
        )



    if not detail["nucleus"]["correct"]:

        errors.append(
            "nucleus_error"
        )



    if not detail["final"]["correct"]:

        errors.append(
            "final_consonant_error"
        )



    if not detail["tone"]["correct"]:

        errors.append(
            "tone_error"
        )



    return errors, detail







# =====================================================
# LEVENSHTEIN WORD ALIGNMENT
# =====================================================


def word_alignment(
        reference,
        prediction
):


    ref_words = [

        normalize_word(w)

        for w in reference.split()

    ]



    hyp_words = [

        normalize_word(w)

        for w in prediction.split()

    ]



    m = len(ref_words)

    n = len(hyp_words)



    dp = [

        [0]*(n+1)

        for _ in range(m+1)

    ]



    for i in range(m+1):

        dp[i][0] = i



    for j in range(n+1):

        dp[0][j] = j





    for i in range(1,m+1):

        for j in range(1,n+1):


            cost = (

                0

                if ref_words[i-1]

                ==

                hyp_words[j-1]

                else

                1

            )


            dp[i][j] = min(

                dp[i-1][j]+1,

                dp[i][j-1]+1,

                dp[i-1][j-1]+cost

            )





    alignment = []


    i = m

    j = n



    while i > 0 or j > 0:



        if (

            i > 0

            and

            j > 0

            and

            ref_words[i-1]

            ==

            hyp_words[j-1]

        ):


            alignment.append({

                "type":"equal",

                "reference":

                ref_words[i-1],

                "prediction":

                hyp_words[j-1]

            })


            i -= 1

            j -= 1




        elif (

            i > 0

            and

            j > 0

            and

            dp[i][j]

            ==

            dp[i-1][j-1]+1

        ):


            alignment.append({

                "type":"substitution",

                "reference":

                ref_words[i-1],

                "prediction":

                hyp_words[j-1]

            })


            i -= 1

            j -= 1





        elif (

            i > 0

            and

            dp[i][j]

            ==

            dp[i-1][j]+1

        ):


            alignment.append({

                "type":"missing_word",

                "reference":

                ref_words[i-1],

                "prediction":

                ""

            })


            i -= 1




        else:


            alignment.append({

                "type":"extra_word",

                "reference":

                "",

                "prediction":

                hyp_words[j-1]

            })


            j -= 1





    alignment.reverse()


    return alignment







# =====================================================
# SENTENCE PHONEME ANALYSIS
# =====================================================


def analyze_sentence_phoneme(
        reference,
        prediction
):


    result = []



    alignment = word_alignment(

        reference,

        prediction

    )





    for item in alignment:


        typ = item["type"]


        ref = item["reference"]


        hyp = item["prediction"]





        if typ == "equal":

            continue





        if typ == "substitution":


            errors, detail = detect_word_error(

                ref,

                hyp

            )



            result.append({

                "type":

                "substitution",


                "reference":

                ref,


                "prediction":

                hyp,


                "errors":

                errors,


                "detail":

                detail

            })







        elif typ == "missing_word":


            result.append({

                "type":

                "missing_word",


                "reference":

                ref,


                "prediction":

                "",


                "errors":

                [

                    "missing_word"

                ],


                "detail":

                None

            })







        elif typ == "extra_word":


            result.append({

                "type":

                "extra_word",


                "reference":

                "",


                "prediction":

                hyp,


                "errors":

                [

                    "extra_word"

                ],


                "detail":

                None

            })





    return result







# =====================================================
# ERROR TYPE SUMMARY
# =====================================================


def simple_error_check(
        reference,
        prediction
):


    errors = []


    analysis = analyze_sentence_phoneme(

        reference,

        prediction

    )



    for item in analysis:


        errors.extend(

            item["errors"]

        )




    return list(set(errors))







# =====================================================
# MAIN ANALYZER
# =====================================================


def analyze_result(
        audio,
        reference,
        prediction
):


    score = calculate_score(

        reference,

        prediction

    )



    errors = simple_error_check(

        reference,

        prediction

    )



    word_analysis = analyze_sentence_phoneme(

        reference,

        prediction

    )




    return {


        "audio":

        audio,



        "ground_truth":

        normalize_sentence(reference),



        "prediction":

        normalize_sentence(prediction),



        "wer":

        score["wer"],



        "cer":

        score["cer"],



        "status":

        (

            "Đúng"

            if len(errors)==0

            else

            "Sai"

        ),



        "errors":

        errors,



        "word_analysis":

        word_analysis

    }