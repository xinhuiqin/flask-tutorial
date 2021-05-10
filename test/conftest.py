"""
1、测试用到的第三方模块是 pytest, coverage
2、测试固件（test fixture）：
    2.1 定义：A test fixture is an environment used to consistently test some item, device, or piece of software.
    2.2 作用：Test fixtures provide a fixed baseline so that tests execute reliably and produce consistent and repeatable results
"""
import os
import tempfile  # 生成临时文件和目录

import pytest

db_path = os.path.join(os.path.dirname(__file__), 'data.sql')
with open(db_path, 'rb') as f:
    # 因为使用 rb 模式打开文件，f.read() 得到的是 bytes 对象，需要使用 decode()方法转换成 str 对象
    _data_sql = f.read().decode('utf-8')
