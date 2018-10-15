import click


@click.command()
def command():
    try:
        print("== Ejecutaste el comando: {{ command_name }} ==")
    except Exception as e:
        print("== Ocrrio un problema durante la ejecución del comando: {{ command_name }} ==")
        print("="*10)
        print(e)
