from app import create_app

app = create_app(debug=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=80)