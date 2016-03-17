import click
from .app import main


@click.command(context_settings={"auto_envvar_prefix": "PYDIRL"})
@click.version_option()
@click.argument('root', type=click.Path(), metavar='[PATH]', default='./', required=False)
@click.option('-p', '--port', type=click.IntRange(min=1, max=65535), metavar="<port>", help='listening port')
@click.option('-a', '--address', type=click.STRING, metavar="<address>", help='address to bind')
@click.option('--exclude', type=click.STRING, metavar="<regex>", help='regex to exclude matching files and directories')
@click.option('-d', '--debug', is_flag=True, help='debug mode')
@click.option('--folder-size', is_flag=True, help='calculate size also for folders (WARNING: could become really slow)')
def pydirl(root, port, address, exclude, debug, folder_size):
    '''Quick file sharing solution

       Start a simple web server to share files and folders over HTTP protocol.

      \b
       PATH controls which elements will be shared:
        - if PATH is a directory, all elements under it will be shared.
        - if PATH is a file, single-file mode will be triggered and
          only that file will be shared.
        - if PATH is not given the current directory (PWD) will be used.
    '''

    conf = {'ROOT': root,
            'DEBUG': debug,
            'FOLDER_SIZE': folder_size}
    if port:
        conf['PORT'] = port
    if address:
        conf['ADDRESS'] = address
    if exclude:
        conf['EXCLUDE'] = exclude

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
