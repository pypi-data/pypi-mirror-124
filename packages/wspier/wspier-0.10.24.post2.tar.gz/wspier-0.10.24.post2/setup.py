from setuptools import setup, find_packages

setup(
    name = "wspier",
    version = "0.10.24-2",
    keywords = ("pip","wspier", "worsoon","log"),
    description = "worsoon 4 python",
    long_description = "time and path tool",
    license = "Mulan PSL v2",

    url = "https://go.worsoon.com/fwlink/?linkid=14",
    author = "worsoon",
    author_email = "airego@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)