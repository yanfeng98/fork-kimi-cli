import time

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.spinner import Spinner
from rich.table import Table

console = Console()

names: str = """
在创建 `Spinner("名称")` 时，你可以使用以下常见名称（Rich 内置了数十种）：
*   `"dots"`: 经典的点状旋转（默认）
*   `"hearts"`: 心形跳动
*   `"clock"`: 时钟旋转
*   `"moon"`: 月相变化
*   `"earth"`: 地球自转
*   `"simpleDots"`: 简单的点
"""
console.print(Markdown(names))

spinner = Spinner("dots", text="正在加载数据，请稍候...", style="green")

with Live(spinner, refresh_per_second=10):
    time.sleep(3)
    spinner.update(text="即将完成...")
    time.sleep(2)

console.print("[red]加载完成！[/red]")

table = Table()

table.add_column("任务 ID")
table.add_column("状态")
table.add_column("进度")

table.add_row("Task-001", "处理中", Spinner("earth", style="blue"))

with Live(table, refresh_per_second=10):
    time.sleep(3)
