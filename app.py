import streamlit as st

st.set_page_config(page_title="Sale support agent", layout="wide")
st.title("Sale support agent")
st.write("Ứng dụng được tạo ra để hỗ trợ các nghiệp vụ của sale nhằm tăng hiệu quả công việc. Giảm thời gian và tăng chất lượng của các nghiệp vụ hiện tại mà sale đang làm thường ngày.")

st.subheader("Danh sách công cụ")
st.page_link("pages/qa.py", label="Hỏi đáp các skills, casestudy... đang có của Rikkeisoft", icon="💬")
st.page_link("pages/matching.py", label="Matching thông tin của một công ty khách với các casestudy của rikkesoft", icon="🔀")