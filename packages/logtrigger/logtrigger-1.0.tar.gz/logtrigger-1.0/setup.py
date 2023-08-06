from setuptools import setup, find_packages

setup(
    name="logtrigger",
    version="1.0",
    author="Alexander.Lee",
    author_email="superpowerlee@gmail.com",
    description="Trigger tasks by monitoring logs",
    install_requires=['sh'],

    # 项目主页
    url="https://github.com/ipconfiger/logtrigger",

    # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
    packages=find_packages(),
    entry_points={
        "console_scripts": ['watch_log=logtrigger.tailer:main']
    }
)
