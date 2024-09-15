import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain import hub
from numpy.f2py.symbolic import Op

load_dotenv()


class PDFload:
    def __init__(self, vector_save_path: str = "faiss_index_react"):
        self.embedding = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vector_save_path: str = vector_save_path

    def pdf_embedding(self, pdf_path: str):
        loader = PyPDFLoader(
            pdf_path,
        )
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        docs = text_splitter.split_documents(docs)

        vector_store = FAISS.from_documents(docs, self.embedding)
        vector_store.save_local(self.vector_save_path)

    def pdf_load_embedding(self):
        new_vectorstore = FAISS.load_local(
            self.vector_save_path,
            embeddings=self.embedding,
            allow_dangerous_deserialization=True,
        )

        retrival_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
        combine_doc_chain = create_stuff_documents_chain(
            OpenAI(), retrival_qa_chat_prompt
        )
        retrival_chain = create_retrieval_chain(
            new_vectorstore.as_retriever(), combine_doc_chain
        )

        for chunk in retrival_chain.stream({"input": "Ceritakan saya tentang zulda"}):
            if "answer" in chunk:
                print(chunk["answer"], end="", flush=True)
            pass


if __name__ == "__main__":
    embed_pdf = PDFload()
    # embed_pdf.pdf_embedding("CV_Kurnia_Zulda_Matondang.pdf")
    embed_pdf.pdf_load_embedding()
