import streamlit as st
import google.generativeai as genai

# 1. Cấu hình trang (Phải để đầu tiên)
st.set_page_config(
    page_title="AI Translator Chuyên Ngành",
    page_icon="medical_symbol",
    layout="wide" # Dùng chế độ màn hình rộng cho dễ nhìn 2 cột
)

st.title("🌐 Gemini Translator: IT & Y Khoa")
st.caption("Sử dụng model Gemini 1.5 Flash - Tối ưu cho thuật ngữ chuyên sâu")

# 2. Sidebar: Nhập Key & Cấu hình
with st.sidebar:
    st.header("⚙️ Cấu hình")
    api_key = st.text_input("Dán Gemini API Key vào đây:", type="password")
    st.info("Lấy Key tại: https://aistudio.google.com/app/apikey")
    
    st.divider()
    
    # Chọn chuyên ngành để AI đổi vai ("Role-playing")
    domain = st.selectbox(
        "Chọn chuyên ngành dịch:",
        ["Công nghệ thông tin (IT)", "Y khoa / Dược phẩm", "Kinh tế / Tài chính", "Đời sống (General)"]
    )
    
    target_lang = st.radio(
        "Dịch sang ngôn ngữ:",
        ["Tiếng Việt", "Tiếng Anh", "Tiếng Nhật", "Tiếng Trung"]
    )

# 3. Giao diện chính (2 cột)
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📥 Văn bản gốc")
    source_text = st.text_area("Nhập nội dung vào đây:", height=300, placeholder="Paste text here...")

with col2:
    st.markdown("### 📤 Bản dịch")
    
    # Logic xử lý
    if st.button("Dịch Ngay ✨", use_container_width=True):
        if not api_key:
            st.warning("⚠️ Vui lòng nhập API Key ở cột bên trái trước!")
        elif not source_text:
            st.warning("⚠️ Chưa có văn bản để dịch.")
        else:
            try:
                # Cấu hình Gemini
                genai.configure(api_key=api_key)
                
                # Chọn model nhẹ và nhanh nhất
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Kỹ thuật Prompt Engineering: Gán vai trò chuyên gia
                prompt = f"""
                Bạn là một chuyên gia biên phiên dịch thâm niên trong lĩnh vực {domain}.
                Nhiệm vụ: Dịch văn bản sau sang {target_lang}.
                
                Yêu cầu quan trọng:
                1. Giữ nguyên các thuật ngữ chuyên ngành (nếu trong ngành đó thường dùng tiếng Anh) hoặc dịch sát nghĩa chuyên môn nhất.
                2. Văn phong chuyên nghiệp, chính xác.
                3. Chỉ trả về kết quả dịch, không giải thích thêm.
                
                Văn bản cần dịch:
                {source_text}
                """
                
                # Gọi API (Hiển thị loading quay quay)
                with st.spinner(f"Đang phân tích thuật ngữ {domain}..."):
                    response = model.generate_content(prompt)
                    translated_text = response.text
                
                # Hiển thị kết quả
                st.success("Hoàn tất!")
                st.text_area("Kết quả:", value=translated_text, height=300)
                
            except Exception as e:
                st.error(f"Lỗi kết nối: {str(e)}")

# Footer
st.markdown("---")
st.markdown("*Dự án Demo bởi Kỹ sư AI tương lai.*")
