import random

# from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_openai import AzureChatOpenAI, ChatOpenAI

from dotenv import load_dotenv
import os

from utils.constants import (
    API_INFO,
    get_question_text_from_id,
    preset_acknowledgement_binary
)

# ===== SETUP ====================================================
load_dotenv()
azure_model = AzureChatOpenAI(
    azure_endpoint=API_INFO["azure_endpoint"],
    api_key=API_INFO["api_key"],
    api_version=API_INFO["api_version"],
    openai_api_type="azure",
    azure_deployment=API_INFO[
        "model"
    ],  # This is the key part. This is extracted from the HKUST curl posts
    verbose=True,
)

vender_model_4 = ChatOpenAI(
    base_url=os.getenv("VENDER_BASE_URL"),
    api_key=os.getenv("VENDER_API_KEY"),
    model="gpt-4-turbo-2024-04-09",
    verbose=True,
)

vender_model_4o = ChatOpenAI(
    base_url=os.getenv("VENDER_BASE_URL"),
    api_key=os.getenv("VENDER_API_KEY"),
    model="gpt-4o-2024-05-13",
    verbose=True,
)

llm_models = [azure_model, vender_model_4, vender_model_4o]


# this will change the way that they ask the question
def repeat_question(curr_question_id, avoid_question):
    return {
        "grace_response": get_question_text_from_id(curr_question_id, avoid_question),
        "next_question_status": curr_question_id,
    }

def make_acknowledgement(curr_question_id, slot_filled):
    acknowledgement = preset_acknowledgement_binary.get(
        (curr_question_id, slot_filled), ""
    )
    if acknowledgement != "":
        acknowledgement = random.choice(acknowledgement)
    return acknowledgement

# TODO: @Nicholas
EMERGENCY_HANDLING_PROMPT = "You are a robot nurse who is conducting patient assessment form survey in Cantonese.\
    Is the patient being uncooperative? Answer yes only if the patient refuses to answer and is upset and curses or is afraid of you and wants to speak to a human nurse. \
    Choose between two options: Yes, No.\n\
    [Dialogue]\nNurse: {grace_uttr_text}\nPatient: {user_uttr}."

def run_gpt_parallel(main_task_prompt, user_uttr, grace_uttr_text, model_type, sub_prompt_dict=None):
    '''
        args:
            main_task_prompt: the prompt for the main current question
            user_uttr: the user utterance
            grace_uttr_text: the grace utterance
            sub_prompt: the sub prompt_text for the follow up questions
    '''
    model = llm_models[model_type]
    main_chain = ChatPromptTemplate.from_template("{prompt}") | model
    emergency_chain = (ChatPromptTemplate.from_template(EMERGENCY_HANDLING_PROMPT)| model)

    sub_prompt = ''
    if sub_prompt_dict is not None:
        sub_prompt = sub_prompt_dict['prompt']
        sub_chain = ChatPromptTemplate.from_template("{sub_prompt}") | model
        map_chain = RunnableParallel(main_task=main_chain, 
                                     emergency_check=emergency_chain,
                                     sub_task=sub_chain)
    else:
        map_chain = RunnableParallel(main_task=main_chain, 
                                     emergency_check=emergency_chain)
        
    res = map_chain.invoke(
        {
            "prompt": main_task_prompt,
            "sub_prompt": sub_prompt,
            "user_uttr": user_uttr,
            "grace_uttr_text": grace_uttr_text,
        }
    )

    main_task_response = res["main_task"].content.lower().strip()
    emergency_response = res["emergency_check"].content.lower().strip()
    sub_task_response = None if sub_prompt == '' else res["sub_task"].content.lower().strip()

    return main_task_response, emergency_response, sub_task_response

# ======= Handling questions ============================================

# decide next_question_id
# def get_next_question_id(curr_question_id, main_task_response, has_follow_up=False, follow_up_sanity_check=False):
def get_next_question_key(main_task_response, has_follow_up=False, follow_up_sanity_check=False):
    if not has_follow_up:
        key = "correct_next"
    else: 
        if main_task_response == "yes":
            key = "sub_skip" if follow_up_sanity_check else "yes"
        elif main_task_response == "no":
            key = "no"
        else:
            key = "skip"
    # return get_next_question_tree[curr_question_id][key]
    return key

