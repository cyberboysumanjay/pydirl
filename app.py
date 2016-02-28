import os

from flask import Flask, safe_join, send_file, render_template
from flask_bootstrap import Bootstrap

def create_app(conf={}):
    app = Flask(__name__)
    app.config.update(
        DEBUG=True,
    )

    Bootstrap(app)

    root = os.environ['PWD']

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def route(path):
        path = safe_join(root, path)
        if os.path.isfile(path):
            return send_file(path)
        entries = {'dirs':[], 'files':[]}
        for e in os.listdir(path):
            e = os.path.join(path, e)
            if os.path.isdir(e):
                entries['dirs'].append(e)
            elif os.path.isfile(e):
                entries['files'].append(e)
            else:
                app.logger.debug('Skipping unknown element: {}'.format(e))
        return render_template('template.html', entries=entries)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
