"""
1、测试用到的第三方模块是 pytest, coverage
2、测试固件（test fixture）：
    2.1 定义：A test fixture is an environment used to consistently test some item, device, or piece of software.
    2.2 作用：Test fixtures provide a fixed baseline so that tests execute reliably and produce consistent and repeatable results
"""
# 最先导入 Python 标准库
import os
import tempfile  # 生成临时文件和目录

# 其次导入第三方库
import pytest

# 最后是导入本项目的库

database_path = os.path.join(os.path.dirname(__file__), 'data.sql')
with open(database_path, 'rb') as f:
    # 因为使用 rb 模式打开文件，f.read() 得到的是 bytes 对象，需要使用 decode()方法转换成 str 对象
    _data_sql = f.read().decode('utf-8')


# 在 pytest 里面，固件的技术实现是一个函数
# 编写固件之前，请阅读有关固件的说明文档：https://docs.pytest.org/en/6.2.x/fixture.html
@pytest.fixture
def app():
    """
    通过添加 @pytest.fixture，表明 app() 函数是一个固件
    :return:
    """
    # mkdtemp() 返回结果示例：(3, '/tmp/tmpi1832kj6')——第一个值表示句柄（handle）,第二个值表示文件的绝对路径
    db_fd, db_path = tempfile.mkdtemp()
