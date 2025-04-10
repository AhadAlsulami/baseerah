import streamlit as st
import cv2
import face_recognition
import numpy as np
import pandas as pd
import os


st.set_page_config(
    page_title="نظام المراقبة", 
    page_icon="🏅", 
    layout="centered"
)


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
            color: #9977FF;
            font-family: 'Tajawal', sans-serif;
            direction: rtl;
            line-height: 1.2;
        }

        /* Container styles */
        .main-container {
            background: white;
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        
        /* User info card */
        .user-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 1.5rem;
            border: 1px solid #e2e8f0;
        }
        
        .user-field {
            font-size: 18px;
            margin-bottom: 0.8rem;
            font-family: 'Tajawal', sans-serif;
            direction: rtl;
        }
        
        .user-label {
            font-weight: 700;
            color: #4b5563;
        }
        
        .user-value {
            font-weight: 500;
            color: #1f2937;
        }
        
        /* Camera feed */
        .camera-feed {
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
        }
        
        /* Sidebar styles */
        .sidebar .sidebar-content {
            background-color: #f8fafc;
            padding: 1rem;
        }
        
        .sidebar-option {
            font-family: 'Tajawal', sans-serif;
            font-size: 18px;
            padding: 0.5rem 1rem;
            margin: 0.5rem 0;
            border-radius: 8px;
            transition: all 0.2s;
            cursor: pointer;
        }
        
        .sidebar-option:hover {
            background-color: #e2e8f0;
        }
        
        .sidebar-option.active {
            background-color: #9977FF;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h2 style='font-family: Tajawal; color: #9977FF;'>خيارات النظام</h2>
        </div>
    """, unsafe_allow_html=True)
    
    
    option = st.radio(
        "",
        ["مراقبة الدخول", "متابعة الازدحام", "رصد النفايات"],
        index=0,
        label_visibility="collapsed"
    )



DATA_PATH = r"C:\Users\lenovo\Desktop\AI League\data\registrations.csv"


if option == "مراقبة الدخول":
    st.markdown('<div class="title">نظام مراقبة الدخول</div>', unsafe_allow_html=True)
    st.empty()
    with st.container():
        #st.markdown('<div class="main-container">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        # Initialize session state
        if 'current_user' not in st.session_state:
            st.session_state.current_user = None
        
        
        with col2:
            #st.markdown('<div class="user-card">', unsafe_allow_html=True)
            st.markdown("**<div style='text-align: center; font-size: 24px; font-family: Tajawal, sans-serif; margin-bottom: 1.5rem;'>بيانات المستخدم</div>**", unsafe_allow_html=True)
            
            user_display = st.empty()
            
            
            if st.session_state.current_user is None:
                user_display.markdown("""
                    <div style='text-align: center; color: #6b7280; font-family: Tajawal, sans-serif; font-size: 18px;'>
                        ...جاري التعرف على الوجه
                    </div>
                """, unsafe_allow_html=True)
            else:
                user = st.session_state.current_user
                user_display.markdown(f"""
                    <div class="user-field">
                        <span class="user-label">الاسم: </span>
                        <span class="user-value">{user['name']}</span>
                    </div>
                    <div class="user-field">
                        <span class="user-label">البريد الإلكتروني: </span>
                        <span class="user-value">{user['email']}</span>
                    </div>
                    <div class="user-field">
                        <span class="user-label">رقم الهاتف: </span>
                        <span class="user-value">{user['phone']}</span>
                    </div>
                    <div class="user-field">
                        <span class="user-label">النشاط الرياضي: </span>
                        <span class="user-value">{user['sport']}</span>
                    </div>
                    <div class="user-field">
                        <span class="user-label">تاريخ التسجيل: </span>
                        <span class="user-value">{user['date']}</span>
                    </div>
                    <div class="user-field">
                        <span class="user-label" style="color: lightgreen;">تم تأكيد الحضور </span>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)  # Close user-card

        # Left column - Continuous camera feed
        with col1:
            st.markdown('<div class="camera-feed">', unsafe_allow_html=True)
            video_placeholder = st.empty()
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Load known faces
            @st.cache_data
            def load_known_faces():
                try:
                    df = pd.read_csv(DATA_PATH, encoding='utf-8')
                    required_columns = ["name", "email", "phone number", "sport", "pic path", "date"]
                    if not all(col in df.columns for col in required_columns):
                        st.error("ملف البيانات لا يحتوي على جميع الأعمدة المطلوبة")
                        return [], []
                    
                    known_face_encodings = []
                    known_face_data = []
                    
                    for _, row in df.iterrows():
                        img_path = row["pic path"]
                        if not os.path.exists(img_path):
                            continue
                            
                        try:
                            image = face_recognition.load_image_file(img_path)
                            encodings = face_recognition.face_encodings(image)
                            if encodings:
                                known_face_encodings.append(encodings[0])
                                known_face_data.append({
                                    "name": row["name"],
                                    "email": row["email"],
                                    "phone": row["phone number"],
                                    "sport": row["sport"],
                                    "date": row["date"]
                                })
                        except Exception as e:
                            st.warning(f"خطأ في معالجة صورة {row['name']}: {e}")
                    
                    return known_face_encodings, known_face_data
                except Exception as e:
                    st.error(f"خطأ في قراءة ملف البيانات: {e}")
                    return [], []
            
            known_encodings, known_data = load_known_faces()
            
            # Start camera
            video_capture = cv2.VideoCapture(0)
            
            try:
                while True:
                    ret, frame = video_capture.read()
                    if not ret:
                        st.error("فشل في قراءة الكاميرا")
                        break
                    
                    # Process frame
                    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                    rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                    
                    # Detect faces
                    face_locations = face_recognition.face_locations(rgb_frame)
                    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                    
                    # Update display for each face found
                    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                        # Scale up face locations
                        top *= 4; right *= 4; bottom *= 4; left *= 4
                        
                        # Compare with known faces
                        matches = face_recognition.compare_faces(known_encodings, face_encoding)
                        name = "غير معروف"
                        
                        if True in matches:
                            best_match_index = np.argmin(face_recognition.face_distance(known_encodings, face_encoding))
                            name = known_data[best_match_index]["name"]
                            
                            st.session_state.current_user = known_data[best_match_index]
                            user = st.session_state.current_user
                            user_display.markdown(f"""
                                <div class="user-field">
                                    <span class="user-label">الاسم: </span>
                                    <span class="user-value">{user['name']}</span>
                                </div>
                                <div class="user-field">
                                    <span class="user-label">البريد الإلكتروني: </span>
                                    <span class="user-value">{user['email']}</span>
                                </div>
                                <div class="user-field">
                                    <span class="user-label">رقم الهاتف: </span>
                                    <span class="user-value">{user['phone']}</span>
                                </div>
                                <div class="user-field">
                                    <span class="user-label">النشاط الرياضي: </span>
                                    <span class="user-value">{user['sport']}</span>
                                </div>
                                <div class="user-field">
                                    <span class="user-label">تاريخ التسجيل: </span>
                                    <span class="user-value">{user['date']}</span>
                                </div>
                                <div class="user-field">
                                    <span class="user-label" style="color: lightgreen;">تم تأكيد الحضور </span>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        # Draw bounding box
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                        cv2.putText(frame, name, (left + 6, bottom - 6), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)
                    
                    # Display the resulting image
                    video_placeholder.image(frame, channels="BGR")
                    
            finally:
                video_capture.release()
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close main-container


elif option == "متابعة الازدحام":
    st.markdown('<div class="title">نظام متابعة الازدحام</div>', unsafe_allow_html=True)
    st.empty()
    from ultralytics import YOLO

    
    @st.cache_resource
    def load_model():
        return YOLO("yolov8n.pt")  # Use larger model if needed (e.g., yolov8s.pt)

    model = load_model()

    
    def process_video(video_path, crowd_threshold=5):
        cap = cv2.VideoCapture(video_path)
        frame_placeholder = st.empty()
        message_placeholder = st.empty()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            
            results = model(frame)
            people_count = sum(1 for box in results[0].boxes if int(box.cls) == 0)

            
            annotated_frame = results[0].plot()
            cv2.putText(annotated_frame, f"People: {people_count}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            frame_placeholder.image(annotated_frame, channels="BGR", use_container_width=True)

            # Crowd status
            if people_count > crowd_threshold:
                message_placeholder.error(f"تم رصد ازدحام! عدد الأشخاص: {people_count}")
            else:
                message_placeholder.success(f"لا يوجد ازدحام. عدد الأشخاص: {people_count}")

        cap.release()

    col1, col2 = st.columns(2)

    # Paths to live videos
    VIDEO_1_PATH = "videos/camera1.mp4"
    VIDEO_2_PATH = "videos/camera2.mp4"

    with col1:
        if st.button("📷 كاميرا 1 - منطقة أ"):
            st.video(VIDEO_1_PATH)
            process_video(VIDEO_1_PATH)

    with col2:
        if st.button("📷 كاميرا 2 - منطقة ج"):
            st.video(VIDEO_2_PATH)
            process_video(VIDEO_2_PATH)

    st.markdown('</div>', unsafe_allow_html=True)




elif option == "رصد النفايات":
    st.empty()
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; font-size: 24px; margin-bottom: 1.5rem;'>
            نظام رصد النفايات
        </div>
        <div style='text-align: center; color: #6b7280; font-size: 18px;'>
            هذه الصفحة تحت التطوير
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)