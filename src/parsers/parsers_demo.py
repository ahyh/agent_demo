from langchain_classic.output_parsers import DatetimeOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from src.common import llm, local_qwen, prompt_template

parser = StrOutputParser()
chain = prompt_template | local_qwen | parser

resp = chain.invoke(
    input= {
        "role": "计算",
        "domain":"数学计算",
        "question":"100*20=?"
    }
)

print(resp)


print("===============================================")


# 时间parser
date_parser = DatetimeOutputParser()
inst = date_parser.get_format_instructions()
prompt = ChatPromptTemplate.from_messages([
    ("system", f"必须按照以下格式返回日期时间：{inst}"),
    ("user","请将以下自然语言转换为标准日期时间格式：{text}")
])

date_chain = prompt | local_qwen | date_parser
date_resp = date_chain.invoke(
    {"text":"二零二五年五月一日上午十点十分"}
)
print(date_resp)