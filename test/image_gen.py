import os
from langchain.chains import LLMChain
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    # model = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    llm = OpenAI(
        temperature=0.9,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    prompt = PromptTemplate(
        input_variables=["image_desc"],
        template="Generate a detailed prompt to generate an image based on the following description: {image_desc}",
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    image_url = DallEAPIWrapper().run(chain.run("halloween"))
    print(image_url)
