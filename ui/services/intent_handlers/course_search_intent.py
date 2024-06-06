import streamlit as st
from services.skillner.skill_extract import extract_skills
from components.course_grid import QnA_SQL
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def course_search_pipeline(user_input):
    skills = extract_skills(user_input)
    st.write("Skills extracted:", skills)
    
    if len(skills) >= 3:
        df, responses = vectorsearch(user_input)
        responses = format_course_response(responses[:5])
    else:
        df, responses = QnA_SQL(user_input)

    return df, responses

def vectorsearch(skills):
    # Load the course data
    df = pd.read_csv("assistant/data/coursera_main_data.csv")

    # Concatenate all the skills into a single sentence
    skills_sentence = ' '.join(skills)

    # Embed the concatenated skills sentence
    skills_embedding = embedding_model.encode([skills_sentence])

    # Calculate cosine similarity with the vector db
    course_vectors = np.stack(df['SkillVectors'].apply(eval).values)  # Assuming 'SkillVectors' column contains string representations of lists
    similarities = cosine_similarity(skills_embedding, course_vectors)

    # Find the top courses based on similarity
    top_indices = np.argsort(similarities[0])[::-1][:20]  # Get top 5 courses
    top_courses = df.iloc[top_indices]
    responses = top_courses['CourseName'].tolist()

    return top_courses, responses


def format_course_response(courses):
    formatted_response = "I found some courses matching your requirements:\n"
    for i, course in enumerate(courses, start=1):
        formatted_response += f"{i}. {course}\n"
    return formatted_response