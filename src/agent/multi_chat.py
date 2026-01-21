import uuid

from langchain_classic.agents import initialize_agent, AgentType
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_core.messages import HumanMessage, AIMessage
from src.agent.multi_chat_prompt import multi_chat_prompt
from src.agent.model import local_qwen
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import FileChatMessageHistory

# 将文件管理tools绑定到llm
file_tools = FileManagementToolkit(root_dir="D:\\source_code\\git_code\\python_code\\agent_demo\\data").get_tools()
llm_with_tools = local_qwen.bind_tools(file_tools)

agent = initialize_agent(
    tools=file_tools,
    llm=llm_with_tools,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 链式
# chain = multi_chat_prompt | agent | StrOutputParser()   #

chain = multi_chat_prompt | agent

# chat history实现
chat_history = ChatMessageHistory()
chat_history.add_user_message(HumanMessage(content="我叫Harvey，我们要做Agent项目"))
chat_history.add_ai_message(AIMessage(content="好的，你想从哪部分开始呢？"))

# 存储session，记录不同用户的chat history
store = {"1": []}

# 传递session id
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    print(store)
    return store[session_id]

# 基于文件的session，保存到file
def get_session_history_via_file(session_id: str):
    return FileChatMessageHistory(f"{session_id}.json")

# RunnableWithMessageHistory
chat_with_history = RunnableWithMessageHistory(
    runnable=chain,
    # get_session_history=get_session_history,
    get_session_history=get_session_history_via_file,
    input_messages_key='question',
    history_messages_key='chat_history',
)

# for chunk in chain.stream({"question": "我们要做什么项目？","chat_history": chat_history.messages}):
#     print(chunk, end='')

# 每次都生成一个新的sessionId，实际业务中应该每个用户的sessionId都是唯一的
session_id = uuid.uuid4()
print(session_id)

# 使用命令行工具，chat history保持在一次运行过程中
while True:
    user_input = input("用户：")
    if user_input.lower() == "quit":
        break

    # invoke是同步的方式
    # stream是流式的方式
    response = chat_with_history.stream(
        {"question": user_input},
        config={'configurable':{'session_id':session_id}},
    )

    print("助理：")
    for chunk in response:
        print(chunk, end='')

    print("\n")