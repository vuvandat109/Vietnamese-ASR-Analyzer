# -*- coding: utf-8 -*-

# =====================================================
# main.py
# Vietnamese ASR Analyzer API V10.6.1
# FastAPI + React Dashboard Compatible
# =====================================================


from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form
)


from fastapi.middleware.cors import CORSMiddleware


import json
import pandas as pd
import os
import shutil
import uuid



from whisper_engine import transcribe_audio


from audio_analyzer import (
    calculate_score,
    simple_error_check,
    analyze_sentence_phoneme
)





# =====================================================
# APP
# =====================================================


app = FastAPI(

    title="Vietnamese ASR Analyzer API",

    version="10.6.1"

)







# =====================================================
# CORS
# =====================================================


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







# =====================================================
# PATH
# =====================================================


BASE_DIR = r"E:\ASR_Project\dataset"


UPLOAD_DIR = r"E:\ASR_Project\web\backend\uploads"



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



STATISTICS_FILE = os.path.join(

    BASE_DIR,

    "error_statistics.json"

)





os.makedirs(

    UPLOAD_DIR,

    exist_ok=True

)









# =====================================================
# HOME
# =====================================================


@app.get("/")

def home():

    return {

        "message":

        "Vietnamese ASR Analyzer API running"

    }









# =====================================================
# HEALTH
# =====================================================


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

        os.path.exists(ANALYSIS_FILE),


        "statistics":

        os.path.exists(STATISTICS_FILE),


        "whisper":

        True

    }









# =====================================================
# OLD REPORT API
# React đang dùng
# =====================================================


@app.get("/report")

def report():


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


        return json.load(f)









# =====================================================
# OLD ERROR API
# =====================================================


@app.get("/errors")

def errors():


    if not os.path.exists(ERROR_FILE):

        return {

            "error":

            "Không tìm thấy file lỗi"

        }



    df = pd.read_csv(

        ERROR_FILE,

        encoding="utf-8-sig"

    )



    df=df.fillna("")



    result=[]



    for _,row in df.iterrows():

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


            "prediction":

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









# =====================================================
# OLD ANALYSIS API
# =====================================================


@app.get("/analysis")

def analysis():


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


        return json.load(f)









# =====================================================
# NEW STATISTICS API
# =====================================================


@app.get("/api/statistics")

def statistics():


    with open(

        STATISTICS_FILE,

        "r",

        encoding="utf-8"

    ) as f:


        return json.load(f)









# =====================================================
# AUDIO LIST
# =====================================================


@app.get("/api/audio-list")

def audio_list():


    with open(

        ANALYSIS_FILE,

        "r",

        encoding="utf-8"

    ) as f:


        data=json.load(f)



    result=[]



    for item in data["data"]:


        result.append({

            "audio":

            item["audio"],


            "wer":

            item["wer"],


            "cer":

            item["cer"],


            "status":

            item["status"]

        })



    return {


        "total":

        len(result),


        "data":

        result

    }









# =====================================================
# AUDIO DETAIL
# =====================================================


@app.get("/api/audio-detail/{audio}")

def audio_detail(audio:str):


    with open(

        ANALYSIS_FILE,

        "r",

        encoding="utf-8"

    ) as f:


        data=json.load(f)



    for item in data["data"]:


        if item["audio"] == audio:


            return item



    return {


        "error":

        "Không tìm thấy audio"

    }









# =====================================================
# UPLOAD ANALYZE
# =====================================================


@app.post("/upload-analyze")

async def upload_analyze(

    audio:UploadFile = File(...),

    reference:str = Form(...)

):


    filename = (

        str(uuid.uuid4())

        +

        "_"

        +

        audio.filename

    )



    path=os.path.join(

        UPLOAD_DIR,

        filename

    )





    with open(

        path,

        "wb"

    ) as f:


        shutil.copyfileobj(

            audio.file,

            f

        )





    prediction=transcribe_audio(path)



    score=calculate_score(

        reference,

        prediction

    )



    errors=simple_error_check(

        reference,

        prediction

    )



    word_analysis=analyze_sentence_phoneme(

        reference,

        prediction

    )



    return {


        "audio":

        audio.filename,


        "ground_truth":

        reference,


        "prediction":

        prediction,


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









# =====================================================
# START SERVER
# =====================================================


if __name__ == "__main__":


    import uvicorn


    uvicorn.run(

        app,

        host="127.0.0.1",

        port=8000

    )