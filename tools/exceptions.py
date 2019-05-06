# coding: utf8


class OkexRequestsException(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'OkexRequestsException:' + self.message