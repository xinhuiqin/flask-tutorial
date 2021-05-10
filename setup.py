"""
参考资料：
1、PyPa,Python Packaging User Guide: https://packaging.python.org/
2、setup.py 文件位于项目的根目录
"""
from setuptools import setup, find_packages

# set() 参数说明： PyPa，Packaging and distributing projects：
# https://packaging.python.org/guides/distributing-packages-using-setuptools/
setup(
    name='flaskr',
    version='1.0.0',
    # packages 参数告诉 Python 需要包含哪些包（及包里面的文件）
    # 使用 find_packages() 可以自动寻找这些包，这样就不用一个一个列出来需要包含的包
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
