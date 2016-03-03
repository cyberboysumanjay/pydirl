import click
from app import main

@click.command(context_settings={"auto_envvar_prefix":"PYDIRL"})
@click.version_option()
@click.argument('root', type=click.Path(), metavar='[PATH]', default='./', required=False)
@click.option('-p', '--port', type=click.IntRange(min=1, max=65535), metavar="<port>", help='listening port')
@click.option('-a', '--address', type=click.STRING, metavar="<address>", help='address to bind')
@click.option('-d', '--debug', is_flag=True, help='debug mode')
@click.option('--folder-size', is_flag=True, help='calculate size also for folders (WARNING: could become really slow)')
@click.option('--last-modified', is_flag=True, help='display last modified time')
def pydirl(root, port, address, debug, folder_size, last_modified):
    conf = {'ROOT': root,
            'DEBUG': debug,
            'FOLDER_SIZE': folder_size,
            'LAST_MODIFIED': last_modified}
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
    pydirl()
