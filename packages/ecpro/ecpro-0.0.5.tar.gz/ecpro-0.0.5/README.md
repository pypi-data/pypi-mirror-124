https://packaging.python.org/tutorials/packaging-projects/#

# 制作包

# 打包
python setup.py sdist bdist_wheel

# 上传
twine upload dist/*

# 下载
pip install ecpro -i  https://pypi.python.org/simple/