import streamlit as st
import openai
import os
from dotenv import load_dotenv
import PyPDF2
import io

# Tải biến môi trường
load_dotenv()

# Thiết lập cấu hình trang
st.set_page_config(page_title="Simple ChatGPT Chatbot", page_icon="🤖", layout="wide")


def extract_text_from_pdf(pdf_file):
    """Hàm trích xuất văn bản từ file PDF hoặc TXT đã tải lên.
    Đầu vào là file đã tải lên, đầu ra là chuỗi văn bản"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Không thể trích xuất văn bản từ file PDF: {e}")
        return ""




def create_context_message(context_text, role=""):
    """Tạo thông điệp hệ thống với context.
    Đầu vào là văn bản context và vai trò, đầu ra là chuỗi thông điệp hệ thống"""
    return


def initialize_openai():
    """Khởi tạo client OpenAI với khóa API.
    Đầu ra là client OpenAI đã khởi tạo"""
    return


def get_chatgpt_response(messages, client=None):
    """Lấy phản hồi từ API ChatGPT.
    Đầu vào là danh sách tin nhắn, đầu ra là phản hồi từ ChatGPT"""
    return


def main():
    # Khởi tạo client OpenAI
    openai_client = initialize_openai()

    # Tiêu đề và mô tả với st.title và st.markdown
    st.title("🤖 Simple ChatGPT Chatbot")
    st.markdown(
        "Chào mừng bạn đến với trợ lý AI cá nhân của mình! Hãy hỏi tôi bất cứ điều gì."
    )

    # Tạo box hướng dẫn với st.expander và st.markdown
    ##### CODE SNIPPET START #####
    with st.expander("📖 Hướng dẫn sử dụng"):\
        st.markdown("""
            **Cách thêm context vào chatbot:**
            1. **Chọn tone giọng**: Chọn tone giọng cho AI trong sidebar (bình thường, hài hước, nghiêm túc...)
            2. **Nhập text**: Viết thông tin tham khảo vào ô "Nhập context"
            3. **Upload file**: Tải lên file .txt hoặc .pdf chứa thông tin
            4. **Bắt đầu chat**: AI sẽ trả lời dựa trên context bạn cung cấp
            
            **Ví dụ context:**
            - Thông tin về công ty, sản phẩm
            - Tài liệu hướng dẫn, quy trình
            - Kiến thức chuyên môn cụ thể
            - Dữ liệu để phân tích
        """)

    # Khởi tạo trạng thái phiên cho lịch sử cuộc trò chuyện
    # Dùng st.session_state để lưu trữ trạng thái cuộc trò chuyện
    ##### CODE SNIPPET START #####

    # Khởi tạo sidebar với st.sidebar
    ##### CODE SNIPPET START #####
    with st.sidebar:
        st.header("⚙️ Cài đặt")

        # Mục Context
        st.subheader("📚 Thêm Context")

        # Chọn tone giọng AI
        # Tạo dropdown menu với st.selectbox
        tone_options = ["Trung tính", "Thân thiện", "Chuyên nghiệp", "Hài hước"]
        select_tone = st.selectbox(
            "Chọn tone giọng AI",
            options=tone_options,
            key="tone_select",
            index=0
        )

        # Nhập context thù công bằng text area
        context_text= st.text_area(
            "Nhập context cho AI (nếu có)",
            height=150,
            placeholder="Nhập thông tin hoặc hướng dẫn cho AI tại đây ...",
            value=(st.session_state.get("context_text", "")),
            key="context_input"
        )

        # Lưu context vào session state
        st.session_state.context_text = context_text

        # Hiển thị độ dài context và nút xóa context
        if context_text:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**Độ dài context:** {len(context_text)} ký tự")
            with col2:
                if  st.button("🗑️", key="clear_context"):
                    st.session_state.context_text = ""

        # Tải lên file context nếu không muốn nhập tay
        # Hỗ trợ file .txt và .pdf
        uploaded_file = st.file_uploader(
            "Tải lên file context (txt hoặc pdf)",
            type=["txt", "pdf"],
            key="file_uploader"
        )

        # Xử lý file đã tải lên và thêm vào file_context
        file_context = ""
        if uploaded_file is not None:
            if uploaded_file.type == "text/plain":
                # Nếu là file txt, đọc nội dung
                file_context = uploaded_file.read().decode("utf-8")
            elif uploaded_file.type == "application/pdf":
                # Nếu là file pdf, trích xuất văn bản
                file_context = extract_text_from_pdf(uploaded_file)
                if file_context:
                    st.success("Đã trích xuất văn bản từ file PDF!")
                else:
                    st.error("Không thể trích xuất văn bản từ file PDF. Vui lòng kiểm tra định dạng file.")

        # Kết hợp context từ text area và file
        full_context = ""
        if context_text:
            full_context += context_text + "\n"
        if file_context:
            full_context += file_context + "\n"


        # Cập nhật thông điệp cho hệ thống nếu context thay đổi
        
        

        # Tạo nút xóa cuộc trò chuyện và giữ nguyên thông điệp hệ thống
        st.button("🗑️ Xóa cuộc trò chuyện", key="clear_chat")

        # Hiển thị context hiện tại nếu có
        if full_context:
            with st.expander("📖 Hiện thị context hiện tại", expanded=True):
                st.text_area(
                    "Context hiện tại",
                    value=full_context,
                    height=200,
                    disabled=True
                )
        
        # Hiện thị tone giọng hiện tại nếu có
        if select_tone:
            st.info(f"Tone giọng hiện tại: {select_tone}")

        st.markdown("---")
        st.markdown("🎭 Made by [KhanhLe](https://kelvin-lee098.github.io)")

    # Hiển thị lịch sử trò chuyện trong st.session_state.chat_history với st.markdown

    # Đầu vào câu hỏi từ người dùng với st.chat_input


if __name__ == "__main__":
    main()
