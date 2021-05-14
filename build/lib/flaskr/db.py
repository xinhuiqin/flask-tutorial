"""
1、考虑直接使用数据库还是ORM
2、连接数据库
3、断开与数据库的连接
4、使用命令初始化数据库（可选）
"""
import sqlite3

import click
from flask.cli import with_appcontext
from flask import g
from flask import current_app


def get_db():
    """
    创建数据库链接
    :return: Connection object
    """
    # 判断数据库是否连接
    if 'db' not in g:  # g对象实现了__contain__()方法，所以可以使用 in 操作符 判断
        g.db = sqlite3.connect(
            # todo: 为什么使用current_app 对象
            current_app.config['DATABASE'],
            # todo: 为什么使用 detect_types 参数？
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


# todo: 为什么使用参数 e
def close_db(e=None):
    # 关闭数据库连接，应该使用 Connection 对象，
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """
    初始化数据库：
    1、获取连接对象。
    2、连接对象执行 SQL 语句。
    :return:
    """
    # 获取连接对象
    db = get_db()
    # 执行 SQL 语句
    with current_app.open_resource('scheme.sql', 'rb') as f:
        """
        1、executescript()内部所实现的事：
            1.1 调用游标对象的 cursor() 方法来创建游标对象：cur = conn.cursor()
            1.2 调用游标对象的 executescript() 方法执行多行 SQL 语句。
        """
        # 因为使用 ‘rb’ 模式打开，f.read()得到的是bytes object
        # 所以需要调用 bytes object 的 decode() 方法将其转为 string
        # 需要注意 f.read() 是操作的是数据流，重复读取可能得到的是空。所以，f.read().decode('utf8') 必须写成一句
        db.executescript(f.read().decode('utf8'))


# click.command()函数用法：https://click.palletsprojects.com/en/7.x/api/#decorators
# 命令默认为函数名且使用中划线(划，dash)代替下划线(underscore)
@click.command()
@with_appcontext
def init_db_command():
    """
    1、cli文档：https://click.palletsprojects.com/en/7.x/
    2、函数里面定义命令要做的事
    3、执行命令前要设置 FLASK_APP 和 FLASK_ENV 。
    """
    init_db()
    # 为了用户友好，应该在操作完成后进行提示
    click.echo('初始化数据库完毕')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
