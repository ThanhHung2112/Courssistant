# Courssistant
Courssistant (Course - Asssistant) is a chatbot support user in course selection

# System Requirements:

python: 3.9.19

## Installation
```bash
pip install -r requirements.txt
```

<<<<<<< HEAD
=======
## Features


## User Interface

> Homepage

<p align="center">
  <img src="https://github.com/ThanhHung2112/Courssistant/blob/main/assests/homepage1.png" alt="Home Page 1">
</p>



>>>>>>> e14947974958d715e5f018393eacc28abbe98ac1
## Run
Old method 

```bash
rasa run --enable-api --cors "*" --debug
```
<<<<<<< HEAD
=======

>>>>>>> e14947974958d715e5f018393eacc28abbe98ac1
On another termial, execute this 
```bash
streamlit run ui/app.py --server.runOnSave true
```

New 🎉 supper easy :>

```bash
python main.py
```

<<<<<<< HEAD
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

import db_test.sql vào mysql để test, connection config trong hàm get_connection(), text2sql.py
=======
## Flow

<p align="center">
  <img src="https://github.com/ThanhHung2112/Courssistant/blob/main/assests/flows.png" alt="Home Page 1">
</p>


>>>>>>> e14947974958d715e5f018393eacc28abbe98ac1
