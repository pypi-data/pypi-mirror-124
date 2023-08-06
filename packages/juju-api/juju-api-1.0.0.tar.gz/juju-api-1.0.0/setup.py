from distutils.core import setup

setup(
    name = 'juju-api', #这是pip项目发布的名称
    version = '1.0.0',#版本号，数值打的会优先被pip执行
    keywords = ['test','learn'],
    description= 'juju学习',
    long_description='Juju学脚手架依赖包',
    license = 'MIT license',

    url= 'https://gitee.com/guoyasoft/juju-api.git',#项目相关文件地址，一般是github
    author = 'juju',
    author_email='jialeiju30@gmail.com',

    data_files = ['tool/random_tool.py'],#开发的代码
    packages = ['juju_tool'],#开放的包
    platforms='python',

    install_requires = [
        'pytest == 6.2.5',
        'requestments == 2.25.1'
    ],#需要的依赖包

)