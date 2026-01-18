from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, merge_completers

animal_completer = WordCompleter(["cat", "dog", "bird", "horse"], meta_dict={"cat": "动物"})
color_completer = WordCompleter(["red", "green", "blue", "yellow"], meta_dict={"red": "颜色"})

combined_completer = merge_completers([animal_completer, color_completer])

if __name__ == "__main__":
    print("试着输入 'r' (匹配 bird/horse/red) 或 'c' (匹配 cat)")
    text = prompt("输入: ", completer=combined_completer)
    print(f"你选择了: {text}")
