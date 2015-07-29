def method(param):
    return Request(param.split())
    
class Request(object):
    def __init__(self, param):
        self.method = param[0]
        self.location = param[1]
        self.protocol = param[2]
        