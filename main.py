from langchain_openai import OpenAI
from fastapi import FastAPI, Form, Request, WebSocket
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain import hub
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

chat_responses = []


@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse(
        "home.html", {"request": request, "chat_responses": chat_responses}
    )


chat_log = [{"role": "system", "content": "You tell jokes."}]


@app.websocket("/ws")
async def chat(websocket: WebSocket):

    await websocket.accept()

    while True:
        user_input = await websocket.receive_text()
        # chat_log.append({"role": "user", "content": user_input})
        # chat_responses.append(user_input)

        try:
            ai_response = ""
            embedding = OpenAIEmbeddings(model="text-embedding-3-small")
            new_vectorstore = FAISS.load_local(
                "faiss_index_react",
                embeddings=embedding,
                allow_dangerous_deserialization=True,
            )

            prompt = """
            Kamu merupakan seorang yang ingin melamar pekerjaan pada suatu perushaan. \
            berikan branding yang baik agar dapat meyakinkan Human Resource Development.

            <context>
                {context}
            </context>
            
            {input}
            """
            retrival_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
            combine_doc_chain = create_stuff_documents_chain(
                OpenAI(), retrival_qa_chat_prompt
            )
            retrival_chain = create_retrieval_chain(
                new_vectorstore.as_retriever(), combine_doc_chain
            )
            for chunk in retrival_chain.stream({"input": user_input}):
                if "answer" in chunk:
                    ai_response += chunk["answer"]
                    await websocket.send_text(chunk["answer"])
                    print(chunk["answer"], end="", flush=True)
                pass

            # response = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            #
            # ai_response = ""
            #
            # async for chunk in response.astream("Give me some advice for code"):
            #     # chunks.append(chunk)
            #     ai_response += chunk
            #     await websocket.send_text(chunk)
            #     print(chunk, end="", flush=True)
            # chat_responses.append(ai_response)

        except Exception as e:
            await websocket.send_text(f"Error: {str(e)}")
            break


# @app.post("/", response_class=HTMLResponse)
# async def chat(request: Request, user_input: Annotated[str, Form()]):
#
#     chat_log.append({'role': 'user', 'content': user_input})
#     chat_responses.append(user_input)
#
#     response = openai.chat.completions.create(
#         model='gpt-4',
#         messages=chat_log,
#         temperature=0.6
#     )
#
#     bot_response = response.choices[0].message.content
#     chat_log.append({'role': 'assistant', 'content': bot_response})
#     chat_responses.append(bot_response)
#
#     return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})
#
#
# @app.get("/image", response_class=HTMLResponse)
# async def image_page(request: Request):
#     return templates.TemplateResponse("image.html", {"request": request})
#
#
# @app.post("/image", response_class=HTMLResponse)
# async def create_image(request: Request, user_input: Annotated[str, Form()]):
#
#     response = openai.images.generate(prompt=user_input, n=1, size="256x256")
#
#     image_url = response.data[0].url
#     return templates.TemplateResponse(
#         "image.html", {"request": request, "image_url": image_url}
#     )
