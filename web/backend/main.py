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
    simple_error_check
)





# =====================================
# FASTAPI
# =====================================

app = FastAPI(

    title="Vietnamese ASR Analyzer API",

    version="6.0"

)





# =====================================
# CORS
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
# PATH
# =====================================


BASE_DIR = r"E:\ASR_Project\dataset"


UPLOAD_DIR = (
    r"E:\ASR_Project\web\backend\uploads"
)



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





# tạo thư mục upload nếu chưa có

os.makedirs(

    UPLOAD_DIR,

    exist_ok=True

)








# =====================================
# HOME
# =====================================


@app.get("/")

def home():


    return {

        "message":

        "Vietnamese ASR Analyzer API running"

    }








# =====================================
# REPORT
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


        return json.load(f)








# =====================================
# ERROR DETAIL
# =====================================


@app.get("/errors")

def get_errors():


    if not os.path.exists(ERROR_FILE):

        return {

            "error":

            "Không tìm thấy file lỗi"

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
# SENTENCE ANALYSIS
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


        return json.load(f)










# =====================================
# HEALTH CHECK
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

        os.path.exists(ANALYSIS_FILE),


        "whisper":

        True

    }









# =====================================
# V6 UPLOAD AUDIO ANALYZE
# =====================================


@app.post("/upload-analyze")

async def upload_analyze(


    audio: UploadFile = File(...),


    reference: str = Form(...)


):


    # tạo tên file


    filename = (

        str(uuid.uuid4())

        +

        "_"

        +

        audio.filename

    )



    save_path = os.path.join(

        UPLOAD_DIR,

        filename

    )




    # lưu audio


    with open(

        save_path,

        "wb"

    ) as buffer:


        shutil.copyfileobj(

            audio.file,

            buffer

        )





    # Whisper nhận dạng


    prediction = transcribe_audio(

        save_path

    )





    # WER CER


    score = calculate_score(

        reference,

        prediction

    )





    # lỗi


    errors = simple_error_check(

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

        errors


    }