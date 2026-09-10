import pandas as pd
import json
import os


# =========================
# FILE INPUT
# =========================

asr_file = r"E:\ASR_Project\dataset\asr_results.csv"

error_file = r"E:\ASR_Project\dataset\vietnamese_error_analysis.csv"


# OUTPUT

output_file = r"E:\ASR_Project\dataset\sentence_analysis.json"



# =========================
# ĐỌC DỮ LIỆU
# =========================

df_asr = pd.read_csv(
    asr_file,
    encoding="utf-8-sig"
)


df_error = pd.read_csv(
    error_file,
    encoding="utf-8-sig"
)



# =========================
# MAP LỖI THEO AUDIO
# =========================

error_map = {}



for audio, group in df_error.groupby("audio"):

    errors = (
        group["error_type"]
        .unique()
        .tolist()
    )


    error_map[audio] = errors



# =========================
# TẠO SENTENCE ANALYSIS
# =========================

result = []



for _, row in df_asr.iterrows():

    audio = row["audio"]


    errors = error_map.get(
        audio,
        []
    )


    if len(errors) == 0:

        status = "Đúng"

    else:

        status = "Sai"



    result.append({

        "audio": audio,

        "ground_truth":
            row["ground_truth"],

        "prediction":
            row["prediction"],

        "wer":
            float(row["wer"]),

        "cer":
            float(row["cer"]),

        "status":
            status,

        "errors":
            errors

    })




data = {

    "total_audio":
        len(result),

    "data":
        result

}



# =========================
# LƯU JSON
# =========================

with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        data,
        f,
        ensure_ascii=False,
        indent=2
    )



print(
    "===== DONE ====="
)

print(
    "Tong audio:",
    len(result)
)

print(
    "Da tao:"
)

print(
    output_file
)