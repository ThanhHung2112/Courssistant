import torch

from transformers import BertTokenizer, BertModel
from transformers import T5ForConditionalGeneration, T5Tokenizer

from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity

import re
import numpy as np
import pandas as pd

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

import en_core_web_sm
spc_en = en_core_web_sm.load()

bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertModel.from_pretrained('bert-base-uncased')


# Load the model and tokenizer
model_name = "t5-base"  # You can use "t5-small", "t5-large", or a fine-tuned version
t5_tokenizer = T5Tokenizer.from_pretrained(model_name)
t5_model = T5ForConditionalGeneration.from_pretrained(model_name)

def preprocess_text(text):
    stopwords_eng = stopwords.words("english")
    text = text.lower()
    text = text.replace(",", "").replace(".", "").replace("!", "").replace("?", "")
    text = re.sub(r"[\W\d_]+", " ", text)
    text = [pal for pal in text.split() if pal not in stopwords_eng]
    spc_text = spc_en(" ".join(text))
    tokens = [word.lemma_ if word.lemma_ != "-PRON-" else word.lower_ for word in spc_text]
    return " ".join(tokens)

def encode_sequence_with_bert(sequence):
    # Khởi tạo tokenizer và mô hình BERT
    bert_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    bert_model = BertModel.from_pretrained("bert-base-uncased")

    # Tiền xử lý và mã hoá câu
    input_ids = bert_tokenizer(preprocess_text(sequence), return_tensors="pt").input_ids
    with torch.no_grad():
        outputs = bert_model(input_ids)
        hidden_states = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

    return hidden_states

def nearest_course(df, course_name):
    # Tiền xử lý và mã hoá câu mới với BERT
    encoded_course_name = encode_sequence_with_bert(course_name)

    # Chuyển đổi chuỗi số thực từ cột BERT_Encoded thành ma trận 2D
    bert_encoded_matrix = df['Course_Name_Encoded'].apply(lambda x: np.fromstring(x[1:-1], sep=' '))
    bert_encoded_matrix = np.vstack(bert_encoded_matrix)

    # Tạo mô hình KNN với k=5 (tìm 5 câu giống nhất)
    knn_model = NearestNeighbors(n_neighbors=5, metric='cosine')
    knn_model.fit(bert_encoded_matrix)

    valid_indices = []
    similarities = []

    for i, encoded_vector in enumerate(bert_encoded_matrix):
        similarity_score = cosine_similarity([encoded_course_name], [encoded_vector])[0][0]
        similarities.append(similarity_score)
        if similarity_score > 0.8:
            valid_indices.append(i)

    nearest_neighbors = knn_model.kneighbors([encoded_course_name], n_neighbors=5, return_distance=False)

    nn = []
    for i, neighbor_index in enumerate(nearest_neighbors[0]):
        if neighbor_index in valid_indices:
            # neighbor_sequence = df.at[neighbor_index, "Course Name"]
            neighbor_data = df.iloc[neighbor_index].to_dict()
            similarity_score = cosine_similarity([encoded_course_name], [bert_encoded_matrix[neighbor_index]])[0][0]
            nn.append((neighbor_data, similarity_score))
            print(f"Course {i + 1}: {neighbor_data['Course Name']} - Similarity: {similarity_score}")

    max_similarity_index = np.argmax(similarities)
    max_similarity_course = df.iloc[max_similarity_index].to_dict()
    max_similarity_score = similarities[max_similarity_index]    
    return nn, {'Course': max_similarity_course, "Score": max_similarity_score}


def course_name_from_input(user_input: str) -> str:
    # Prepare the input text in the format expected by T5
    promt = " Can you tell me the name of the course?"

    input_text = f"question: {promt} context: {user_input}"
    inputs = t5_tokenizer.encode(input_text, return_tensors="pt", truncation=True)

    # Generate the answer
    with torch.no_grad():
        outputs = t5_model.generate(inputs, max_length=150, num_beams=5, early_stopping=True)
    
    # Decode the generated answer
    answer = t5_tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer

