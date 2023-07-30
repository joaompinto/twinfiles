import typer

from .finder import Finder


def main(path: str, delete: bool = False):
    finder = Finder(path)
    finder.get_file_stats()
    finder.find_same_size()
    finder.find_same_content()
    if delete:
        finder.delete()


def run_main():
    typer.run(main)


if __name__ == "__main__":
    run_main()
