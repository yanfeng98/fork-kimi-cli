from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory

history = InMemoryHistory()

print("输入一些内容（输入 'exit' 退出）。")
print("提示：输入几次后，尝试按 '向上箭头' 键查看历史。\n")

while True:
    user_input = prompt(">>> ", history=history)

    if user_input.strip() == "exit":
        break

    print(f"你输入了: {user_input}")
