# 玩具微博，一个小型微博网站

## 运行前准备
* 系统要求：Linux操作系统，如Ubuntu 16.04
* 安装：gStore，Flask

## 使用方法
1. 生成数据：修改sql2rdf/sql2rdf.py代码中的文件路径，将weibodatabase.sql转为gStore可读入的格式。也可直接使用small.nt，它是一个微型数据。
2. 建立数据库：使用第1步生成的数据，在gStore建立名为toyweibo的数据库。
    sudo bin/gbuild toyweibo ../ToyWeibo/sql2rdf/small.nt
3. 启动gStore的ghttp服务，端口9000，加载toyweibo数据库。
    sudo bin/ghttp 9000 toyweibo
4. 命令行输入python3 main.py启动服务器。
5. 打开浏览器，输入
    http://127.0.0.1:5000/
（以启动服务器时显示的地址为准），访问网站。

## 文件结构
* sql2rdf：sql数据、nt数据以及二者转换脚本。
* static：css、js以及图片文件。
* templates：html页面文件。
* backend.py：与gStore的交互。
* GstoreConnector.py：gStore的python API。
* main.py：运行文件。
* router.py：使用flask处理url请求。
* structs.py：定义前后端交互时使用的数据结构。