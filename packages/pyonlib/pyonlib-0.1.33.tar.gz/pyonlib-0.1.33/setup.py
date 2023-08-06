from setuptools import find_packages,setup
from xes import version
setup(
    name = 'pyonlib',
    version = version.version,
    author = 'Ruoyu Wang',
    description = '解析pyon文件，即保存一个python词典的文件，和json类似。',
    packages = find_packages(),
    install_requires = ["xes-lib",],
    url = 'https://code.xueersi.com'
)