def check_main_task_satisfy(curr_question_id, main_task_response, sub_task_response):
    if curr_question_id == 'q5_0_lose_weight_existance':
        return main_task_response == "yes" and sub_task_response not in ['na', '0kg', 'unclear']
    return False

def handle_question(
    user_uttr,
    grace_uttr_text,
    curr_question_id,
    slot_filling_key,
    prompt,
    model_type,
    original_question,
    has_follow_up=False,
    sub_prompt_dict=None,
):
    
    main_task_response, emergency_response, sub_task_response = run_gpt_parallel(
                                            main_task_prompt=prompt, user_uttr=user_uttr, grace_uttr_text=grace_uttr_text, sub_prompt_dict=sub_prompt_dict, model_type=model_type
                                        )
    sub_task_sanity_check = False
    if emergency_response == "yes":
        return {
            "emergency_help_needed": emergency_response,
        }
    elif main_task_response == "unclear":  # repeat
        return repeat_question(curr_question_id, avoid_question=original_question)
    else:
        slot_filling = {slot_filling_key: main_task_response} 

        # adding sub_prompt_result
        if sub_prompt_dict:
            sub_task_sanity_check = check_main_task_satisfy(curr_question_id, main_task_response, sub_task_response)
            if sub_task_sanity_check:
                slot_filling[sub_prompt_dict['slot_filling_key']] = sub_task_response  

        next_question_key = get_next_question_key(
                            main_task_response,
                            has_follow_up=has_follow_up,
                            follow_up_sanity_check=sub_task_sanity_check)
        
        return {
            "next_question_key": next_question_key,
            "slot_filling": slot_filling,
            "acknowledgement": make_acknowledgement(curr_question_id, main_task_response),
            "emergency_help_needed": emergency_response,
        }

# ======= QUESTION CUSTOMIZED PROMPTS ============================================
def check_cough_yes_or_no(user_uttr, curr_question_id, grace_uttr_text, model_type):
    '''
        curr_question_id == q1_0_coughing_existance
    '''
    prompt = f"Evaluate if the patient has experienced coughing. Choose between two options: Yes, No.\n\
If the patient does not answer the question, choose UNCLEAR.\n\n\
[Dialogue]\nNurse: {grace_uttr_text}\nPatient: {user_uttr}."

    return handle_question(
        user_uttr,
        grace_uttr_text,
        curr_question_id,
        model_type=model_type,
        slot_filling_key="cough_existence",
        prompt=prompt,
        original_question=grace_uttr_text,
    )


def check_sputum_yes_or_no(user_uttr, curr_question_id, grace_uttr_text, model_type):
    '''
        * have follow-up-question
        curr_question_id == q2_0_sputum_existance
    '''
    prompt = f"Evaluate if the patient has experienced sputum. Choose between two options: Yes, No.\n\
If the patient does not answer the question, choose UNCLEAR.\n\n\
[Dialogue]\nNurse: {grace_uttr_text}\nPatient: {user_uttr}."

    # FOLLOW UP QUESTION HANDLING
    return handle_question(
        user_uttr,
        grace_uttr_text,
        curr_question_id,
        slot_filling_key="sputum_existence",
        prompt=prompt,
        model_type=model_type,
        original_question=grace_uttr_text,
        has_follow_up=True
    )


def check_sputum_amount(user_uttr, curr_question_id, grace_uttr_text, model_type):
    '''
        curr_question_id == q2_1_sputum_amount
    '''
    prompt = f"Evaluate how much sputum the patient has experienced. Answer concisely.\n\
If the patient does not answer the question, generate UNCLEAR.\n\n\
[Dialogue]\nNurse: {grace_uttr_text}\nPatient: {user_uttr}."

    return handle_question(
        user_uttr,
        grace_uttr_text,
        curr_question_id,
        model_type=model_type,
        slot_filling_key="sputum_amount",
        prompt=prompt,
        original_question=grace_uttr_text,
    )


