# Shinya Aoi
# CSS 340
# 12/08/2018

import fund


class ClientAccount:
    def __init__(self, first, last, accountNum):
        self.__first = first
        self.__last = last
        self.__accountNum = accountNum
        self.__funds = []
        for i in range(10):
            self.__funds.append(fund.Fund(i, accountNum, 0))

    def getFirst(self):
        return self.__first

    def getLast(self):
        return self.__last

    def getAmount(self, fund):
        return self.__funds[fund]

    def getFunds(self):
        return self.__funds

    def getAccountNum(self):
        return self.__accountNum

    def setAmount(self, fund, amount):
        self.__funds[fund] = amount

    def __str__(self):
        return self.__first + self.__last + self.__accountNum

    def __repr__(self):
        return self.__str__()