import click


@click.command()
def command(ctx):
    try:
        print("== Its a test ==")
    except Exception as e:
        print("== Ocrrio un problema durante la actualización ==")
        print("="*10)
        print(e)
