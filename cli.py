import click
from app import main

@click.command()
@click.version_option()
@click.argument('root', type=click.Path(), metavar='[PATH]', default='./', required=False)
@click.option('-p', '--port', type=click.IntRange(min=1, max=65535), metavar="<port>", help='listening port')
@click.option('-a', '--address', type=click.STRING, metavar="<address>", help='adress to bind')
@click.option('-d', '--debug', is_flag=True, help='debug mode')
def pydirl(root, port, address, debug):
    conf = {'ROOT': root,
            'DEBUG': debug }
    if port:
        conf['PORT'] = port
    if address:
        conf['ADDRESS'] = address

    try:
        main(conf)
    except Exception as e:
        if conf.get('DEBUG', False):
            raise
        else:
            click.secho(str(e), fg='yellow', err=True)
            exit(1)


if __name__ == "__main__":
    pydirl(auto_envvar_prefix='PYDIRL')
