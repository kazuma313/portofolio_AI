from services.NLP.main import stream_response, get_token_count
from settings import Settings
import streamlit as st


st.error("Still on progress development")
st.title("Kurnia Zulda Matondang")
st.divider()


if "token_limitation" not in st.session_state:
    st.session_state.token_limitation = 200

def natural_language_processing():
    st.header("Chat bot about Kurnia Zulda Matondang")
    with st.form("my_form"):
        text = st.text_area(
            "Enter text:",
            placeholder="Ask anything about kurnia zulda matondang",
        )
        st.text(f"Token: {st.session_state.token_limitation} (just scenario if i limit the token)")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write_stream(stream_response(text))
            token_used = get_token_count(text + "".join(list(stream_response(text))))
            st.session_state.token_limitation -= len(token_used)
            st.text(f"token used {len(token_used)}")
            st.text(f"Remaining token limit: {st.session_state.token_limitation}")


def computer_vision():
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


pg = st.navigation([st.Page(natural_language_processing), st.Page(computer_vision)])
pg.run()


##########################################
##########################################
