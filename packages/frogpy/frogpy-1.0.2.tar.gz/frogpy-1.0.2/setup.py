# from distutils.core import setup
from setuptools import setup,find_packages


def readme_file():
    with open("README.md", encoding="utf-8") as rf:
        return rf.read()


setup(
    name="frogpy",  # 需要打包的名字
    version="1.0.2",  # The initial release version
    description="frogpy: Implement algorithms and solve equations",
    long_description=readme_file(),
    packages=find_packages(),
    python_requires=">=3.6",
    license="Apache",
    author="Tao Xiang",  # Full name of the author
    url="https://github.com/xiang-tao",
    author_email="xiangtao@smail.xtu.edu.cn"
)
