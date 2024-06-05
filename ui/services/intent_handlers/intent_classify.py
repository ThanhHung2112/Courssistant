import numpy as np 
import torch
import torch.nn as nn
from transformers import AutoTokenizer, RobertaModel
from services.intent_handlers.architecture import IntentClassifier

def intent_classification(message):
    intents = {
        'description': 0,
        'course_search': 1,
        'open_landingpage': 2,
        'negative': 3,
        'bot_challenge': 4,
        'greet': 5,
        'ask_features': 6,
        'ask_name': 7
    }
    path = 'ui/services/intent_handlers/models'

    # Load tokenizer
    roberta_tokenizer = AutoTokenizer.from_pretrained(path + '/common_intents/intent_tokenizer')
    roberta_model = RobertaModel.from_pretrained("FacebookAI/roberta-base")
    # Initialize model
    intent_model = IntentClassifier(roberta_model, num_classes=8)
    # Load model state_dict
    intent_model.load_state_dict(torch.load(path + '/common_intents/intent_model.pt', map_location=torch.device('cpu')))
    # Specify the device (e.g., 'cuda', 'mps' for GPU or 'cpu' for CPU)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    # Predict intent
    predicted_intent = predict_intents(message, intent_model, roberta_tokenizer, intents, device)
    return predicted_intent
    

def whisper_intent_classification(message):
    path = 'ui/services/intent_handlers/models'
    intents = {
        'whisper_on': 0,
        'whisper_off': 1,
        'whisperon_n_intent': 2,
        'whisperoff_n_intent': 3,
        'common': 4,
    }
    # Load tokenizer
    roberta_tokenizer = AutoTokenizer.from_pretrained(path + '/whisper_intents/whisper_intent_tokenizer')
    roberta_model = RobertaModel.from_pretrained("FacebookAI/roberta-base")
    # Initialize model
    intent_model = IntentClassifier(roberta_model, num_classes=5)
    # Load model state_dict
    intent_model.load_state_dict(torch.load(path + '/whisper_intents/whisper_intent_model.pt', map_location=torch.device('cpu')))
    # Specify the device (e.g., 'cuda', 'mps' for GPU or 'cpu' for CPU)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    # Predict intent
    predicted_intent = predict_intents(message, intent_model, roberta_tokenizer, intents, device)
    return predicted_intent

def predict_intents(sentence, model, tokenizer, intent_map, device):
    # Move model and tokenizer to the specified device
    model = model.to(device)
    tokenizer = tokenizer
    # Tokenize the sentence
    encoded_sentence = tokenizer(sentence, padding=True, truncation=True, return_tensors="pt").to(device)
    with torch.no_grad():
        # Forward pass
        logits = model(encoded_sentence['input_ids'], encoded_sentence['attention_mask'])
        predicted_label = torch.argmax(logits, dim=1).item()
    # Get the predicted tense label
    predicted_intent = [k for k, v in intent_map.items() if v == predicted_label][0]
    
    return predicted_intent

