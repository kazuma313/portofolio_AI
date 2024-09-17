import streamlit as st
# from langchain_openai.chat_models import ChatOpenAI

from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain import hub
from langchain_core.prompts import PromptTemplate

from dotenv import load_dotenv

project = ["Computer Vision", "Natural Language Processing", "Data Science"]
load_dotenv()

st.title("Kurnia Zulda Matondang")

st.sidebar.header("#__My Project__")
select_project = st.sidebar.selectbox('Project name', project)

# openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
embedding = OpenAIEmbeddings(model="text-embedding-3-small")
new_vectorstore = FAISS.load_local(
    "faiss_index_react",
    embeddings=embedding,
    allow_dangerous_deserialization=True,
)


def stream_response(input_text):
    retrival_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    prompt = PromptTemplate.from_template("""
    Kamu merupakan seorang yang ingin melamar pekerjaan pada suatu perushaan. \
    berikan branding yang baik agar dapat meyakinkan Human Resource Development.\
    jika terdapat pertanyaan yang tidak sesuai dengan kompetensi atau bukan mengenai suatu perkerjaan,\
    berikan penolakan jawaban yang sopan dan elegan.

    <context>
        {context}
    </context>

    {input}
    """)
    combine_doc_chain = create_stuff_documents_chain(
        OpenAI(), prompt
    )
    retrival_chain = create_retrieval_chain(
        new_vectorstore.as_retriever(), combine_doc_chain
    )
    for chunk in retrival_chain.stream({"input": input_text}):
        if "answer" in chunk:
            yield chunk["answer"]
        pass

if select_project == project[1]:
    st.header("Chat bot about me")
    with st.form("my_form"):
        text = st.text_area(
            "Enter text:",
            "Tanya-tanya tentang saya",
        )
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write_stream(stream_response(text))
        # if not openai_api_key.startswith("sk-"):
        #     st.warning("Please enter your OpenAI API key!", icon="⚠")
        # if submitted and openai_api_key.startswith("sk-"):
        #     st.write_stream(stream_response(text))
