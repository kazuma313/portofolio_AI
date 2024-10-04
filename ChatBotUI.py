from services.NLP.main import stream_response, get_token_count
from streamlit_pdf_viewer import pdf_viewer
from settings import Settings
import streamlit as st

project = Settings().project_option
st.error("Still on progress development")
st.title("Kurnia Zulda Matondang")

st.sidebar.header("#__My Project__")

select_project = st.sidebar.selectbox("Project name", project)

if "token_limitation" not in st.session_state:
    st.session_state.token_limitation = 200


if select_project == project[0]:
    st.header("Chat bot about me")
    with st.form("my_form"):
        text = st.text_area(
            "Enter text:",
            placeholder="Tanya-tanya tentang saya",
        )
        st.text(f"Token: {st.session_state.token_limitation} (just scenario if i limit the token)")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write_stream(stream_response(text))
            token_used = get_token_count(text + "".join(list(stream_response(text))))
            st.session_state.token_limitation -= len(token_used)
            st.text(f"token used {len(token_used)}")
            st.text(f"Remaining token limit: {st.session_state.token_limitation}")


elif select_project == project[1]:
    st.header("My last computer vision project")
    col1, col2 = st.columns((1, 1))
    with col1:
        st.info('OCR', icon="ℹ️")
        st.video("assets/videos/container_id_1.mp4")
    with col2:
        st.info('Face Mask Detection', icon="ℹ️")
        st.video("assets/videos/face_mask_detection.mp4")

    st.info('Age detection', icon="ℹ️")
    st.image("assets/images/age_detection.jpg")


if select_project == project[2]:
    pass


if select_project == project[3]:
    st.success("This is just a small part of what I've learned, but It's show that I'm serious about this field and continue to build my skills.", icon="✅")
    st.title("##AI Bootcamp certification")
    col1, col2 = st.columns(2)
    with col1:
        st.info("Got Excellent result", icon="ℹ️")
        pdf_viewer(
            "assets/documents/Certificate of Excellence Mastering AI Bootcamp - Kurnia Zulda Matondang.pdf"
        )

    with col2:
        st.info("Complete AI Bootcamp successfully", icon="ℹ️")
        pdf_viewer(
            "assets/documents/Certificate of Completion Mastering AI Bootcamp - Kurnia Zulda Matondang.pdf"
        )

    st.info('Udemy certification', icon="ℹ️")
    st.text("Learning Computer Vision")
    pdf_viewer("assets/documents/Udemy_COMVIS_KurniaZuldaMatondang.pdf")


if select_project == project[4]:
    pdf_viewer("assets/documents/CV_Kurnia_Zulda_Matondang.pdf")


##########################################
##########################################
