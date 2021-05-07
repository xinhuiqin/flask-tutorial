import os
from flask import Flask
from flask import render_template


# 名字一般是make_app()或者create_app()参考：https://flask.palletsprojects.com/en/1.1.x/cli/
# 如果不是上面的两个名字，那么需要设置 FLASK_APP=包名:方法名，如 export  FLASK_APP=flaskr:init_app
def create_app(test_config=None):
    """
    1、init_app() 方法的使用对应“工厂方法模式”，不是“抽象工厂模式”。
    2、“工厂方法模式”的具体实现为：在函数（或类方法）里面实例化一个类，并对类的实例执行某些操作，然后返回该类的实例。
       这里使用函数实现。
    3、这里使用“工厂方法模式”的目的是根据不同的环境（如开发环境、测试环境、生产环境），在实例化的时候进行不同的设置。
    """
    # 首先创建实例
    app = Flask(__name__, instance_relative_config=False)
    # 配置数据库
    # app.config 是 flask.config.Config 类型，是一个字典。 然后调用Config.from_mapping()方法
    # Config.from_mapping()方法会给app.config添加属性
    app.config.from_mapping(
        SECRET_KEY='dev',
        # app.instance_path 会在 flaskr 目录下创建一个 instance 目录,
        # 效果示例：/home/codists/project/flask-tutorial/flaskr/instance/flaskr.sqlite
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    # 根据传入的参数进行配置，这是“工厂方法模式”思想的实际应用
    if test_config is None:
        # silent 参数：如果没有 config.py 文件不存在，且 silent=True，那么某些情况下返回 False，不抛出异常
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # 创建目录，后续SQLite数据库使用
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    # @app.route('/hello')
    # def hello():
    #     return 'Hello, World!'
    from . import db
    db.init_app(app)

    # 把蓝图注册到应用上
    from . import auth
    # register_blueprint()：做了两件事：1、将blueprint.name添加到 Flask.blueprints 属性
    # 2、调用 Blueprint.register()方法
    app.register_blueprint(auth.bp)
    app.add_url_rule("/", endpoint="index", view_func=auth.register)

    from . import blog
    app.register_blueprint(blog.bp)

    # 这句与 blog 无关
    app.add_url_rule("/", endpoint="index")

    # 测试 base.html 页面
    @app.route('/base')
    def base():
        return render_template('base.html')

    return app


