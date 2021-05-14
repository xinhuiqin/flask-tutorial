"""
 蓝图：组织一组相关试图及其他代码的方式
 认证蓝图
1、创建蓝图：名字，蓝图的位置，路径
2、注册蓝图：把蓝图注册到应用上（类似于@app.route()）
3、视图函数：注册、登录
"""
import functools

from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import render_template
from flask import session
from flask import g
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

# 这里使用的是绝对导入
from flaskr.db import get_db

# __name__ 一般表示当前模块的名称
bp = Blueprint(name='auth', import_name=__name__, url_prefix='/auth')


# 蓝图的路由
@bp.route(rule='/register', methods=['GET', 'POST'])
def register():
    """
    1、获取请求数据：获取参数的方式取决于前端传数据的方式，这里使用表单进行传递
    2、数据处理：判断数据是否为空，判断用户名是否已经存在，
    :return:
    """
    if request.method == 'POST':
        # request  是 flask.Request 对象
        username = request.form['username']
        password = request.form['password']

        # 如果输入的内容不符合规范，则返回错误信息
        error = None
        # 连接数据库
        db = get_db()

        if not username:
            error = '请输入用户名'
        elif not password:
            error = '请输入用户密码'
        elif db.execute(  # db.execute() 返回 Cursor 对象, 并不是查询结果，所以还需要执行 fetchone() 方法获取查询结果
                'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f'用户名: {{username}}已经被注册'
        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))
        # 如果 error 是 None, 那么就重定向到登录页面，所以不用加 else 了，直接在下面写 flash(error)
        flash(error)
    return render_template('auth/register.html')


@bp.route(rule='/login', methods=['GET', 'POST'])
def login():
    # 如果是 GET 请求，就跳转到登录页面，如果是 POST 请求，就是提交用户名和密码
    if request.method == 'POST':
        # 获取用户名和密码
        username = request.form['username']
        password = request.form['password']
        error = None
        db = get_db()
        # 需要判断用户名和密码是否为空，因为虽然前端界面控制了不能提交，但是还是可以通过其它方式发送请求（比如：postman）。
        if not username:
            error = '请输入用户名'
        elif not password:
            error = '请输入密码'
        else:
            user = db.execute(
                'SELECT * FROM user WHERE username = ? ', username
            ).fetchone()

            if user is None:
                error = '用户名不存在'
            # check_password_hash 返回的值是 True 或者 False
            elif not check_password_hash(user['password'], password):
                error = '密码错误'

        if error is None:
            # session 是一个类字典对象
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        # fetchone() 返回的是 Row Object, 具体参考：https://docs.python.org/3.9/library/sqlite3.html#row-objects
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id=? ', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_require(view):
    # 使用 functools.wraps 是为了保留原函数的一些性质，如 __name__
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for(endpoint='auth.login'))
        return view(**kwargs)

    return wrapped_view

