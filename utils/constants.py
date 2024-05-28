import random
from dotenv import load_dotenv
import os

load_dotenv()
# ---------------------------------------------
# [DICT] API INFO
# --------------------------------------------
API_INFO = {
    "api_key": os.getenv("HKUST_OPENAI_KEY"),
    "azure_endpoint": os.getenv("HKUST_OPENAI_BASE"),
    "api_version": os.getenv("HKUST_OPENAI_API_VERSION"),
    "model": "gpt-4",
}

# ---------------------------------------------
# [list] QUESTION TEXTS
# --------------------------------------------
# TODO: improvement can be expended with more texts and read from csv files
q0_greeting_texts = ["你好啊！我喺 Grace。你今日覺得點啊？"]
q0_greeting_texts_eng = ["Hello, my name is Grace, how are you?"]
q1_0_coughing_existance_texts = [
    "請問你有冇咳？",
    # From Rosita
    "請問你有冇咳呀？",
    "你有冇咳呀？",
]  # some random ones for testing
q1_0_coughing_existance_texts_eng = [
    "Have you been coughing？"
]  # some random ones for testing
q2_0_sputum_existance_texts = [
    "請問有冇痰？",
    "有冇痰呀？",
    "請問有冇痰呀？",
]
q2_0_sputum_existance_texts_eng = [
    "Do you have sputum？",
    "Have you coughed up any sputum?"
]
q2_1_sputum_amount_texts = [
    "有痰，咁係多痰定少少呢？",
    "有痰，咁係多痰定少少痰？",
    "有痰，咁多定少呀？",
    "係好多痰，定係少少痰呀？",
]
q2_1_sputum_amount_texts_eng = [
    "Would you say a lot, or just a little?",
    "Would you say a lot of sputum, or just a little?"
]
q2_2_sputum_colour_texts = [
    "痰係咩顏色架？",
    "啲痰係乜嘢顏色？",
    "啲痰通常係乜嘢顏色？",
]
q2_2_sputum_colour_texts_eng = [
    "What's the colour of your sputum?",
    "What colour is it?",
    "Could you describe the colour?"
]
q3_0_history_falling_texts = [
    "請問你過去嗰三個月有冇試過跌親？",
    "請問你過去嗰三個月有冇試過跌親呀？",
    "你最近嗰三個月有冇試過跌親？",
    "你過去嗰三個月有冇跌親過呀？",
]
q3_0_history_falling_texts_eng = [
    "Have you had a fall within the past three months?",
    "Have you experienced a fall over the past three months?"
]
q3_1_ambulatory_aid_texts = [
    "你平時行路洗唔洗揸住或者扶住野架？",
    "你平時行路使唔使揸拐杖或者扶住嘢㗎？",
    "你平時行路洗唔洗揸住支棍或者其他嘢呀？",
    "你平時行路需唔需要揸住支棍或者其他嘢呀？",
    "你使唔使揸拐杖或者扶住嘢行路架？",
]
q3_1_ambulatory_aid_texts_eng = [
    "Do you need to hold on to something, or require a walking stick when walking?",
    "Do you normally need to use a cane or hold onto anything when you walk?"
]
q4_0_vision_texts = [
    "請問你嘅視力好唔好？睇野清唔清楚呀？",
    "你嘅視力係咪正常呀？",
    "你嘅視力有冇問題呀？",
    "你睇嘢有冇困難呀？",
]
q4_0_vision_texts_eng = [
    "How is your eyesight, are you able to see clearly?",
    "Do you have trouble seeing?",
]
q5_0_lose_weight_existance_texts = [
    "請問你過去嗰三個月有冇無端端輕左？",
    "近三個月你有冇發現自己嘅體重輕咗？",
    "最近三個月你有冇瘦咗啲？",
    "請問你之前三個月有冇突然輕咗？ ",
    "你喺過去三個月有冇無緣無故變瘦？",
    "你之前三個月有冇無緣無故變輕咗？",
]
q5_0_lose_weight_existance_texts_eng = [
    "Have you experienced unintended weight loss over the past three months?",
    "Have you had unintentional weight loss over the past three months?",
    "Have you lost weight without trying over the past three months?"
]
q5_1_lose_weight_amount_texts = [
    "輕左幾多呀？",
    "輕左幾多磅呀？",
]
q5_1_lose_weight_amount_texts_eng = [
    "How much weight have you lost?",
    "How many kilograms did you lose?"
]
q5_2_decreased_appetite_texts = [
    "胃口有冇差到？",
    "胃口有冇變差？",
    "胃口點呀？有冇唔想食嘢？",
]
q5_2_decreased_appetite_texts_eng = [
    "Have you been experiencing a loss of appetite?",
    "Have you been experiencing a loss in appetite?",
    "Has your appetite gotten worse?"
]
q6_0_denture_texts = [
    "請問你有冇假牙呀？",
    "你使唔使用假牙㗎？",
    "請問你有冇用假牙？",
]
q6_1_dental_followup_fixed_or_removable_texts = [
    "係鑲落去定係戴嘅假牙？",
    "你個假牙係鑲落去嗰啲，定係戴嗰啲假牙嚟㗎？",
    "係鑲落去定係戴嘅假牙嚟㗎？",
]
q7_0_diet_texts = [
    "你有冇需要食一啲特別餐㗎？",
    "對於你嘅飲食方面，有冇任何特別要求或者限制？",
    # "關於飲食，你有冇任何特別嘅營養需求或者醫囑要遵循嘅？", 醫囑
    # From Rosita
    "你使唔使食特別餐㗎？",
    "你食嘢係食普通嗰啲，定係食特別餐㗎？",
]
q7_0_diet_texts_eng = [
    "Do you have any dietary requirements?",
    "Do you have any special dietary needs or restrictions?"
]
q7_1_thickener_for_dysphagia_texts = [
    "你有冇需要用食物凝固粉？",
    # From Rosita
    "你食野需唔需要加食物凝固粉？",
    "你需唔需要加凝固粉落去嘢食度㗎？",
]
q7_2_food_preference_texts = [
    "你有冇特別嘅嘢唔食㗎？",
    "你有冇嘢係特別唔食㗎？"
    # "你有冇特別嘅嘢唔食㗎？ 例如豬，牛，雞？ 又或者你係食素嘅？",
    # # From Rosita
    # "你有冇特別嘅嘢唔食㗎？例如豬，牛，雞？又或者你係食齋嘅？",
    # "你有冇嘢係特別唔食㗎？例如豬，牛，雞？又或者你係食素嘅？",
    # "你有冇嘢係特別唔食㗎？例如豬，牛，雞？又或者你係食齋嘅？",
]  # no beef
q7_2_food_preference_texts_eng = [
    "Are there any foods in particular which you don't eat?",
    "Is there anything in particular you don't eat?"
]
closing_texts = [
    "好多謝你嘅時間，我已經將你所有嘅答案記錄曬。"
    # "多謝你答曬全部嘅問題。我哋已經錄咗晒你嘅答案，而家問卷部分就算完成。",
    # "多謝你嘅回答，你提供嘅信息我哋已經處理好，問卷到此結束。",
]

