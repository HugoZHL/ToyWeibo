
CREATE TABLE `user` (
  `uid` varchar(20) collate utf8_unicode_ci NOT NULL,
  `screen_name` varchar(50) collate utf8_unicode_ci NOT NULL,
  `name` varchar(50) collate utf8_unicode_ci NOT NULL,
  `province` int(11) NOT NULL,
  `city` int(11) NOT NULL,
  `location` varchar(20) collate utf8_unicode_ci NOT NULL,
  `url` varchar(80) collate utf8_unicode_ci NOT NULL,
  `gender` varchar(10) collate utf8_unicode_ci NOT NULL,
  `followersnum` int(11) NOT NULL,
  `friendsnum` int(11) NOT NULL,
  `statusesnum` int(11) NOT NULL,
  `favouritesnum` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY  (`uid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

INSERT INTO `user` VALUES ('1', 'Jing_Mini_Shop', 'Jing_Mini_Shop', 61, 1, '陕西 西安', 'http://wd.koudai.com/s/160206134?wfr=dx', 'f', 3860, 228, 507, 0, '2011-10-07 18:54:43');
INSERT INTO `user` VALUES ('2', '百年润发One', '百年润发One', 42, 8, '湖北 荆门', '', 'm', 260, 103, 1326, 0, '2012-08-06 14:44:20');
INSERT INTO `user` VALUES ('3', '互联网的那点事', '互联网的那点事', 400, 1000, '海外', 'http://www.alibuybuy.com', 'f', 1583942, 989, 30643, 331, '2009-08-28 11:55:09');

CREATE TABLE `userrelation` (
  `suid` varchar(20) collate utf8_unicode_ci NOT NULL,
  `tuid` varchar(20) collate utf8_unicode_ci NOT NULL,
  PRIMARY KEY  (`suid`,`tuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

INSERT INTO `userrelation` VALUES ('1', '2');

CREATE TABLE `weibo` (
  `mid` varchar(20) collate utf8_unicode_ci NOT NULL,
  `date` datetime NOT NULL,
  `text` varchar(500) collate utf8_unicode_ci NOT NULL,
  `source` varchar(100) collate utf8_unicode_ci NOT NULL,
  `repostsnum` int(11) NOT NULL,
  `commentsnum` int(11) NOT NULL,
  `attitudesnum` int(11) NOT NULL,
  `uid` varchar(20) collate utf8_unicode_ci NOT NULL,
  `topic` varchar(20) collate utf8_unicode_ci NOT NULL,
  PRIMARY KEY  (`mid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

INSERT INTO `weibo` VALUES ('1', '2014-04-30 15:53:35', '魅族MX3，配件齐全，充电头保护套贴膜支架剪卡器全赠送，代理拿货价¥1760，想当代理的评论留电话，Amy跟你聊聊天', '<a href="http://app.weibo.com/t/feed/9ksdit" rel="nofollow">iPhone客户端</a>', 0, 0, 0, '1', '魅族');
INSERT INTO `weibo` VALUES ('2', '2014-04-30 15:51:19', '我只能这样说，凡是有欣赏能力和懂得区别美丑的人都会选择魅族，从产品的细节和精神上都能看出魅族的用心和诚意，对于我们这些懂手机且懂得欣赏的人，魅族在安卓手机里面没有对手，硬说对手OPPO倒是值得一提，其他则平庸。所以魅族敢于挑战自己。支持魅族！', '<a href="http://app.weibo.com/t/feed/5dtGzh" rel="nofollow">MEIZU MX</a>', 0, 0, 0, '2', '魅族');
INSERT INTO `weibo` VALUES ('3', '2014-04-29 21:40:26', '我发起了一个投票【1799元的魅族MX3和1699元的小米3，你会买哪个？】凡是转发本微博，并投票的，到时间随机抽一位，送得票高的哪款手机！点击投票：http://t.cn/8smABBw', '<a href="http://weibo.com/" rel="nofollow">微博 weibo.com</a>', 10561, 3559, 537, '1', '魅族');
INSERT INTO `weibo` VALUES ('4', '2014-04-30 15:48:06', '真心觉得米3不好看啊 支持魅族', '<a href="http://weibo.com/" rel="nofollow">微博 weibo.com</a>', 0, 0, 0, '1', '魅族');

CREATE TABLE `weiborelation` (
  `smid` varchar(20) collate utf8_unicode_ci NOT NULL,
  `tmid` varchar(20) collate utf8_unicode_ci NOT NULL,
  PRIMARY KEY  (`smid`,`tmid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

INSERT INTO `weiborelation` VALUES ('1', '2');
