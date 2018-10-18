import click
import os
import yaml


config_folder = os.path.join(os.path.dirname(__file__), 'config.yml')
command_folder = os.path.join(os.path.dirname(__file__), 'commands')


class Context(object):
    def __init__(self):
        self.config = yaml.load(open(config_folder, 'r').read())


pass_context = click.make_pass_decorator(Context, ensure=True)


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
@pass_context
def cli(ctx):
    pass


if __name__ == '__main__':
    @pass_context
    cli(ctx)
