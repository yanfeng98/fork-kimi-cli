from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings

kb = KeyBindings()


@kb.add("c-t")
def _(event):
    event.app.current_buffer.insert_text("Hello World")


if __name__ == "__main__":
    print("试试按 'Ctrl-T' 插入文本，或按 'Ctrl-Q' 退出。")
    text = prompt("请输入: ", key_bindings=kb)
    print(f"你输入了: {text}")
