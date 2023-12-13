

class Endpoint:
    def __init__(self, http_method, url, restcontroller):
        self.http_method = http_method
        self.url = url
        self.restcontroller = restcontroller

    def displayEndpoint(self):
        print("%s - %s - %s" % (self.restcontroller, self.http_method, self.url))

