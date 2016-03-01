import os

from flask import Flask, safe_join, send_file, render_template, abort
from flask_bootstrap import Bootstrap
from files_utils import get_file_size, get_file_mimetype, get_folder_size

def create_app(conf={}):
    app = Flask(__name__)
    app.config.update(
        DEBUG=True,
        BOOTSTRAP_SERVE_LOCAL=True,
        ROOT=os.environ['PWD']
    )
    app.config.update(conf)

    Bootstrap(app)

    root = app.config['ROOT']
    app.logger.debug("Serving root: '{}'".format(root))

    @app.route('/favicon.ico')
    def favicon():
        abort(404)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>/')
    def folder_route(path):
        path = safe_join(root, path)
        if os.path.isfile(path):
            return send_file(path)
        entries = {'dirs':{}, 'files':{}}
        for e in os.listdir(path):
            e_path = os.path.join(path, e)
            if os.path.isdir(e_path):
                size, files_num = get_folder_size(e_path)
                entries['dirs'][e] = {'size': size, 'files_num': files_num}
            elif os.path.isfile(e_path):
                size = get_file_size(e_path)
                mime = get_file_mimetype(e_path)
                entries['files'][e] = {'size': size, 'mime':mime}
            else:
                app.logger.debug('Skipping unknown element: {}'.format(e))
        return render_template('template.html', entries=entries)
    return app

    @app.route('/<path:path>')
    def file_route(path):
        path = safe_join(root, path)
        return send_file(path)


def main(conf={}):
    app = create_app(conf)
    app.run(host=conf.get('ADDRESS', None),
            port=conf.get('PORT', None))


if __name__ == "__main__":
    main()
