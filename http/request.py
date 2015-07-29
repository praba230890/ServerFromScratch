class Request(object):
    def __init__(self, param):
        param = param.split()
        self.method = param[0]
        self.location = param[1]
        if self.location.endswith('/'):
            self.location += "/index.html"
        self.protocol = param[2]