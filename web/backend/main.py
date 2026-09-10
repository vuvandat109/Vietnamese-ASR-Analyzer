from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import json
import os



# ==================================
# KHỞI TẠO APP
# ==================================

app = FastAPI(
    title="Vietnamese ASR Analyzer API"
)



# ==================================
# CHO PHÉP REACT GỌI API
# ==================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ]

)





# ==================================
# ĐƯỜNG DẪN DATA
# ==================================


BASE_DIR = r"E:\ASR_Project\dataset"


REPORT_FILE = os.path.join(
    BASE_DIR,
    "summary_report.json"
)



ERROR_FILE = os.path.join(
    BASE_DIR,
    "vietnamese_error_analysis.csv"
)





# ==================================
# TRANG TEST
# ==================================


@app.get("/")
def home():

    return {

        "message":
        "Vietnamese ASR Analyzer API running"

    }







# ==================================
# API LẤY BÁO CÁO TỔNG QUAN
# ==================================


@app.get("/report")
def get_report():


    if not os.path.exists(
        REPORT_FILE
    ):

        return {

            "error":
            "Không tìm thấy summary_report.json"

        }



    with open(

        REPORT_FILE,

        "r",

        encoding="utf-8"

    ) as f:


        data = json.load(f)



    return data







# ==================================
# API LẤY CHI TIẾT LỖI
# ==================================


@app.get("/errors")
def get_errors():


    if not os.path.exists(
        ERROR_FILE
    ):


        return {

            "error":
            "Không tìm thấy vietnamese_error_analysis.csv"

        }



    # Đọc CSV

    df = pd.read_csv(

        ERROR_FILE,

        encoding="utf-8-sig"

    )



    # QUAN TRỌNG:
    # Xóa NaN để JSON không lỗi

    df = df.fillna("")



    data = df.to_dict(

        orient="records"

    )



    return {


        "total":

        len(data),



        "data":

        data


    }







# ==================================
# CHẠY:
#
# uvicorn main:app --reload
#
# ==================================
# =====================================
# PHÂN TÍCH LỖI THEO CÂU
# =====================================

@app.get("/analysis")
def sentence_analysis():

    import pandas as pd
    import os


    error_file = r"E:\ASR_Project\dataset\vietnamese_error_analysis.csv"


    if not os.path.exists(error_file):

        return {
            "error": "Không tìm thấy file vietnamese_error_analysis.csv"
        }



    df = pd.read_csv(
        error_file,
        encoding="utf-8-sig"
    )


    df = df.fillna("")


    result = []


    # Gom theo từng audio
    for audio, group in df.groupby("audio"):


        ground_truth = group.iloc[0]["ground_truth"]

        prediction = group.iloc[0]["prediction"]


        errors = (
            group["error_type"]
            .unique()
            .tolist()
        )


        result.append({

            "audio": audio,

            "ground_truth": ground_truth,

            "prediction": prediction,

            "errors": errors,

            "total_error": len(group)

        })


    return {

        "total_audio": len(result),

        "data": result

    }