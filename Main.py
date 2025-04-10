import streamlit as st


st.set_page_config(
    page_title="نظام بصيرة",
    page_icon="👁️",
    layout="centered",
    initial_sidebar_state="collapsed"
)


st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@500;700&display=swap');
        
        .stApp {{
            background: #f8fafc;
        }}
        
        /* Hide default Streamlit elements */
        header {{ visibility: hidden; }}
        #MainMenu {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        
        .title {{
            font-size: 60px;
            font-weight: 750;
            text-align: center;
            margin: 1rem 0 2rem 0;
            color: #1e40af;
            font-family: 'Tajawal', sans-serif;
            direction: rtl;
            line-height: 1.2;
        }}
        
        .stButton>button {{
            height: 100px;
            border-radius: 12px;
            border: 1px solid #e2e8f0 !important;
            font-size: 1.3rem;
            font-weight: 500;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin: 0.5rem 0;
        }}
        
        #user {{
            background: white !important;
            color: #3b82f6 !important;
        }}
        
        #admin {{
            background: #1e40af !important;
            color: #f8fafc !important;
            border: 1px solid #1e40af !important;
        }}
        
        .metric-card {{
            text-align: center;
            padding: 1.5rem 1rem;
            direction: rtl;
        }}
        
        .metric-label {{
            font-family: 'Tajawal';
            font-size: 1rem;
            color: #64748b;
            margin-bottom: 0.5rem;
        }}
        
        .metric-value {{
            font-family: 'Tajawal';
            font-size: 1.8rem;
            font-weight: 700;
            color: #1e293b;
        }}
        
        .metric-delta {{
            font-family: 'Tajawal';
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }}
    </style>
""", unsafe_allow_html=True)


st.markdown('<div class="title">👁️<br>بصيرة</div>', unsafe_allow_html=True)


col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    b1, b2 = st.columns(2)
    
    with b1:
        if st.button("واجهة الزوار",
                   key="user",
                   use_container_width=True,
                   help="الدخول إلى واجهة التسجيل"):
            st.switch_page("pages/User.py")
    
    with b2:
        if st.button("لوحة التحكم",
                   key="admin",
                   use_container_width=True,
                   help="الدخول إلى نظام المراقبة"):
            st.switch_page("pages/Admin.py")


st.markdown("""
    <div style="text-align: center; font-family: 'Tajawal'; 
                font-size: 1.1rem; color: #475569; margin: 2rem 0 1rem 0;
                font-weight: 500;">
        مؤشرات الأداء الرئيسية
    </div>
""", unsafe_allow_html=True)


m1, m2, m3 = st.columns(3)

with m1:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-label">الأجهزة المتصلة</div>
            <div class="metric-value">24</div>
            <div class="metric-delta" style="color: #10b981;">3 جديد ▲</div>
            <div style="font-size:0.8rem; color:#64748b; margin-top:0.5rem;">
                (من أصل 25 جهازاً)
            </div>
        </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-label">الحالات الطارئة</div>
            <div class="metric-value">2</div>
            <div class="metric-delta" style="color: #ef4444;">1 حرج ▼</div>
            <div style="font-size:0.8rem; color:#64748b; margin-top:0.5rem;">
                (1 إنذار, 1 تحذير)
            </div>
        </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-label">استقرار النظام</div>
            <div class="metric-value">٩٩٫٨٪</div>
            <div class="metric-delta" style="color: #10b981;">٠٫١٪ ▲</div>
            <div style="font-size:0.8rem; color:#64748b; margin-top:0.5rem;">
                (7 أيام الأخيرة)
            </div>
        </div>
    """, unsafe_allow_html=True)