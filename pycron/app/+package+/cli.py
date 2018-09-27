import click
import os


command_folder = os.path.join(os.path.dirname(__file__), 'commands')


class schedulesCli(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(command_folder):
            if filename.endswith('.py'):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            ns = {}
            fn = os.path.join(command_folder, name + '.py')
            with open(fn) as f:
                code = compile(f.read(), fn, 'exec')
                eval(code, ns, ns)
            return ns['command']
        except Exception as e:
            return


cli = schedulesCli(help='Esta herramienta ayuda a ejecutar crones.')


@click.command(cls=schedulesCli)
def cli():
    pass


if __name__ == '__main__':
    cli()
