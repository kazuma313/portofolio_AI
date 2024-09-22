from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.tools.render import render_text_description
from langchain.schema import AgentAction, AgentFinish
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool, tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import Union, List


load_dotenv()


@tool
def link(type_link:str):
    """give social media link give link"""
    if "social media" in type_link:
        return {
            "github": "https://github.com/kazuma313",
            "linkedIn": "https://www.linkedin.com/in/kurnia-zulda-400665234/",
            "email": "koerzoelmatondang@gmail.com",
        }
    else:
        return "dont have any link"


def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool wtih name {tool_name} not found")


if __name__ == "__main__":
    print("My experiment")
    tools = [link]

    template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought: {agent_scratchpad}
    """

    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )

    intermediate_steps = []

    llm = ChatOpenAI(temperature=0, stop=["\nObservation"])
    agents = (
        {"input": lambda x: x["input"],
         "agent_scratchpad": lambda x: format_log_to_str(x["agent_scratchpad"])
         } | prompt | llm | ReActSingleInputOutputParser()
    )
    agents_step:Union[AgentAction, AgentFinish] = agents.invoke(
        {"input": "give me social media link?",
         "agent_scratchpad": intermediate_steps}
    )
    print(agents_step)

    if isinstance(agents_step, AgentAction):
        tool_name = agents_step.tool
        tool_to_use = find_tool_by_name(tools, tool_name)
        tool_input = agents_step.tool_input

        observation = tool_to_use.func(str(tool_input))
        print(f"{observation=}")
        intermediate_steps.append((agents_step, str(observation)))

    agents_step:Union[AgentAction, AgentFinish] = agents.invoke(
        {"input": "how to get my social media?",
         "agent_scratchpad": intermediate_steps}
    )
    print(agents_step)