def check_sputum_color(user_uttr, curr_question_id, grace_uttr_text, model_type):
    '''
        curr_question_id == q2_2_sputum_colour
    '''
    prompt = f"Evaluate sputum color of the patient. Only generate color.\n\
If the patient does not answer the question, generate UNCLEAR.\n\n\
[Dialogue]\nNurse: {grace_uttr_text}\nPatient: {user_uttr}."

    return handle_question(
        user_uttr,
        grace_uttr_text,
        curr_question_id,
        model_type=model_type,
        slot_filling_key="sputum_color",
        prompt=prompt,
        original_question=grace_uttr_text,
    )


def check_history_of_falling(user_uttr, curr_question_id, grace_uttr_text, model_type):
    '''
        curr_question_id == q3_0_history_falling
    ''' 
    prompt = f"Evaluate if the patient has experienced falling. Choose between two options: Yes, No\n\
If the patient does not answer the question, generate UNCLEAR.\n\n\
[Dialogue]\nNurse: {grace_uttr_text}\nPatient: {user_uttr}."

    return handle_question(
        user_uttr,
        grace_uttr_text,
        curr_question_id,
        model_type=model_type,
        slot_filling_key="history_of_falling",
        prompt=prompt,
        original_question=grace_uttr_text,
    )


def check_ambulatory_aid(user_uttr, curr_question_id, grace_uttr_text, model_type):
    prompt = f"Evaluate if the patient has require walking aids or need to grab onto something when you walk.\
Choose among three options: None/Best rest/Nurse assist, Crutches/Cane/Walkers, Furniture\n\
If the patient does not answer the question, generate UNCLEAR.\n\n\
[Dialogue]\nNurse: {grace_uttr_text}\nPatient: {user_uttr}."

    return handle_question(
        user_uttr,
        grace_uttr_text,
        curr_question_id,
        model_type=model_type,
        slot_filling_key="ambulatory_aid",
        prompt=prompt,
        original_question=grace_uttr_text,
    )


# Q4 VISION
def check_vision(user_uttr, curr_question_id, grace_uttr_text, model_type):
    '''
        curr_question_id == q4_0_vision
    ''' 
    prompt = f"Evaluate if the patient has issue with vision. Choose between two options: Yes, No.\
If the patient does not answer the question, generate UNCLEAR.\n\n\
[Dialogue]\nNurse: {grace_uttr_text}\nPatient: {user_uttr}."

    return handle_question(
        user_uttr,
        grace_uttr_text,
        curr_question_id,
        model_type=model_type,
        slot_filling_key="vision_problem",
        prompt=prompt,
        original_question=grace_uttr_text,
    )


def check_weight_loss_existence(user_uttr, curr_question_id, grace_uttr_text, model_type):
    '''
        * has follow up 
        curr_question_id == q5_0_lose_weight_existance
    ''' 
    main_prompt = f"Evaluate if the patient has experienced weight loss. Choose between two options: Yes, No.\n\
If the patient does not answer the question, choose UNCLEAR.\n\n\
[Dialogue]\nNurse: {grace_uttr_text}\nPatient: {user_uttr}."

    sub_followup_prompt = f"Evaluate how much the patient lost the weight, choose one of the categories: 0kg, 1-5kg, 6-10kg, 11-15kg, >15kg.\n\
If the patient did NOT state the amount in number, return NA.\n\
[Dialogue]\nNurse: {grace_uttr_text}\nPatient: {user_uttr}."
    sub_followup_slot_filling_key = "weight_loss_amount"

     # FOLLOW UP QUESTION HANDLING
    return handle_question(
        user_uttr,
        grace_uttr_text,
        curr_question_id,
        model_type=model_type,
        slot_filling_key="weight_loss_existance",
        prompt=main_prompt,
        original_question=grace_uttr_text,
        has_follow_up=True,
        sub_prompt_dict={"prompt": sub_followup_prompt, "slot_filling_key": sub_followup_slot_filling_key}
    )

