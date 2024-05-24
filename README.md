# Courssistant
Courssistant (Course - Asssistant) is a chatbot support user in course selection

# System Requirements:

python: 3.9.19

## Run

```bash
rasa run --enable-api --cors "*" --debug
```

```bash
streamlit run ui/main.py --server.runOnSave true
```

```
zone = st.empty()
for userInput in userInputs:
    df, response = QnA_SQL(userInput)
    with zone.container():
        st.write(response)
        display_course_grid(df)        
```
zone = st.empty() {khai báo để gọi container cho 1 session hiển thị mới}

display_course_grid(df) {render html từ 1 dataframe}

hàm QnA_SQL() là hàm xử lý chính, input là câu hỏi, output là df để render và 1 câu trả lời