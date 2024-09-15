import getpass
import os
from langchain_openai import OpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    model = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    messages = [
        SystemMessage(content="Translate the following from English into Italian"),
        HumanMessage(content="hi!"),
    ]

    print(model.invoke(messages))

    chunks = []
    for chunk in model.stream("Berikan puisi tentang koruptor"):
        chunks.append(chunk)
        print(chunk, end="", flush=True)
