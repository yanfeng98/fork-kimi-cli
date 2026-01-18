from rich.align import Align
from rich.box import ROUNDED
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

message = Text.from_markup("系统状态: [green]正常运行[/]\n当前时间: 2026-01-18")
content = Align(message, align="center")

panel = Panel(
    content,
    title="[bold yellow]控制面板[/]",
    subtitle="[dim]按 Ctrl+C 退出[/]",
    border_style="blue",
    box=ROUNDED,
    padding=(1, 2),
    expand=True,
    highlight=True,
)

console.print(panel)
