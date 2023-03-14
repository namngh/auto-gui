import typer

from auto_gui import Parsing

app = typer.Typer()

@app.command()
def run(path: str = typer.Option(
        str("script"),
        "--path",
        "-p",
        prompt="Script path",
    )):
    Parsing(script_path=path).run()

if __name__ == "__main__":
    app()