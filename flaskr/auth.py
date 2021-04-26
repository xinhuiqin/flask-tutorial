"""
 蓝图：组织一组相关试图及其他代码的方式
1、创建蓝图：名字，蓝图的位置，路径
2、注册蓝图：把蓝图注册到应用上（类似于@app.route()）
3、视图函数：注册、
"""
from flask import Blueprint
from flask import request

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
    # request  是 flask.Request 对象
    username = request.form['username']
    password = request.form['password']
    if not username:
