from services.NLP.main import stream_response
from streamlit_pdf_viewer import pdf_viewer
from settings import Settings
import streamlit as st

project = Settings().project_option

st.title("Kurnia Zulda Matondang")

st.sidebar.header("#__My Project__")
select_project = st.sidebar.selectbox("Project name", project)


if select_project == project[0]:
    st.header("Chat bot about me")
    with st.form("my_form"):
        text = st.text_area(
            "Enter text:",
            placeholder="Tanya-tanya tentang saya",
        )
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write_stream(stream_response(text))


elif select_project == project[1]:
    st.header("My last computer vision project")
    col1, col2 = st.columns((1, 1))
    with col1:
        st.video("assets/videos/container_id_1.mp4")
    with col2:
        st.video("assets/videos/face_mask_detection.mp4")

    st.header("Age detection")
    st.image("assets/images/age_detection.jpg")


if select_project == project[2]:
    pass


if select_project == project[3]:
    st.header("this is just a small part of what i learned which i show")
    st.title("##AI Bootcamp certification")
    col1, col2 = st.columns(2)
    with col1:
        st.text("Got Excellent result")
        pdf_viewer(
            "assets/documents/Certificate of Excellence Mastering AI Bootcamp - Kurnia Zulda Matondang.pdf"
        )

    with col2:
        st.text("Complete Bootcamp successfully")
        pdf_viewer(
            "assets/documents/Certificate of Completion Mastering AI Bootcamp - Kurnia Zulda Matondang.pdf"
        )

    st.title("## Udemy certification")
    st.text("Learning Computer Vision")
    pdf_viewer("assets/documents/Udemy_COMVIS_KurniaZuldaMatondang.pdf")


if select_project == project[4]:
    st.text("My Curriculum Vitae")
    pdf_viewer("assets/documents/CV_Kurnia_Zulda_Matondang.pdf")
