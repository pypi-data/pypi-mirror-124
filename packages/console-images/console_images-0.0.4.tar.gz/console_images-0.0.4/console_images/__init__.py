import typing
import os
import platform
import time
import colorama
from PIL import Image, ImageSequence
from math import ceil


def get_terminal_size() -> typing.Tuple[int, int]:
    columns: int
    rows: int
    try:
        columns, rows = os.get_terminal_size(0)
    except OSError:
        columns, rows = 160, 80
    return columns, rows

def clear_term() -> None:
    if platform.system() == "Linux":
        os.system("clear")
    elif platform.system() == "Windows":
        os.system("cls")


table: typing.Sequence = [" ", "▂", "▃", "▄", "▅", "▆", "▇", "█"]


colors = {"GREEN": [colorama.Style.DIM + colorama.Fore.GREEN, colorama.Fore.GREEN,
                    colorama.Style.BRIGHT + colorama.Fore.GREEN, colorama.Style.DIM + colorama.Fore.LIGHTGREEN_EX,
                    colorama.Fore.LIGHTGREEN_EX, colorama.Style.BRIGHT + colorama.Fore.LIGHTGREEN_EX],
          "RED": [colorama.Style.DIM + colorama.Fore.RED, colorama.Fore.RED, colorama.Style.BRIGHT + colorama.Fore.RED,
                  colorama.Style.DIM + colorama.Fore.LIGHTRED_EX, colorama.Fore.LIGHTRED_EX,
                  colorama.Style.BRIGHT + colorama.Fore.LIGHTRED_EX],
          "YELLOW": [colorama.Style.DIM + colorama.Fore.YELLOW, colorama.Fore.YELLOW,
                     colorama.Style.BRIGHT + colorama.Fore.YELLOW, colorama.Fore.LIGHTYELLOW_EX,
                     colorama.Style.DIM + colorama.Fore.LIGHTYELLOW_EX, colorama.Style.BRIGHT + colorama.Fore.LIGHTYELLOW_EX],
          "MAGENTA": [colorama.Style.DIM + colorama.Fore.MAGENTA, colorama.Fore.MAGENTA,
                      colorama.Style.BRIGHT + colorama.Fore.MAGENTA, colorama.Fore.LIGHTMAGENTA_EX,
                      colorama.Style.DIM + colorama.Fore.LIGHTMAGENTA_EX, colorama.Style.BRIGHT + colorama.Fore.LIGHTMAGENTA_EX],
          "CYAN": [colorama.Style.DIM + colorama.Fore.CYAN, colorama.Fore.CYAN,
                   colorama.Style.BRIGHT + colorama.Fore.CYAN, colorama.Fore.LIGHTCYAN_EX,
                   colorama.Style.DIM + colorama.Fore.LIGHTCYAN_EX, colorama.Style.BRIGHT + colorama.Fore.LIGHTCYAN_EX],
          "WHITE": [colorama.Style.DIM + colorama.Fore.WHITE, colorama.Fore.WHITE,
                    colorama.Style.BRIGHT + colorama.Fore.WHITE, colorama.Fore.LIGHTWHITE_EX,
                    colorama.Style.DIM + colorama.Fore.LIGHTWHITE_EX, colorama.Style.BRIGHT + colorama.Fore.LIGHTWHITE_EX],
          "BLACK": [colorama.Style.DIM + colorama.Fore.BLACK, colorama.Fore.BLACK,
                    colorama.Style.BRIGHT + colorama.Fore.BLACK, colorama.Fore.LIGHTBLACK_EX,
                    colorama.Style.DIM + colorama.Fore.LIGHTBLACK_EX, colorama.Style.BRIGHT + colorama.Fore.LIGHTBLACK_EX],
          "BLUE": [colorama.Style.DIM + colorama.Fore.BLACK, colorama.Fore.BLACK,
                   colorama.Style.BRIGHT + colorama.Fore.BLACK, colorama.Fore.LIGHTBLACK_EX,
                   colorama.Style.DIM + colorama.Fore.LIGHTBLACK_EX, colorama.Style.BRIGHT + colorama.Fore.LIGHTBLACK_EX]}


def color_it(color: tuple) -> str:
    if all([col > 160 for col in color]):
        return colors["WHITE"][round((len(colors["WHITE"]) - 1) / 255 * (color[1] + color[2]) / 2)]
    if all([col < 60 for col in color]):
        return colors["BLACK"][round((len(colors["BLACK"]) - 1) / 255 * (color[1] + color[2]) / 2)]
    if color[1] + color[2] > color[0] * 2 + 40:
        return colors["CYAN"][round((len(colors["CYAN"]) - 1) / 255 * (color[1] + color[2]) / 2)]
    if color[0] + color[2] > color[1] * 2 + 40:
        return colors["MAGENTA"][round((len(colors["MAGENTA"]) - 1) / 255 * (color[2] + color[1]) / 2)]
    if sum(color[0:2]) > color[2] * 2 + 40:
        return colors["YELLOW"][round((len(colors["YELLOW"]) - 1) / 255 * (color[1] + color[0]) / 2)]
    if max(color) == color[1] and color[1] > 200:
        return colors["GREEN"][round((len(colors["GREEN"]) - 1) / 255 * color[1])]
    if max(color) == color[0] and color[0] > 200:
        return colors["RED"][round((len(colors["RED"]) - 1) / 255 * color[0])]
    if max(color) == color[2] and color[2] > 200:
        return colors["BLUE"][round((len(colors["BLUE"]) - 1) / 255 * color[0])]
    return ""


def convert(depth: int) -> str:
    return table[round((len(table) - 1) / 255 * depth)]


def print_image(path: str, columns: int, rows: int, center: bool = True) -> None:
    terminal_size: typing.Tuple[int, int] = get_terminal_size()
    image: Image.Image = Image.open(path)
    image = image.convert("RGB").resize((terminal_size[0] // columns, terminal_size[1] // rows))
    imagel: Image.Image = image.convert("L")
    for i in range(0, image.height):
        if center:
            print(" " * ceil(terminal_size[0] / 2 - terminal_size[0] / columns / 2), end="")
        for j in range(0, image.width):
            middle: typing.Tuple[int, int, int]
            print(color_it(image.getpixel((j, i))) + convert(imagel.getpixel((j, i))) + colorama.Style.RESET_ALL,
                  end='')
        print()


def generate_image(path: str, columns: int, rows: int) -> typing.Generator:
    image: Image.Image = Image.open(path)
    image = image.convert("RGB").resize((columns, rows))
    imagel: Image.Image = image.convert("L")
    for i in range(0, image.height):
        result: str = ""
        for j in range(0, image.width):
            middle: typing.Tuple[int, int, int]
            result += color_it(image.getpixel((j, i))) + convert(imagel.getpixel((j, i))) + colorama.Style.RESET_ALL
        yield result


def show_gif(path: str) -> None:
    img: Image.Image = Image.open(path)
    while True:
        for image in ImageSequence.Iterator(img):
            columns, rows = get_terminal_size()
            image = image.convert("RGB").resize((columns, rows))
            imagel = image.convert("L")
            for i in range(0, image.height):
                for j in range(0, image.width):
                    print(
                        color_it(image.getpixel((j, i))) + convert(imagel.getpixel((j, i))) + colorama.Style.RESET_ALL,
                        end='')
                print()

            time.sleep(1 / 30)
            clear_term()

