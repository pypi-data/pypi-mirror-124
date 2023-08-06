from rich.console import Console
from rich import box
from rich.align import Align
from rich.table import Table
from rich.text import Text
import json
import os

this_dir, this_filename = os.path.split(__file__)
DATA_PATH = os.path.join(this_dir, "text.json")

with open(DATA_PATH, encoding="utf8") as f:
        data = json.load(f)

console = Console()

def main():

        console.print("Hey Folks", style="bold red", justify="center")
        console.print("I am",data['name'], style="bold green", justify="center")

# table = Table(title="Hey Folks!", show_header=False)
# table.add_column(justify="center", style="cyan")
# table.add_column(justify="left", style="magenta")


# table_centered = Align.center(table)
# # console.print(table_centered)
