'''
https://flask.palletsprojects.com/en/2.3.x/tutorial/factory/
A Flask application is an instance of the Flask class. Everything about the application, such as 
configuration and URLs, will be registered with this class.

The most straightforward way to create a Flask application is to create a global Flask instance 
directly at the top of your code, like how the “Hello, World!” example did on the previous page. 
While this is simple and useful in some cases, it can cause some tricky issues as the project grows.

Instead of creating a Flask instance globally, you will create it inside a function. This function 
is known as the application factory. Any configuration, registration, and other setup the application
 needs will happen inside the function, then the application will be returned.
'''
import os

from flask import Flask

# create_app is the application factory function.
def create_app(test_config=None):
    '''
    create and configure the app (creates the Flask instance)
    
    __name__ is the name of the current Python module. The app needs to know where it’s located to set
      up some paths, and __name__ is a convenient way to tell it that.

    instance_relative_config=True tells the app that configuration files are relative to the instance 
    folder. The instance folder is located outside the flaskr package and can hold local data that shouldn’t 
    be committed to version control, such as configuration secrets and the database file.
    '''
    app = Flask(__name__, instance_relative_config=True)
    # sets some default configuration that the app will use
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'web.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
######################## INÍCIO SEÇÃO ESPECIFICIDADES ###################33
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # Define and Access the Database: registrar init-db com o app
    # https://flask.palletsprojects.com/en/2.3.x/tutorial/database/
    # executa a função definida lá, registrando os comandos
    # app agora "sabe" das funções e pode acioná-las
    from . import db
    db.init_app(app)
    # https://flask.palletsprojects.com/en/2.3.x/tutorial/views/
    # registrando o primeiro blueprint
    from . import auth
    app.register_blueprint(auth.bp)

######################## FIM SEÇÃO ESPECIFICIDADES ########################
    # no final, a fábrica do app retorna....o app, funcionando
    return app

# Para rodar, use o comando flask no diretório do pacote
#
# $ flask --app .\src\web run --debug
# * Serving Flask app '.\src\web'
# * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
# Acesse http://127.0.0.1:5000/hello