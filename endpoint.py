

class Endpoint:
    def __init__(self, http_method, url, rest_controller):
        self.http_method = http_method
        self.url = url
        self.rest_controller = rest_controller

    def display_endpoint(self):
        print("%s - %s - %s" % (self.rest_controller, self.http_method, self.url))

