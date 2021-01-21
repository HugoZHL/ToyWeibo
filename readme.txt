系统要求：
Linux操作系统，如Ubuntu 16.04

运行前准备：
安装gStore
安装Flask（pip3 install flask）

运行方法：
1. 生成数据：修改sql2rdf/sql2rdf.py代码中的文件路径，将weibodatabase.sql转为gStore可读入的格式。也可直接使用small.nt，它是一个微型数据。
2. 建立数据库：使用第1步生成的数据，在gStore建立名为toyweibo的数据库。
    sudo bin/gbuild toyweibo ../ToyWeibo/sql2rdf/small.nt
3. 启动gStore的ghttp服务，端口9000，加载toyweibo数据库。
    sudo bin/ghttp 9000 toyweibo
4. 命令行输入python3 main.py启动服务器。
5. 打开浏览器，输入http://127.0.0.1:5000/（以启动服务器时显示的地址为准），访问网站。
