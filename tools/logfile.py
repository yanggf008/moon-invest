# coding: utf8
from tools.time_util import get_format_time


class Logfile:
    """
    This is a Logfile class to represent a logfile
    Attribute:
        logfile_name(str): the name of logfile
    Function:
        write_logfile(content):
            Parameter: content(str)
        add the content into the logfile
    """
    def __init__(self, logfile_name):
        """
        the Constructor of Logfile class
        :param logfile_name: the name of the logfile to be edited
        """
        self.logfile_name = logfile_name

    def write_logfile(self, content):
        """
        This function is to add content to logfile, if there is no this file
        a new file will be made
        :param content: the content to be added into the logfile
        :return: None
        """
        with open("../log/" + self.logfile_name, "a") as file:
            file.write(get_format_time() + "|")
            file.write(content)
            file.write("\n")
