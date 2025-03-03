# https://github.com/Textualize/rich?tab=readme-ov-file
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({
    "success": "bold bright_green",
    "head": "bold bright_white",
    "info": "dim cyan",
    "warn": "bold magenta",
    "bug": "bold bright_red",
    "alrt": "red",
    "counter": "bold bright_yellow"
})


printc = Console(theme=custom_theme).print
