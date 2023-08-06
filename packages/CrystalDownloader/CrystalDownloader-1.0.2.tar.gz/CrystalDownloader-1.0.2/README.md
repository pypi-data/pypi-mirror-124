## 打包流程
### 1. 打包项目
```
python setup.py sdist  
python setup.py sdist bdist_wheel 
```
### 2. 检查
```
twine check dist/*
or
python3 -m twine check dist/*
```
### 3. 上传pypi
```
twine upload dist/* 
or
python3 -m twine upload dist/*
```
### 4. 安装最新版本
```
pip install CrystalDownloader==1.0.1
```

## 描述
将文件分段 于多个线程中同时下载 最终写入指定路径下