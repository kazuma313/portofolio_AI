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
        You are an assistant for question-answering tasks. \
        Use the following pieces of retrieved context to answer the question. \
        If you don't know the answer, just say that you don't know. \
        If the query not in Indonesia language, you should translate the answer as same as the query language.
        
        Question: {input} 
        Context: {context} 
        Answer:
    """
    )
    combine_doc_chain = create_stuff_documents_chain(ChatOpenAI(model=model), prompt)
    retrival_chain = create_retrieval_chain(
        new_vectorstore.as_retriever(), combine_doc_chain
    )
    text = ""
    # real_token = 0
    for chunk in retrival_chain.stream({"input": input_text}):
        print(chunk)

        if "answer" in chunk:
            text += chunk["answer"]
            # real_token += 1
            # print(chunk)
            yield chunk["answer"]
        pass

