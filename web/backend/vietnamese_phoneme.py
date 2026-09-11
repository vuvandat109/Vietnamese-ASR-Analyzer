# ==========================================
# vietnamese_phoneme.py
# Vietnamese syllable analyzer V8.2
# ==========================================



# ==========================================
# THANH ĐIỆU
# ==========================================


TONE_MAP = {


    "á":"sắc",
    "à":"huyền",
    "ả":"hỏi",
    "ã":"ngã",
    "ạ":"nặng",


    "ắ":"sắc",
    "ằ":"huyền",
    "ẳ":"hỏi",
    "ẵ":"ngã",
    "ặ":"nặng",


    "ấ":"sắc",
    "ầ":"huyền",
    "ẩ":"hỏi",
    "ẫ":"ngã",
    "ậ":"nặng",


    "é":"sắc",
    "è":"huyền",
    "ẻ":"hỏi",
    "ẽ":"ngã",
    "ẹ":"nặng",


    "ế":"sắc",
    "ề":"huyền",
    "ể":"hỏi",
    "ễ":"ngã",
    "ệ":"nặng",


    "í":"sắc",
    "ì":"huyền",
    "ỉ":"hỏi",
    "ĩ":"ngã",
    "ị":"nặng",


    "ó":"sắc",
    "ò":"huyền",
    "ỏ":"hỏi",
    "õ":"ngã",
    "ọ":"nặng",


    "ố":"sắc",
    "ồ":"huyền",
    "ổ":"hỏi",
    "ỗ":"ngã",
    "ộ":"nặng",


    "ớ":"sắc",
    "ờ":"huyền",
    "ở":"hỏi",
    "ỡ":"ngã",
    "ợ":"nặng",


    "ú":"sắc",
    "ù":"huyền",
    "ủ":"hỏi",
    "ũ":"ngã",
    "ụ":"nặng",


    "ứ":"sắc",
    "ừ":"huyền",
    "ử":"hỏi",
    "ữ":"ngã",
    "ự":"nặng",


    "ý":"sắc",
    "ỳ":"huyền",
    "ỷ":"hỏi",
    "ỹ":"ngã",
    "ỵ":"nặng"

}





# ==========================================
# LẤY THANH ĐIỆU
# ==========================================


def get_tone(word):


    for c in word.lower():


        if c in TONE_MAP:

            return TONE_MAP[c]



    return "ngang"







# ==========================================
# BỎ DẤU NHƯNG GIỮ ÂM ĐẶC BIỆT
# ==========================================


def remove_tone(word):


    table = str.maketrans(


        "áàảãạ"
        "ắằẳẵặ"
        "ấầẩẫậ"
        "éèẻẽẹ"
        "ếềểễệ"
        "íìỉĩị"
        "óòỏõọ"
        "ốồổỗộ"
        "ớờởỡợ"
        "úùủũụ"
        "ứừửữự"
        "ýỳỷỹỵ",



        "aaaaa"
        "ăăăăă"
        "âââââ"
        "eeeee"
        "êêêêê"
        "iiiii"
        "ooooo"
        "ôôôôô"
        "ơơơơơ"
        "uuuuu"
        "ưưưưư"
        "yyyyy"

    )


    return word.lower().translate(table)







# ==========================================
# PHỤ ÂM ĐẦU
# ==========================================


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


    "đ",

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







# ==========================================
# ÂM CUỐI
# ==========================================


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








# ==========================================
# NGUYÊN ÂM ĐÔI
# ==========================================


VOWELS = [

    "iê",

    "yê",

    "uô",

    "ươ",

    "oa",

    "oe",

    "uy",

    "ua",

    "ia",

    "ay",

    "ai",

    "ao",

    "au",

    "âu",

    "ôi",

    "ơi",

    "ui",

    "eo",

    "êu"


]








# ==========================================
# TÁCH ÂM TIẾT
# ==========================================


def split_syllable(word):


    clean = remove_tone(word)



    result = {


        "initial":"",

        "nucleus":"",

        "final":""


    }



    # ------------------
    # phụ âm đầu
    # ------------------


    for i in INITIALS:


        if clean.startswith(i):


            result["initial"] = i


            clean = clean[len(i):]


            break






    # ------------------
    # âm cuối
    # ------------------


    for f in FINALS:


        if clean.endswith(f):


            result["final"] = f


            clean = clean[:-len(f)]


            break






    # ------------------
    # âm chính
    # ------------------


    result["nucleus"] = clean



    return result







# ==========================================
# SO SÁNH HAI TỪ
# ==========================================


def analyze_word(reference, prediction):


    ref = split_syllable(reference)


    hyp = split_syllable(prediction)




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

            get_tone(reference),



            "prediction":

            get_tone(prediction),



            "correct":

            get_tone(reference)

            ==

            get_tone(prediction)


        }



    }