from langchain_experimental.utilities import PythonREPL

python_repl = PythonREPL()

# 将python代码作为参数
ret = python_repl.run("print(1+1)")

print(ret)