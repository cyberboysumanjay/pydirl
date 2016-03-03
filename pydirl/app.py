import os
import logging

from flask import Flask, safe_join, send_file, render_template, abort, request
from flask_bootstrap import Bootstrap

from files_utils import get_file_size, get_file_mimetype, get_folder_size, get_mtime
from tools import gevent_run, init_loggers, stream_zipped_dir


def create_app(conf={}):
    app = Flask('pydirl')
    app.config.update(
            DEBUG=True,
            ADDRESS='127.0.0.1',
            PORT='5000',
            BOOTSTRAP_SERVE_LOCAL=True,
            ROOT=os.environ['PWD'],
            FOLDER_SIZE=False,
            LAST_MODIFIED=False
        )

    app.config.update(conf)

    '''dirty trick: prevent default flask handler to be created
      in flask version > 0.10.1 will be a nicer way to disable default loggers
      tanks to this new code mitsuhiko/flask@84ad89ffa4390d3327b4d35983dbb4d84293b8e2
    '''
    app._logger = logging.getLogger(app.import_name)

    Bootstrap(app)

    root = os.path.abspath(app.config['ROOT'])
    app.logger.debug("Serving root: '{}'".format(root))

    @app.route('/favicon.ico')
    def favicon():
        abort(404)

    @app.route('/', defaults={'relPath': ''})
    @app.route('/<path:relPath>')
    def folder_route(relPath):
        path = safe_join(root, relPath)
        app.logger.debug("Absolute requested path: '{}'".format(path))

        if os.path.isfile(path):
            return send_file(path)
        if os.path.isdir(path) and 'download' in request.args:
            zipName = os.path.basename(path) if relPath else 'archive'
            return stream_zipped_dir(path, zipName)

        entries = {'dirs':{}, 'files':{}}
        for e in os.listdir(path):
            e_path = os.path.join(path, e)
            data=dict()
            if os.path.isdir(e_path):
                if app.config['FOLDER_SIZE']:
                    size, files_num = get_folder_size(e_path)
                else:
                    size = None;
                    files_num = None;
                data['size'] = size;
                data['file_num'] = files_num;
                if app.config['LAST_MODIFIED']:
                    data['mtime'] = get_mtime(e_path)
                entries['dirs'][e] = data
            elif os.path.isfile(e_path):
                data['size'] = get_file_size(e_path)
                data['mime'] = get_file_mimetype(e_path)
                if app.config['LAST_MODIFIED']:
                    data['mtime'] = get_mtime(path)
                entries['files'][e] = data
            else:
                app.logger.debug('Skipping unknown element: {}'.format(e))
        return render_template('template.html', entries=entries, relPath=relPath)

    @app.errorhandler(OSError)
    def oserror_handler(e):
        if app.config['DEBUG']:
            app.logger.exception(e)
        else:
            app.logger.error(e)
        return render_template('error.html', message=e.strerror, code=403), 403

    return app


def main(conf={}):
    init_loggers(logNames=['pydirl', 'werkzeug'],
                 logLevel=logging.DEBUG if conf.get('DEBUG', False) else logging.INFO)
    app = create_app(conf)
    gevent_run(app,
               address=app.config.get('ADDRESS'),
               port=int(app.config.get('PORT')),
               reloader=app.config.get('DEBUG'),
               debugger=app.config.get('DEBUG'))


if __name__ == "__main__":
    main()
