import typer

from .finder import Finder


def main(path: str):
    finder = Finder(path)
    finder.get_file_list()
    finder.find_duplicates()


if __name__ == "__main__":
    typer.run(main)
