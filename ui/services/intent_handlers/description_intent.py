import streamlit as st
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load the trained model and tokenizer
model_path = 'ui/services/intent_handlers/models/test-squad-trained'
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForQuestionAnswering.from_pretrained(model_path)

def description_pipeline(user_input):
    query_params = st.experimental_get_query_params()
    course = query_params.get("course", [None])[0]
    # st.write(course)
    df = pd.read_csv("assistant/data/courssistant_main.csv")

    if course is None:
        responses = "Look like you try asking about information in a course, please navigate to the course page to use this feature 😚"
    else:
        context = get_context()
        # st.write(context)
        responses = question_answering(context, user_input)
    return  df, responses

def get_context():
    query_params = st.experimental_get_query_params()
    # Extract the parameters if they exist, otherwise set them to None
    course = query_params.get("course", [None])[0]
    level = query_params.get("level", [None])[0]
    rate = query_params.get("rate", [None])[0]
    description = query_params.get("description", [None])[0]
    spec = query_params.get("spec", [None])[0]
    university = query_params.get("university", [None])[0]

    context = \
    f"course name : {course} \n" \
    f"dificult level : {level} \n" \
    f"rate : {rate} \n" \
    f"specilized : {spec} \n" \
    f"university : {university} \n" \
    f"description : {description[:100]} \n"
    return context

def question_answering(context, message):
    responses = answer_question(message, context)
    responses = t5_generate_answer(message, context)
    print(f"Answer: {responses}")
    return responses


def answer_question(question: str, context: str) -> str:
    # Tokenize the input question and context
    inputs = tokenizer.encode_plus(question, context, return_tensors="pt", truncation=True)

    # Get the input IDs and attention mask
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    # Run the model to get start and end logits
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        start_logits = outputs.start_logits
        end_logits = outputs.end_logits

    # Get the most likely start and end token positions
    start_idx = torch.argmax(start_logits)
    end_idx = torch.argmax(end_logits)

    # Convert token indices to answer text
    tokens = input_ids[0][start_idx:end_idx+1]
    answer = tokenizer.decode(tokens, skip_special_tokens=True)

    return answer

# Load the model and tokenizer
model_name = "t5-base"  # You can use "t5-small", "t5-large", or a fine-tuned version
t5_tokenizer = T5Tokenizer.from_pretrained(model_name)
t5_model = T5ForConditionalGeneration.from_pretrained(model_name)

def t5_generate_answer(question: str, context: str) -> str:
    # Prepare the input text in the format expected by T5
    input_text = f"question: {question} context: {context}"
    inputs = t5_tokenizer.encode(input_text, return_tensors="pt", truncation=True)

    # Generate the answer
    with torch.no_grad():
        outputs = t5_model.generate(inputs, max_length=150, num_beams=5, early_stopping=True)
    
    # Decode the generated answer
    answer = t5_tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer