from project import app, ConfigFlask

if __name__ == '__main__':
    app.run(host=ConfigFlask.HOST, port=ConfigFlask.PORT)
