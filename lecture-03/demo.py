import subprocess
import ollama
import json

# ---- 定义函数工具（给 Ollama 暴露的能力） ----
def lint_code(code: str) -> str:
    """调用 flake8 检查 Python 代码"""
    try:
        process = subprocess.Popen(
            ["flake8", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = process.communicate(code)
        if stdout.strip():
            return stdout
        elif stderr.strip():
            return f"Error: {stderr}"
        else:
            return "No lint issues ✅"
    except FileNotFoundError:
        return "flake8 not installed. Run: pip install flake8"

tools = [
    {
        "name": "lint_code",
        "description": "Check Python code with flake8 linter",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The Python code to lint",
                },
            },
            "required": ["code"],
        },
    }
]

# ---- 主逻辑：让 Ollama 生成代码 & 调用 linter ----
def main():
    # 给 Ollama 提示：请写函数并调用 linter 检查
    prompt = "Write a Python factorial function and call the linter to check it."

    response = ollama.chat(
        model="llama3.1",   # 选择支持 function calling 的模型
        messages=[{"role": "user", "content": prompt}],
        tools=tools,
    )

    message = response["message"]

    if message.get("tool_calls"):
        for tool_call in message["tool_calls"]:
            if tool_call["name"] == "lint_code":
                args = tool_call["arguments"]
                code_to_check = args["code"]
                print("=== Generated Code ===\n", code_to_check)

                result = lint_code(code_to_check)
                print("\n=== Linter Output ===\n", result)

                # 把结果再反馈给模型（可选）
                followup = ollama.chat(
                    model="llama3.1",
                    messages=[
                        {"role": "user", "content": prompt},
                        message,
                        {
                            "role": "tool",
                            "name": "lint_code",
                            "content": result,
                        },
                    ],
                )
                print("\n=== Final Model Reply ===\n", followup["message"]["content"])
    else:
        print("Model did not request tool call:", message)

if __name__ == "__main__":
    main()

## #!/usr/bin/python
## # coding: utf-8
## from pyflakes import reporter,api
## import io
## 
## def check_code(code):
##     stream = io.StringIO()
##     rep = reporter.Reporter(stream, stream)
##     num = api.check(code, "<code>", rep)
##     if num:
##         issues = stream.getvalue().strip()
##     else:
##         issues = ""
##     return num, issues
## 
## 
## num, issues = check_code("print(a)")
## print(num, issues)
## 
## num, issues = check_code("print(1)")
## print(num, issues)

