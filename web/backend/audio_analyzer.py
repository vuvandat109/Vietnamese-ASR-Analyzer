import jiwer


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
        "wer": round(wer, 4),
        "cer": round(cer, 4)
    }



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


    else:

        for r, h in zip(
            ref_words,
            hyp_words
        ):

            if r != h:

                errors.append(
                    "word_error"
                )


    return list(set(errors))