def check_weight_loss_amount(user_uttr, curr_question_id, grace_uttr_text, model_type):
    '''
        curr_question_id == q5_1_lose_weight_amount
    ''' 
    prompt = f"Evaluate how much the patient lost the weight. Choose one of the categories: 1-5kg, 6-10kg, 11-15kg, >15kg, Unsure\n\
If the patient does not answer the question, choose UNCLEAR.\n\n\
[Dialogue]\nNurse: {grace_uttr_text}\nPatient: {user_uttr}."

    return handle_question(
        user_uttr,
        grace_uttr_text,
        curr_question_id,
        model_type=model_type,
        slot_filling_key="weight_loss_amount",
        prompt=prompt,
        original_question=grace_uttr_text,
    )

def check_appetite(user_uttr, curr_question_id, grace_uttr_text, model_type):
    '''
        curr_question_id == q5_2_decreased_appetite
    ''' 
    prompt = f"Evaluate if the patient have been eating poorly because of decreased appetite. Choose between two options: Yes, No.\n\
If the patient does not answer the question, choose UNCLEAR.\n\n\
[Dialogue]\nNurse: {grace_uttr_text}\nPatient: {user_uttr}."

    return handle_question(
        user_uttr,
        grace_uttr_text,
        curr_question_id,
        model_type=model_type,
        slot_filling_key="appetite_loss",
        prompt=prompt,
        original_question=grace_uttr_text,
    )


def check_denture(user_uttr, curr_question_id, grace_uttr_text, model_type):
    '''
        curr_question_id == q6_0_denture
    ''' 
    prompt = f"Evaluate if the patient got a denture, Choose between two options: Yes, No.\n\
If the patient does not answer the question, choose UNCLEAR.\n\n\
[Dialogue]\nNurse: {grace_uttr_text}\nPatient: {user_uttr}."

    # FOLLOW UP QUESTION HANDLING
    return handle_question(
        user_uttr,
        grace_uttr_text,
        curr_question_id,
        model_type=model_type,
        slot_filling_key="denture",
        prompt=prompt,
        original_question=grace_uttr_text,
        has_follow_up=True
    )


def check_denture_followup(user_uttr, curr_question_id, grace_uttr_text, model_type):
    '''
        curr_question_id == q6_1_dental_followup_fixed_or_removable
    ''' 
    prompt = f"Evaluate if the patient got fixed denture or removable denture, Choose between two options: fixed, removable.\n\
If the patient does not answer the question, choose UNCLEAR.\n\n\
[Dialogue]\nNurse: {grace_uttr_text}\nPatient: {user_uttr}."

    return handle_question(
        user_uttr,
        grace_uttr_text,
        curr_question_id,
        model_type=model_type,
        slot_filling_key="denture_option",
        prompt=prompt,
        original_question=grace_uttr_text,
    )


def check_diet(user_uttr, curr_question_id, grace_uttr_text, model_type):
    '''
        curr_question_id == q7_0_diet
    ''' 
    prompt = f"Evaluate if the patient has any special diet. Choose between two options: yes or no.\n\
If the patient does not answer the question, choose UNCLEAR.\n\n\
[Dialogue]\nNurse: {grace_uttr_text}\nPatient: {user_uttr}."

    return handle_question(
        user_uttr,
        grace_uttr_text,
        curr_question_id,
        model_type=model_type,
        slot_filling_key="special_diet",
        prompt=prompt,
        original_question=grace_uttr_text,
    )


def check_food_preference(user_uttr, curr_question_id, grace_uttr_text, model_type):
    '''
        curr_question_id == q7_2_food_preference
    ''' 
    prompt = f"Evaluate if the patient has any food preference. Choose from these categories: No preference, fish only, no beef, no pork, no chicken, vegetarian, others\n\
If the option is others, please specify the food preference based on the patient's answer.\n\
If the patient does not answer the question, choose UNCLEAR.\n\n\
[Dialogue]\nNurse: {grace_uttr_text}\nPatient: {user_uttr}."

    return handle_question(
        user_uttr,
        grace_uttr_text,
        curr_question_id,
        model_type=model_type,
        slot_filling_key="food_preference",
        prompt=prompt,
        original_question=grace_uttr_text,
    )
