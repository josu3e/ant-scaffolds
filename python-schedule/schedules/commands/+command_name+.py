import click
from schedules.cli import pass_context


@click.command()
@pass_context
def command(ctx):
    try:
        print("== Ejecutaste el comando: {{ command_name }} ==")
        print("datos de configuración")
        print(ctx.config)
    except Exception as e:
        print("== Ocrrio un problema durante la ejecución del comando: {{ command_name }} ==")
        print("="*10)
        print(e)
