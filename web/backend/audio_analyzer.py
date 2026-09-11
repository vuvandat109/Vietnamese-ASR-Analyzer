import jiwer

from vietnamese_phoneme import analyze_word



# =====================================
# TÍNH WER / CER
# =====================================


def calculate_score(reference, prediction):


    wer = jiwer.wer(
        reference,
        prediction
    )


    cer = jiwer.cer(
        reference,
        prediction
    )


    return {

        "wer":
        round(wer,4),


        "cer":
        round(cer,4)

    }






# =====================================
# PHÂN TÍCH LỖI CƠ BẢN
# =====================================


def simple_error_check(reference, prediction):


    errors = []


    if reference.strip() == prediction.strip():

        return errors



    ref_words = reference.split()

    hyp_words = prediction.split()



    if len(ref_words) != len(hyp_words):

        errors.append(
            "multi_component_error"
        )

        return errors





    for r, h in zip(
        ref_words,
        hyp_words
    ):


        if r != h:


            try:

                detail = analyze_word(
                    r,
                    h
                )



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



            except Exception:


                errors.append(
                    "word_error"
                )



    return list(set(errors))





# =====================================
# PHÂN TÍCH TỪ SAI CHI TIẾT
# =====================================


def analyze_sentence_phoneme(
        reference,
        prediction
):


    ref_words = reference.split()


    hyp_words = prediction.split()



    result=[]



    max_len=max(
        len(ref_words),
        len(hyp_words)
    )




    for i in range(max_len):


        ref = (

            ref_words[i]

            if i < len(ref_words)

            else ""

        )



        hyp = (

            hyp_words[i]

            if i < len(hyp_words)

            else ""

        )





        # chỉ phân tích từ sai

        if ref != hyp and ref and hyp:



            try:


                detail = analyze_word(
                    ref,
                    hyp
                )


            except Exception as e:


                detail={

                    "error":
                    str(e)

                }




            result.append({

                "reference":

                ref,



                "prediction":

                hyp,



                "detail":

                detail


            })




    return result







# =====================================
# PHÂN TÍCH TOÀN BỘ AUDIO
# =====================================


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

        reference,



        "prediction":

        prediction,



        "wer":

        score["wer"],



        "cer":

        score["cer"],



        "status":

        "Đúng"

        if len(errors)==0

        else

        "Sai",




        "errors":

        errors,




        "word_analysis":

        word_analysis



    }