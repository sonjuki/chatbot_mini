import streamlit as st
import google.generativeai as genai

# Cấu hình trang
st.set_page_config(
    page_title="Chat với Gemini",
    page_icon="💬",
    layout="wide"
)

# Hàm hiển thị tin nhắn
def display_message(role, content):
    with st.chat_message(role):
        st.markdown(content)

# Tiêu đề
st.title("💬 Gemini Chat Demo của Sơn")
st.markdown("Ứng dụng demo tương tác với API Gemini (Google)")

# Sidebar
with st.sidebar:
    st.header("Cấu hình")
    api_key = st.text_input("Google Gemini API Key", type="password")
    
    st.markdown("---")
    st.markdown("### Thông tin")
    st.markdown("""
    - Miễn phí với Google Gemini API
    - Dùng mô hình Gemini 1.5 hoặc 1.0
    """)
    if st.button("Xóa lịch sử chat"):
        st.session_state.messages = []

# Khởi tạo lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử
for message in st.session_state.messages:
    display_message(message["role"], message["content"])

# Nhập prompt
if prompt := st.chat_input("Nhập tin nhắn..."):
    if not api_key:
        st.error("Vui lòng nhập Google API Key!")
        st.stop()

    # Thêm tin nhắn người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    display_message("user", prompt)

    # Cấu hình Gemini API
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    with st.spinner("Đang suy nghĩ..."):
        try:
            # Gửi prompt trực tiếp đến model (không dùng chat history)
            response = model.generate_content(prompt)
            reply = response.text

            # Lưu lại câu trả lời
            st.session_state.messages.append({"role": "assistant", "content": reply})
            display_message("assistant", reply)

        except Exception as e:
            st.error(f"Lỗi khi gọi Gemini API: {e}")
