

class Weibo(object):
    __slots__ = [
        'username',
        'text',
        'time',
        'repostsum',
        'commentsum',
        'attitudesum',
        'topic',
        'replies',
    ]
    def __init__(self, username, text, time, repostsum, commentsum, attitudesum, topic, replies):
        self.username = username
        self.text = text
        self.time = time
        self.repostsum = repostsum
        self.commentsum = commentsum
        self.attitudesum = attitudesum
        self.topic = topic
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
