import pandas as pd
import json
import sys



# =====================================
# IMPORT BACKEND MODULE
# =====================================

sys.path.append(
    r"E:\ASR_Project\web\backend"
)


from audio_analyzer import analyze_sentence_phoneme





# =====================================
# FILE PATH
# =====================================


ASR_FILE = (

    r"E:\ASR_Project\dataset\asr_results.csv"

)



ERROR_FILE = (

    r"E:\ASR_Project\dataset\vietnamese_error_analysis.csv"

)



OUTPUT_FILE = (

    r"E:\ASR_Project\dataset\sentence_analysis.json"

)







# =====================================
# LOAD DATA
# =====================================


print("Loading dataset...")



df_asr = pd.read_csv(

    ASR_FILE,

    encoding="utf-8-sig"

)



df_error = pd.read_csv(

    ERROR_FILE,

    encoding="utf-8-sig"

)





print(

    "ASR samples:",

    len(df_asr)

)







# =====================================
# ERROR MAP
# =====================================


error_map = {}




for audio, group in df_error.groupby("audio"):


    error_map[audio] = (

        group["error_type"]

        .dropna()

        .unique()

        .tolist()

    )







# =====================================
# CREATE ANALYSIS
# =====================================


result = []





for index,row in df_asr.iterrows():



    audio = row["audio"]



    reference = str(
        row["ground_truth"]
    ).strip()



    prediction = str(
        row["prediction"]
    ).strip()





    errors = error_map.get(

        audio,

        []

    )





    status = (

        "Đúng"

        if len(errors)==0

        else

        "Sai"

    )





    # ==============================
    # PHONEME ANALYSIS
    # ==============================


    if status == "Sai":


        try:


            word_analysis = (

                analyze_sentence_phoneme(

                    reference,

                    prediction

                )

            )


        except Exception as e:


            print(

                "Phoneme error:",

                audio,

                e

            )


            word_analysis = []



    else:


        word_analysis = []








    item = {



        "audio":

        audio,



        "ground_truth":

        reference,



        "prediction":

        prediction,



        "wer":

        float(row["wer"]),



        "cer":

        float(row["cer"]),



        "status":

        status,



        "errors":

        errors,



        "word_analysis":

        word_analysis



    }



    result.append(item)






# =====================================
# OUTPUT JSON
# =====================================


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