closing_texts_eng = [
    "Thank you very much for your time, I have recorded all your answers."
    # "多謝你答曬全部嘅問題。我哋已經錄咗晒你嘅答案，而家問卷部分就算完成。",
    # "多謝你嘅回答，你提供嘅信息我哋已經處理好，問卷到此結束。",
]
# ---------------------------------------------
# [dict] QUESTION ID TO TEXTS
# --------------------------------------------
question_id_to_texts = {
    "initial_status": ["你好啊！我喺 Grace。你今日覺得點啊？"],
    "q0_greeting": q0_greeting_texts,
    "q0_greeting_eng": q0_greeting_texts_eng,
    "q1_0_coughing_existance_eng": q1_0_coughing_existance_texts_eng,
    "q2_0_sputum_existance_eng": q2_0_sputum_existance_texts_eng,
    "q1_0_coughing_existance": q1_0_coughing_existance_texts,
    "q2_0_sputum_existance": q2_0_sputum_existance_texts,
    "q2_1_sputum_amount": q2_1_sputum_amount_texts,
    "q2_1_sputum_amount_eng": q2_1_sputum_amount_texts_eng,
    "q2_2_sputum_colour": q2_2_sputum_colour_texts,
    "q2_2_sputum_colour_eng": q2_2_sputum_colour_texts_eng,
    "q3_0_history_falling": q3_0_history_falling_texts,
    "q3_0_history_falling_eng": q3_0_history_falling_texts_eng,
    "q3_1_ambulatory_aid": q3_1_ambulatory_aid_texts,
    "q3_1_ambulatory_aid_eng": q3_1_ambulatory_aid_texts_eng,
    "q4_0_vision": q4_0_vision_texts,
    "q4_0_vision_eng": q4_0_vision_texts_eng,
    "q5_0_lose_weight_existance": q5_0_lose_weight_existance_texts,
    "q5_0_lose_weight_existance_eng": q5_0_lose_weight_existance_texts_eng,
    "q5_1_lose_weight_amount": q5_1_lose_weight_amount_texts,
    "q5_1_lose_weight_amount_eng": q5_1_lose_weight_amount_texts_eng,
    "q5_2_decreased_appetite": q5_2_decreased_appetite_texts,
    "q5_2_decreased_appetite_eng": q5_2_decreased_appetite_texts_eng,
    "q6_0_denture": q6_0_denture_texts,
    "q6_1_dental_followup_fixed_or_removable": q6_1_dental_followup_fixed_or_removable_texts,
    "q7_0_diet": q7_0_diet_texts,
    "q7_0_diet_eng": q7_0_diet_texts_eng,
    "q7_1_thickener_for_dysphagia": q7_1_thickener_for_dysphagia_texts,
    "q7_2_food_preference": q7_2_food_preference_texts,  # no beef
    "q7_2_food_preference_eng": q7_2_food_preference_texts_eng,  # no beef
    "closing": closing_texts,
    "closing_eng": closing_texts_eng,
}


