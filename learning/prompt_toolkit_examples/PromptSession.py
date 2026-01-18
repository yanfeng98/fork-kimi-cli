from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.styles import Style


def main():
    commands = ["start", "stop", "restart", "status", "help", "exit", "quit"]
    command_completer = WordCompleter(commands, ignore_case=True)

    my_style = Style.from_dict(
        {
            "prompt": "ansicyan bold",
            "input": "#ff0066",
        }
    )

    session = PromptSession(history=InMemoryHistory(), completer=command_completer, style=my_style)

    print("欢迎使用交互式命令行！(输入 'exit' 或按 Ctrl+C 退出)")

    while True:
        try:
            text = session.prompt("MyShell> ")
            if not text.strip():
                continue

            if text.lower() in ("exit", "quit"):
                print("再见！")
                break

            print(f"你输入了: {text}")

            if text == "help":
                print("可用命令: " + ", ".join(commands))

        except KeyboardInterrupt:
            print("\n检测到 Ctrl+C，再次按下或输入 exit 退出。")
            continue
        except EOFError:
            print("\nExiting...")
            break


if __name__ == "__main__":
    main()
