from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

my_completer = WordCompleter(
    ["java", "python", "javascript", "rust", "go", "c++"], ignore_case=True
)

# 当你在终端运行这行代码并输入 'j' 或 'py' 时，按下 Tab 键就会看到补全提示
text = prompt("请输入编程语言: ", completer=my_completer)

print(f"你输入了: {text}")
