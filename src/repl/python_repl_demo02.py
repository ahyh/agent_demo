from langchain_core.prompts import PromptTemplate
from langchain_classic.agents import initialize_agent, AgentType
from langchain_experimental.tools.python.tool import PythonREPLTool

from src.common import local_qwen

# 定义工具
tools = [PythonREPLTool()]
tool_names = ["PythonREPLTool"]

# 创建agent
agent = initialize_agent(
    tools=tools,
    llm=local_qwen,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True  # 添加错误处理
)

# 创建提示词
prompt_template = PromptTemplate.from_template(
    template="""
    尽你所能回答以下问题或执行用户的命令，你可以使用以下工具：{tool_names}
    --
    请按照以下格式进行思考：
    ```
    
    # 思考的过程
    - 问题：你必须回答的输入问题
    - 思考：你考虑应该怎么做
    - 行动：要采取的行动应该是[{tool_names}]中的一个
    - 行动输入：行动的输入
    - 观察：行动的结果
    ...(这个思考/行动/行动输入/观察可以重复多次)
    # 最终答案
    对原始输入问题的最终答案
    ```
    --
    注意：
    - PythonREPLTool工具的入参是python代码，不允许添加```python 或 ```py 等标记
    --
    问题：{question}
    """
)

prompt = prompt_template.format(
    tool_names=",".join(tool_names),
    question=f"""
        要求：
        1. 向 D:\\source_code\\git_code\\python_code\\agent_demo\\data 目录下写入一个新文件，名称为index.html
        2. 写一个在线教育产品的官网，包含3个tab，分别是：首页，实战可，体系课和关于我们
        3. 首页展示3个模块，分别是：热门课程，上新课程，爆款课程
        4. 关于我们展示平台的联系方式等基本信息
     """
)

resp = agent.invoke(prompt)
