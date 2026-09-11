# -*- coding: utf-8 -*-

# =====================================================
# generate_sentence_analysis.py
# Vietnamese ASR Sentence Analysis V10.5
# Normalize + Alignment + Phoneme Error
# =====================================================


import pandas as pd
import json
import sys
import re
import unicodedata




# =====================================================
# IMPORT BACKEND
# =====================================================


sys.path.append(
    r"E:\ASR_Project\web\backend"
)


from audio_analyzer import (
    analyze_sentence_phoneme
)







# =====================================================
# FILE PATH
# =====================================================


ASR_FILE = (

    r"E:\ASR_Project\dataset\asr_results.csv"

)



OUTPUT_FILE = (

    r"E:\ASR_Project\dataset\sentence_analysis.json"

)







# =====================================================
# TEXT NORMALIZATION
# =====================================================


def normalize_text(text):


    text = unicodedata.normalize(

        "NFC",

        str(text)

    )


    text = text.lower()



    # bỏ dấu câu

    text = re.sub(

        r"[^\w\sà-ỹđ]",

        "",

        text

    )



    # bỏ khoảng trắng thừa

    text = re.sub(

        r"\s+",

        " ",

        text

    )



    return text.strip()







# =====================================================
# LOAD DATA
# =====================================================


print(
    "Loading dataset..."
)




df_asr = pd.read_csv(

    ASR_FILE,

    encoding="utf-8-sig"

)



print(

    "ASR samples:",

    len(df_asr)

)







# =====================================================
# CREATE ANALYSIS
# =====================================================


result = []





for index,row in df_asr.iterrows():



    audio = row["audio"]




    reference = normalize_text(

        row["ground_truth"]

    )



    prediction = normalize_text(

        row["prediction"]

    )






    # =====================================
    # PHONEME ANALYSIS
    # =====================================



    try:


        word_analysis = analyze_sentence_phoneme(

            reference,

            prediction

        )



    except Exception as e:


        print(

            "Analysis error:",

            audio,

            e

        )


        word_analysis = []






    # =====================================
    # COLLECT ERROR
    # =====================================



    errors = []



    for item in word_analysis:


        for err in item.get(

            "errors",

            []

        ):


            errors.append(err)





    errors = list(set(errors))






    status = (

        "Đúng"

        if len(errors)==0

        else

        "Sai"

    )








    item = {



        "audio":

        audio,




        "ground_truth":

        reference,




        "prediction":

        prediction,




        "wer":

        float(

            row["wer"]

        ),




        "cer":

        float(

            row["cer"]

        ),




        "status":

        status,




        "errors":

        errors,




        "word_analysis":

        word_analysis



    }



    result.append(item)







# =====================================================
# SAVE JSON
# =====================================================



output = {



    "total_audio":

    len(result),



    "data":

    result



}






with open(

    OUTPUT_FILE,

    "w",

    encoding="utf-8"

) as f:



    json.dump(

        output,

        f,

        ensure_ascii=False,

        indent=2

    )







print("==========================")

print("DONE")

print(

    "Total:",

    len(result)

)


print(

    "Saved:",

    OUTPUT_FILE

)

print("==========================")