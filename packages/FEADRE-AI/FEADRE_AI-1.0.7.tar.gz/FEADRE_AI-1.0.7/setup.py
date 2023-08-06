import setuptools

'''
修改版本号 删除后(删FEADRE_AI.egg-info) 复制
python setup.py sdist       ---生成FEADRE_AI.egg-info
twine upload dist/*   ---打包上传
    用户名 zkbutt  M.123
pip install  -i https://pypi.tuna.tsinghua.edu.cn/simple FEADRE_AI
pip install --upgrade FEADRE_AI
'''
setuptools.setup(
    name="FEADRE_AI",  # Replace with your own username  #自定义封装模块名与文件夹名相同
    version="1.0.7",  # 版本号，下次修改后再提交的话只需要修改当前的版本号就可以了
    author="FEADRE",  # 作者
    author_email="318740003@qq.com",  # 邮箱
    description="My short description for my project.",  # 描述
    long_description='My short description for my project.',  # 描述
    long_description_content_type="text/markdown",  # markdown
    url="https://gitee.com/feadre/feadre-ai.git",  # github地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",  # License
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  # 支持python版本
)
