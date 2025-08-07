from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os


load_dotenv()

llm=ChatOpenAI(
    model='deepseek/deepseek-chat-v3-0324:free',
    api_key=os.environ['OPENROUTER_API_KEY'],
    base_url='https://openrouter.ai/api/v1'
)

class ChatClass(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

def chat_node(state:ChatClass):
    messages=state['messages']

    response=llm.invoke(messages).content

    return{'messages':[response]}


checkpointer=InMemorySaver()

graph=StateGraph(ChatClass)

graph.add_node('chat_node',chat_node)
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot =graph.compile(checkpointer=checkpointer)

