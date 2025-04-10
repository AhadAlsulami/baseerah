import streamlit as st
import pandas as pd
from datetime import datetime
import os


st.set_page_config(page_title="التسجيل للمباراه", page_icon="🏆", layout="centered")
st.sidebar.empty()


st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@500;700&display=swap');

        .stApp {
            background: #f8fafc;
        }

        /* Hide default Streamlit elements */
        header { visibility: hidden; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        

        /* Title */
        .title {
            font-size: 60px;
            font-weight: 450;
            text-align: center;
            margin: 1rem 0 2rem 0;
            color: #ff7066;
            font-family: 'Tajawal', sans-serif;
            direction: rtl;
            line-height: 1.2;
        }

        /* Button styles */
        .stButton>button {
            height: 50px;
            border-radius: 12px;
            border: 1px solid #e2e8f0 !important;
            font-size: 16px;
            font-weight: 500;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin: 0.5rem 0;
        }

        /* Input fields */
        .stTextInput input, .stSelectbox select, .stFileUploader input {
            font-size: 16px;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            margin: 0.5rem 0;
        }

        .stTextInput input:focus, .stSelectbox select:focus, .stFileUploader input:focus {
            border-color: #1e40af;
        }
        
        /* Success/Error Message */
        .stSuccess, .stError {
            text-align: center;
            font-size: 18px;
            font-weight: 500;
            margin-top: 1rem;
            color: #1e40af;
        }

        .stError {
            color: #ef4444;
        }
    </style>
""", unsafe_allow_html=True)


st.markdown('<div class="title">التسجيل للمبارايات</div>', unsafe_allow_html=True)


os.makedirs("data/pictures", exist_ok=True)


with st.form("form"):
    col1, col2 = st.columns(2)
    
    with col1:
        email = st.text_input("البريد الإلكتروني")
        phone = st.text_input("رقم الهاتف")
    
    with col2:
        name = st.text_input("الاسم الكامل")
        sport = st.selectbox("الرياضة", ["كرة القدم","فورمولا 1" ,"كرة السلة", "التنس", "الكرة الطائرة", "تنس الريشة", "أخرى"])
    
    picture = st.file_uploader("تحميل صورة شخصية", type=["jpg", "jpeg", "png"])
    submit = st.form_submit_button("تسجيل")


if submit:
    if not all([name, email, phone, sport, picture]):
        st.error("يرجى تعبئة جميع الحقول")
    else:
        pic_name = f"{name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{picture.name.split('.')[-1]}"
        pic_path = os.path.join("data/pictures", pic_name)
        with open(pic_path, "wb") as f:
            f.write(picture.getbuffer())

        data = {
            "name": name,
            "email": email,
            "phone number": phone,
            "sport": sport,
            "pic path": pic_path,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Save data to CSV
        file_path = "data/registrations.csv"
        df = pd.read_csv(file_path) if os.path.exists(file_path) else pd.DataFrame()
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_csv(file_path, index=False)

        st.success("تم التسجيل بنجاح!")

# Show registered users
if os.path.exists("data/registrations.csv"):
    st.subheader("المسجلين")
    st.dataframe(pd.read_csv("data/registrations.csv"))