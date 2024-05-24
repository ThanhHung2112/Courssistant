# Courssistant
Courssistant (Course - Asssistant) is a chatbot support user in course selection

# System Requirements:

python: 3.9.19

# Huong dan su dung

zone = st.empty()
for userInput in userInputs:
    df, response = QnA_SQL(userInput)
    with zone.container():
        st.write(response)
        display_course_grid(df)

zone = st.empty {bắt buộc, để reset kết quả hiển thị trên component chính}

with zone.container() {để thực hiện 1 session xử lý hiển thị mới}

display_course_grid() dùng để render thẻ html từ 1 df

QnA_SQL() là hàm xử lý chính call ở main, return 1 df và 1 câu trả lời, input là câu hỏi về database