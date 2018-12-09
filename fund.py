# Shinya Aoi
# CSS 340
# 12/8/2018


class Fund:
    def __init__(self, fundId, id, amount):
        if fundId == 0:
            self.__fundName = "Money Market"
        elif fundId == 1:
            self.__fundName = "Prime Money Market"
        elif fundId == 2:
            self.__fundName = "Long-Term Bond"
        elif fundId == 3:
            self.__fundName = "Short-Term Bond"
        elif fundId == 4:
            self.__fundName = "500 Index Fund"
        elif fundId == 5:
            self.__fundName = "Capital Value Fund"
        elif fundId == 6:
            self.__fundName = "Growth Equity Fund"
        elif fundId == 7:
            self.__fundName = "Growth Index Fund"
        elif fundId == 8:
            self.__fundName = "Value Fund"
        elif fundId == 9:
            self.__fundName = "Value Stock Index"
        self.__fundId = id
        self.__amount = amount
        self.__history = []

    def getfundId(self):
        return self.__fundId

    def getAmount(self):
        return self.__amount

    def getFundName(self):
        return self.__fundName

    def getHistory(self):
        return self.__history

    def getHistoryLen(self):
        return len(self.__history)

    def setAmount(self, amount):
        self.__amount = amount

    def deposit(self, amount):
        self.__amount += amount
        return self.__amount

    def withDraw(self, amount):
        self.__amount -= amount
        if self.__amount < 0:
            self.__amount += amount
            return False
        return self.__amount

    def appendHistory(self, history):
        self.__history.append(history)

    def printHistoryInFund(self):
        for history in self.__history:
            print("    " + str(history))

    def __str__(self):
        return str(self.__fundName) + ": $" + str(self.__amount) + " Account id:" + str(self.__fundId)

    def __repr__(self):
        return self.__str__()
