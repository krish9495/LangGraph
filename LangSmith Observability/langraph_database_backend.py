from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os
import sqlite3


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

conn=sqlite3.connect(database='chatbot.db',check_same_thread=False)

checkpointer=SqliteSaver(conn=conn)

graph=StateGraph(ChatClass)

graph.add_node('chat_node',chat_node)
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot =graph.compile(checkpointer=checkpointer)




# test
# CONFIG={'configurable':{'thread_id':'thread-1'}}
# response=chatbot.invoke(
#     {'messages':[HumanMessage(content='What is my name')]},
#     config=CONFIG
# )

# print(response)

def retrive_allthread():
    all_thread=set()
    for checkpoint in checkpointer.list(None):
        all_thread.add(checkpoint.config['configurable']['thread_id'])
    return list(all_thread)