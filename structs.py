

class Weibo(object):
    __slots__ = [
        'userID',
        'postID',
        'username',
        'text',
        'time',
        'repostsum',
        'commentsum',
        'attitudesum',
        'topic',
        'replies',
        'myself',
        'forwardlist', # 所有转发者的三元信息(userID, username, text)，包括自己；如果有转发，那么Weibo的username是原微博的username，其他的仍是本微博信息。
        'forwardshow', # 转发的时候显示的信息，即所有转发内容的拼合，e.g. "test1：好 // @test2：不好 //"
        'praised',
    ]
    def __init__(self, userID, postID, username, text, time, repostsum, commentsum, attitudesum, topic, forwardlist, forwardshow, replies):
        self.userID = userID
        self.postID = postID
        self.username = username
        self.text = text
        self.time = time
        self.repostsum = repostsum
        self.commentsum = commentsum
        self.attitudesum = attitudesum
        self.topic = topic
        self.forwardlist = forwardlist
        self.forwardshow = forwardshow
        self.replies = replies


class Reply(object):
    __slots__ = [
        'username',
        'text',
        'time',
        'praisesum',
        'target', # target username
    ]
    def __init__(self, username, text, time, praisesum, target):
        self.username = username
        self.text = text
        self.time = time
        self.praisesum = praisesum
        self.target = target
