import typer

from auto_gui import parsing

app = typer.Typer()

@app.command()
def run(path: str = typer.Option(
        str("script"),
        "--path",
        "-p",
        prompt="Script path",
    )):
    parsing.Parsing(script_path=path).run()

if __name__ == "__main__":
    app()