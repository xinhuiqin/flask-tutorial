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
from flask import redirect
from flask import url_for
from flask import abort

from flaskr.db import get_db
from flaskr.auth import login_require

bp = Blueprint(name='blog', import_name=__name__)


def get_post(post_id, check_author=True):
    """
    1、因为编辑和删除都需要获取文章，为了避免代码重复，所以可以创建一个函数来获取文章。
    2、获取文章的逻辑：
     2.1、因为发布文章后默认都是公开的，所以获取文章一般不用校验用户是否登录。
     2.2、获取的文章的可能不存在，因此需要根据文章 id 进行校验。
    3、Python 有一个内置函数的名称为id，所以这里参数名使用 post_id,既避免了与关键字冲突，同时也更好理解。
    :return: post
    """
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (post_id,)
    ).fetchone()

    # 404 文章没找到
    if post is None:
        abort(404, "文章不存在（id： {0}）。".format(post_id))
    # 403 认证不通过，禁止删除文章
    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


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
            # 提交之后定向到首页
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@bp.route('/<int:post_id>/update', methods=('GET', 'POST'))
@login_require
def update(post_id):
    """
    1、如果是 GET 方法：那么是显示编辑文章的页面;如果是 POST 方法，那么就是提交数据。
    2、
    :param post_id: 文章id,
    :return:
    """
    post = get_post(post_id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if not title:
            error = '文章标题不能为空'
        elif not body:
            error = '内容不能为空'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, post_id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=post)


# 注意：POST——只有一个元素的元组后面必须跟一个逗号，否则被认为是字符串，而不是元组
@bp.route('/<int:post_id>/delete', methods=('POST',))
@login_require
def delete(post_id):
    # 删除文章之前先判断文章是否存在
    get_post(post_id)
    db = get_db()
    db.execute(
        'DELETE FROM post WHERE id = ?', (post_id,)
    )
    db.commit()
    return redirect(url_for(endpoint='blog.index'))
