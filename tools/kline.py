# coding:utf8


class Kline:
    """
        K line class represent a real kline

        Attributes:
            period(str): the period of the kline
            high(float): the highest price of the kline
            low(float): the lowest price of the kline
            open(float): the open price of the kline
            close(float): the close price of the kline
    """
    def __init__(self, period, high, low, open, close, time):
        """
            The constructor of Kline class
        :param period: the period of the kline (1day, 5min, 15min, 30min)
        :param high: the highest price of the kline
        :param low: the lowest price of the kline
        :param open: the open price of the kline
        :param close: the close price of the kline
        :param time: the timestamp of the beginning of the kline
        """
        self.period = period
        self.high = float(high)
        self.low = float(low)
        self.open = float(open)
        self.close = float(close)
        self.time = time

    def display(self):
        """
        the function to display the important attributes of the kline
        :return: None
        """
        print("Period: ", self.period, ", Low:", self.low,
              ", High:", self.high, "Open:", self.open, "Close:", self.close)

    def valid(self):
        """
        The function to check whether this kline is valid
        :return: True or False
        """
        if self.low > self.high:
            return False
        else:
            return True

    def __str__(self):
        """
        This is a built-in function to implement str()
        :return: a String to represent this kline
        """
        return "Period: " + self.period + ", Low:" + str(self.low) + ", High:" + str(self.high) + \
               ",Open:" + str(self.open) + ",Close:" + str(self.close) + ",Time:" + str(self.time)



