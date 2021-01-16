
后端接口说明（编号与我发的长微信对应）：
1. 我在后端代码开头写了gc = GstoreConnector.GstoreConnector('localhost', 9000, 'root', '123456')
2. 注册：register(email, screen_name, password, location, url, gender)
参数都是字符串，返回(True, <uid>)或(False, <error info>)
函数内会判断email和screen_name不重复，会改\和"的转义字符，但是不会判断空字符串。
现有用户属性：
标识符uid是string，可转为int
string属性：email, screen_name, password, location, url, gender, created_at
int属性：followersnum, riendsnum, statusesnum
3. 登陆：login(email, password)
返回(True, <uid>)或(False, 'Wrong email or password')
4. 查看个人信息：user_query_values(uid, keys)
参数keys是list，每个元素是一个属性名（以2为准），返回一个list，每个元素是对应属性值，且必定为字符串格式
5. 修改个人信息：update_info(uid, email, screen_name, location, url, gender)
参数和返回值与2一样。
允许改email和screen_name，也允许不改
5.5. 修改密码：change_password(uid, old_pwd, new_pwd)
返回True或False
要求旧密码正确
6. 查看关注对象的所有微博：latest_weibo(uid)
参数uid是自己的id，返回一个list，每个元素是一条微博的信息，按日期字符串从大到小排序，返回的是关注对象的所有微博
这里返回的信息由weibo_info(wid)函数生成，目前包括wid, uid, text, date
6.5. 查看所有人的微博：all_weibo()
与6类似
7. 查看某个用户的微博：user_weibo(uid)
与6类似，查看的用户可以是自己也可以是别人
7.6. 判断A是否关注B：is_following(uid1, uid2)
返回True或False
8. 发送微博：send_weibo(uid, text)
无返回值
注意不会判断text是否为空字符串
现有微博属性：
标识符wid是string，可转为int。其实应该叫mid。。。
string属性：text, date
int属性：repostsnum, commentsnum
9. 按昵称查找用户：find_user(screen_name)
返回(True, <uid>)或(False, 'User not exist')
11. 查看自己关注的人：followings(uid)
返回uid的list
12. 查看关注自己的人：followers(uid)
返回uid的list
13. 加关注：follow(uid1, uid2)
无返回值，不会判断是否已关注，前端要保证正确性
13.5. 取关：unfollow(uid1, uid2)
与13类似
14. 查询用户联系：routes4(uid1, uid2)
输入双方的uid，返回四条边以内的用户uid路径
比如routes4('1','2')返回[['1','2'], ['1','3','2']]

暂不支持（打算晚点弄或者不弄）：
点赞，转发，评论，收藏（作业没要求）
删除微博（有的论坛不支持用户删帖
推荐n跳邻居的用户（明明是朋友的朋友却没加关注，意思很明显了（笑

前端要注意的事情：
1. gstore的启动？
2. 要做空字符串判断
3. 关注、取关要合法

