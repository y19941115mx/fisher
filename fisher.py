from flask import render_template
from werkzeug.exceptions import HTTPException

from app import create_app

app = create_app(debug=False)


@app.errorhandler(Exception)
def framework_error(e):
    # 调试环境
    if app.config['DEBUG']:
        raise e
    # 生产环境
    else:
        if isinstance(e, HTTPException) and e.code == 404:
            return render_template('404.html'), 404
        else:
            app.logger.exception('error')
            return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=80)