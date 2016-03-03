import os
import logging

from flask import Flask, safe_join, send_file, render_template, abort
from flask_bootstrap import Bootstrap

from files_utils import get_file_size, get_file_mimetype, get_folder_size
from tools import gevent_run, init_loggers


def create_app(conf={}):
    app = Flask('pydirl')
    app.config.update(
            DEBUG=True,
            ADDRESS='127.0.0.1',
            PORT='5000',
            BOOTSTRAP_SERVE_LOCAL=True,
            ROOT=os.environ['PWD'],
            FOLDER_SIZE=False
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

    #@app.route('/<path:path>')
    def file_route(path):
        path = safe_join(root, path)
        return send_file(path)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def folder_route(path):
        path = safe_join(root, path)
        app.logger.debug("Absolute requested path: '{}'".format(path))
        if os.path.isfile(path):
            return send_file(path)
        entries = {'dirs':{}, 'files':{}}
        for e in os.listdir(path):
            e_path = os.path.join(path, e)
            if os.path.isdir(e_path):
                if app.config['FOLDER_SIZE']:
                    size, files_num = get_folder_size(e_path)
                else:
                    size = None;
                    files_num = None;
                entries['dirs'][e] = {'size': size, 'files_num': files_num}
            elif os.path.isfile(e_path):
                size = get_file_size(e_path)
                mime = get_file_mimetype(e_path)
                entries['files'][e] = {'size': size, 'mime':mime}
            else:
                app.logger.debug('Skipping unknown element: {}'.format(e))
        return render_template('template.html', entries=entries)

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
