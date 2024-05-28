from utils.constants import get_question_text_from_id
from utils.validation_funcs import (
    check_ambulatory_aid,
    check_appetite,
    check_cough_yes_or_no,
    check_denture,
    check_denture_followup,
    check_diet,
    check_food_preference,
    check_history_of_falling,
    check_sputum_amount,
    check_sputum_color,
    check_sputum_yes_or_no,
    check_vision,
    check_weight_loss_amount,
    check_weight_loss_existence,
)


def resolve_user_uttr(user_uttr, curr_question_id, grace_uttr_text, model_type):
    match curr_question_id:
        case "q0_greeting":
            res = {"next_question_key": "correct_next"}
        # cough / sputum
        case "q1_0_coughing_existance":
            res = check_cough_yes_or_no(
                user_uttr, curr_question_id, grace_uttr_text, model_type
            )
        case "q2_0_sputum_existance":
            res = check_sputum_yes_or_no(
                user_uttr, curr_question_id, grace_uttr_text, model_type
            )
        case "q2_1_sputum_amount":
            res = check_sputum_amount(
                user_uttr, curr_question_id, grace_uttr_text, model_type
            )
        case "q2_2_sputum_colour":
            res = check_sputum_color(
                user_uttr, curr_question_id, grace_uttr_text, model_type
            )
        # falling
        case "q3_0_history_falling":
            res = check_history_of_falling(
                user_uttr, curr_question_id, grace_uttr_text, model_type
            )
        case "q3_1_ambulatory_aid":
            res = check_ambulatory_aid(
                user_uttr, curr_question_id, grace_uttr_text, model_type
            )
        # vision
        case "q4_0_vision":
            res = check_vision(user_uttr, curr_question_id, grace_uttr_text, model_type)
        # lose weight
        case "q5_0_lose_weight_existance":
            res = check_weight_loss_existence(
                user_uttr, curr_question_id, grace_uttr_text, model_type
            )
        case "q5_1_lose_weight_amount":
            res = check_weight_loss_amount(
                user_uttr, curr_question_id, grace_uttr_text, model_type
            )
        case "q5_2_decreased_appetite":
            res = check_appetite(
                user_uttr, curr_question_id, grace_uttr_text, model_type
            )
        # dental
        case "q6_0_denture":
            res = check_denture(
                user_uttr, curr_question_id, grace_uttr_text, model_type
            )
        case "q6_1_dental_followup_fixed_or_removable":
            res = check_denture_followup(
                user_uttr, curr_question_id, grace_uttr_text, model_type
            )
        case "q7_0_diet":
            res = check_diet(user_uttr, curr_question_id, grace_uttr_text, model_type)
        case "q7_2_food_preference":
            res = check_food_preference(
                user_uttr, curr_question_id, grace_uttr_text, model_type
            )
        case _:
            res = {"error": "error"}
    return res