# ---------------------------------------------
# [function] MAP QUESTION ID TO TEXT
# --------------------------------------------
def get_question_text_from_id(question_id: str, avoid_question: str = None):
    random_question = random.choice(question_id_to_texts[question_id])
    while random_question == avoid_question:
        random_question = random.choice(question_id_to_texts[question_id])
    return random_question


# ---------------------------------------------
# [dict] (QUESTION ID, SLOT-FILLED) TO ACKNOELDGEMENT TEXTS
# --------------------------------------------
preset_acknowledgement_binary = {
    ("q1_0_coughing_existance", "no"): ["收到。", "冇咳。", "冇。", "係。"],
    ("q1_0_coughing_existance", "yes"): [""],
    ("q4_0_vision", "yes"): [""],  # your eye sight is good. "你嘅視力好."
    ("q4_0_vision", "no"): [""],  # your eye sight is bad. "你嘅視力唔好."
    ("q5_2_decreased_appetite", "yes"): [
        "係。",
        "收到。",
    ],  # your appetite is bad. "胃口差."
    ("q5_2_decreased_appetite", "no"): ["好嘅。"],  # your appetite is good. "胃口好."
    ("q6_0_denture", "no"): [
        "冇假牙。",
    ],
    ("q6_0_denture", "yes"): [
        "有假牙。",
    ],
    ("q6_1_dental_followup_fixed_or_removable", "removable"): ["明白。", "收到。"],
    # ("q2_2_sputum_colour", )
    ("q3_0_history_falling", "no"): ["冇跌親就好啦。"],  # you haven't felt.
}

# emergency help
emergency_help_text = "唔好意思, 我而家即刻搵個護士嚟幫手"
#"冇問題, 我明白, 我搵個護士嚟幫手"

# @nicholas
confused_patient_handling_text = "唔該你等等吓, 我而家搵個護士嚟同你傾吓偈"
