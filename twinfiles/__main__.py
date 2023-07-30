import typer

from .finder import Finder


def main(path: str, delete: bool = False, list: bool = False):
    if delete and list:
        typer.echo("You can't delete and list at the same time.")
        raise typer.Exit()

    finder = Finder(path)
    finder.get_file_stats()
    finder.find_same_size()
    finder.find_same_content()

    if delete:
        finder.delete()
    if list:
        finder.list()


def run_main():
    typer.run(main)


if __name__ == "__main__":
    run_main()
