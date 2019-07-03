from flask import render_template, make_response
from werkzeug.exceptions import HTTPException

from app import create_app
from app.libs.exception import ApiException

from flask_cors import CORS

app = create_app(debug=False)
CORS(app, supports_credentials=True)


@app.errorhandler(Exception)
def framework_error(e):

    if isinstance(e, ApiException):
        return e

    if app.config['DEBUG']:
        raise e

    if isinstance(e, HTTPException) and e.code == 404:
        return render_template('404.html'), 404
    else:
        app.logger.exception('error')
        return render_template('500.html'), 500

@app.after_request
def af_request(resp):     
    """
    #请求钩子，在所有的请求发生后执行，加入headers。
    :param resp:
    :return:
    """
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)