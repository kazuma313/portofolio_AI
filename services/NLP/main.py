from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import tiktoken

load_dotenv()

model = "gpt-3.5-turbo"
model_embedding = "text-embedding-3-small"
token_limit = 20

embedding = OpenAIEmbeddings(model=model_embedding)
new_vectorstore = FAISS.load_local(
    "services/NLP/tentang_zulda",
    embeddings=embedding,
    allow_dangerous_deserialization=True,
)


def get_token_count(input_text: str):
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(input_text)
    # print("token:", tokens)
    # print("panjang token:", len(tokens) + 5)
    return tokens


def stream_response(input_text: str):
    prompt = PromptTemplate.from_template(
        """
        Nama kamu adalah Kurnia Zulda Matondang. Kamu merupakan Artificial Intelligent Developer yang juga memiliki beberapa skill tambahan\
        Kamu merupakan seorang yang ingin melamar pekerjaan pada suatu perushaan. \
        berikan branding yang baik agar dapat meyakinkan Human Resource Development.\
        kamu tidak berkenan untuk menanyakan seseuatu, lakukan pelayanan agar mereka bertanya, tugas anda hanya menjawab.\
        Berikan informasi yang hanya terkait dengan kamu beserta bidang kamu.\
        
        Jika pertanyaan yang diajukan menggunakan bahasa inggris maka jawab lah dengan bahasa inggris.\
        Jika pertanyaan yang diajukan menggunakan bahasa Indonesia maka jawab lah dengan bahasa Indonesia.\
        pastikan bahasa yang digunakan sama dengan bahasa dari pertanyaan.

    <context>
        {context}
    </context>

    {input}
    """
    )
    combine_doc_chain = create_stuff_documents_chain(ChatOpenAI(model=model), prompt)
    retrival_chain = create_retrieval_chain(
        new_vectorstore.as_retriever(), combine_doc_chain
    )
    text = ""
    # real_token = 0
    for chunk in retrival_chain.stream({"input": input_text}):

        if "answer" in chunk:
            text += chunk["answer"]
            # real_token += 1
            # print(chunk)
            yield chunk["answer"]
        pass
