from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyCompleter, WordCompleter

words = ["apple", "apricot", "banana", "blueberry", "cherry", "coconut", "date"]

base_completer = WordCompleter(words)
my_fuzzy_completer = FuzzyCompleter(base_completer)

if __name__ == "__main__":
    print("试着输入 'nut' 来匹配 'coconut'，或者 'rr' 来匹配 'cherry'/'blueberry'")
    text = prompt("请选择水果: ", completer=my_fuzzy_completer)
    print(f"你选择了: {text}")
