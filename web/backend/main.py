from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import json
import pandas as pd
import os


# =====================================
# KHỞI TẠO FASTAPI
# =====================================

app = FastAPI(
    title="Vietnamese ASR Analyzer API",
    version="4.0"
)



# =====================================
# CHO PHÉP REACT GỌI API
# =====================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)



# =====================================
# ĐƯỜNG DẪN DATASET
# =====================================

BASE_DIR = r"E:\ASR_Project\dataset"


REPORT_FILE = os.path.join(
    BASE_DIR,
    "summary_report.json"
)


ERROR_FILE = os.path.join(
    BASE_DIR,
    "vietnamese_error_analysis.csv"
)


ANALYSIS_FILE = os.path.join(
    BASE_DIR,
    "sentence_analysis.json"
)



# =====================================
# TRANG KIỂM TRA
# =====================================

@app.get("/")
def home():

    return {

        "message":
        "Vietnamese ASR Analyzer API running"

    }




# =====================================
# LẤY BÁO CÁO TỔNG QUAN
# =====================================

@app.get("/report")
def get_report():


    if not os.path.exists(REPORT_FILE):

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





# =====================================
# LẤY LỖI TOKEN CHI TIẾT
# =====================================

@app.get("/errors")
def get_errors():


    if not os.path.exists(ERROR_FILE):

        return {

            "error":
            "Không tìm thấy vietnamese_error_analysis.csv"

        }



    df = pd.read_csv(

        ERROR_FILE,

        encoding="utf-8-sig"

    )


    df = df.fillna("")



    result = []



    for _, row in df.iterrows():


        result.append({

            "audio":
            row.get(
                "audio",
                ""
            ),


            "reference":
            row.get(
                "reference_word",
                ""
            ),


            "hypothesis":
            row.get(
                "hypothesis_word",
                ""
            ),


            "error_type":
            row.get(
                "error_type",
                ""
            )

        })



    return {

        "total":
        len(result),


        "data":
        result

    }





# =====================================
# PHÂN TÍCH THEO CÂU (V4)
# =====================================

@app.get("/analysis")
def sentence_analysis():


    if not os.path.exists(ANALYSIS_FILE):

        return {

            "error":
            "Không tìm thấy sentence_analysis.json"

        }



    with open(

        ANALYSIS_FILE,

        "r",

        encoding="utf-8"

    ) as f:


        data = json.load(f)



    return data





# =====================================
# CHẠY KIỂM TRA
# =====================================

@app.get("/health")
def health():


    return {


        "status":
        "OK",


        "report":
        os.path.exists(REPORT_FILE),


        "errors":
        os.path.exists(ERROR_FILE),


        "analysis":
        os.path.exists(ANALYSIS_FILE)

    }