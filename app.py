from logs import log
from app import create_app

app = create_app()

if __name__ == '__main__':
    log(f'Task-Manager running at port: {app.config["PORT"]}')
    app.run(host='0.0.0.0', port=app.config["PORT"], debug=True)
