import streamlit as st
from langraph_database_backend import chatbot,retrive_allthread
from langchain_core.messages import HumanMessage
import uuid

#******************************************************* Utility Function    **********************************************************

def generate_thred_id():
    thread_id=uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id=generate_thred_id()
    st.session_state['thread_id']=thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history']=[]


def add_thread(thread_id):
    if thread_id not in st.session_state['chat_thread']:
        st.session_state['chat_thread'].append(thread_id)

def load_convo(thread_id):
    state=chatbot.get_state(config={'configurable':{'thread_id':thread_id}})
    return state.values.get('messages',[])





#******************************************************* Session Setup    ****************************************************************
# st.session_state ->dict -> 
if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=generate_thred_id()

if 'chat_thread' not in st.session_state:
    st.session_state['chat_thread']=retrive_allthread()

add_thread(st.session_state['thread_id'])

#******************************************************* SideBar UI    ********************************************************************

st.sidebar.title("LangGraph Chatbot")
if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversation')
for thread_id in st.session_state['chat_thread']:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id']=thread_id
        messages=load_convo(thread_id)

        temp_messages=[]

        for msg in messages:
            if isinstance(msg,HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role':role,'content':msg.content})

        st.session_state['message_history']=temp_messages

#******************************************************* Main UI    ***********************************************************************

#loading the conversation
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


# {'role':'user',''content:'HI'}
# {'role':'assistant',''content:'how can i assist you'}

user_input=st.chat_input('Type here')

if user_input:
    #first add the message to the history
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input  )

    CONFIG={'configurable':{'thread_id':st.session_state['thread_id']}}

    
    with st.chat_message('assistant'):
        ai_message=st.write_stream(
            message_chunk.content for message_chunk,metadata in chatbot.stream(
                {'messages':[HumanMessage(content=user_input)]},
                  config=CONFIG,
                  stream_mode='messages'
            )
        )
    st.session_state['message_history'].append({'role':'assistant','content':ai_message})