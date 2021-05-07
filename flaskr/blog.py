"""
博客蓝图
说明：因为博客是最主要的特性，所以 url 应该设置在 / 下
1、创建蓝图：名字，蓝图的位置，路径
2、注册蓝图：把蓝图注册到应用上（类似于@app.route()）
3、视图函数：首页，发表文章页面，编辑文章页面，
"""
import datetime

from flask import Blueprint
from flask import Request
from flask import render_template
from flask import g
from flask import request
from flask import flash

from flaskr.db import get_db
from flaskr.auth import login_require

bp = Blueprint(name='blog', import_name=__name__)


@bp.route('/')
def index():
    db = get_db()
    # fetchall()方法返回的是一个 list 对象
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=['GET', 'POST'])
@login_require
def create():
    """
    1.非空校验
    :return:
    """
    if request.method == 'POST':
        # 获取参数
        author_id = g.user['id']
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = '文章标题不能为空'
        elif not body:
            error = '内容不能为空'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            # 因为 created 字段是数据库自动调用 CURRENT_TIMESTAMP，所以直接不用填写
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)', (title, body, author_id)
            )
            # 更新数据之后需要提交
            db.commit()

    return render_template('blog/create.html')
