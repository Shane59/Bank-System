# Shinya Aoi
# CSS 340
# 12/08/2018

import queue
import trees
import client

clients = trees.BinarySearchTree()
transactions = queue.Queue()


# This is a bank class to make an object of a bank.
# The constructor reads a file of transactions and put them into the queue.
class Bank:
    def __init__(self, file):
        bank = open(file, "r")
        line = bank.readline().strip()
        while line != "":
            parts = line.split()
            transactions.put(parts)
            line = bank.readline().strip()
        bank.close()

    def executeTransactions(self):
        while 0 < transactions.qsize():
            myList = transactions.get(0)
            action = myList[0]
            # This is to create an account and put it into the BST.
            if action == "O":
                last = myList[1]
                first = myList[2]
                accountNum = int(myList[3])
                if clients.search(accountNum):
                    print("Error: Account " + str(accountNum) + " is already exist. Transaction Failed.")
                else:
                    newClient = client.ClientAccount(first, last, accountNum)
                    clients.put(accountNum, newClient.getFunds())
            # This is to deposit money into a fund.
            elif action == "D":
                accountNum = int(myList[1][0:4])
                fund = int(myList[1][4:])
                amount = int(myList[2])
                if clients.search(accountNum):
                    c = clients.get(accountNum)
                    c[fund].deposit(amount)
                    history = Transaction("D", accountNum, amount, True)
                    c[fund].appendHistory(history)
                else:
                    # when there is no such account
                    print("Error: Account " + str(accountNum) + " was not found!")
            # This is to withdraw money from a fund.
            elif action == "W":
                accountNum = int(myList[1][0:4])
                fund = int(myList[1][4:])
                amount = int(myList[2])
                c = clients.get(accountNum)
                if c == None:
                    print("Error: Account " + str(accountNum) + " was not found!")
                # Checking from other funds
                else:
                    if c[fund].withDraw(amount) == False:
                        amountInTheFund = c[fund].getAmount()
                        dif = amount - amountInTheFund
                        c[fund].withDraw(amountInTheFund)
                        if fund == 0:
                            # Check fund 1
                            if c[1].withDraw(dif) == False:
                                print("Error: Not enough fund to withdraw $" + str(amount) + " from " +
                                      first + " " + last + " " + c[0].getFundName())
                                history = Transaction("W", accountNum, amount, False)
                                c[fund].appendHistory(history)
                                # Put the money back into the fund
                                c[fund].deposit(amountInTheFund)
                            # Success
                            else:
                                history = Transaction("W", accountNum, amountInTheFund, True)
                                history2 = Transaction("W", accountNum, dif, True)
                                c[fund].appendHistory(history)
                                c[1].appendHistory(history2)
                            # When the fund is 1
                        elif fund == 1:
                            # Check the fund 0
                            if c[0].withDraw(dif) == False:
                                print("Error: Not enough fund to withdraw $" + str(amount) + " from " +
                                      first + " " + last + " " + c[1].getFundName())
                                history = Transaction("W", accountNum, amount, False)
                                c[fund].appendHistory(history)
                                c[fund].deposit(amountInTheFund)
                            # Success
                            else:
                                history = Transaction("W", accountNum, amountInTheFund, True)
                                history2 = Transaction("W", accountNum, dif, True)
                                c[fund].appendHistory(history)
                                c[0].appendHistory(history2)
                        # When the fund is 2
                        elif fund == 2:
                            if c[3].withDraw(dif) == False:
                                print("Error: Not enough fund to withdraw $" + str(amount) + " from " +
                                      first + " " + last + " " + c[2].getFundName())
                                history = Transaction("W", accountNum, amount, False)
                                c[fund].appendHistory(history)
                                c[fund].deposit(amountInTheFund)
                            # Success
                            else:
                                history = Transaction("W", accountNum, amountInTheFund, True)
                                history2 = Transaction("W", accountNum, dif, True)
                                c[fund].appendHistory(history)
                                c[3].appendHistory(history2)
                        elif fund == 3:
                            if c[2].withDraw(dif) == False:
                                print("Error: Not enough fund to withdraw $" + str(amount) + " from " +
                                      first + " " + last + " " + c[3].getFundName())
                                history = Transaction("W", accountNum, amount, False)
                                c[fund].appendHistory(history)
                                c[fund].deposit(amountInTheFund)
                            else:
                                history = Transaction("W", accountNum, amountInTheFund, True)
                                history2 = Transaction("W", accountNum, dif, True)
                                c[fund].appendHistory(history)
                                c[2].appendHistory(history2)
                        else:
                            print("Error: Not enough fund to withdraw $" + str(amount) + " from " +
                                  first + " " + last + " " + c[fund].getFundName())
                            history = Transaction("W", accountNum, amount, False)
                            c[fund].appendHistory(history)
                            c[fund].deposit(amountInTheFund)
                    # Success without any issue
                    else:
                        history = Transaction("W", accountNum, amount, True)
                        c[fund].appendHistory(history)

            # This is to transfer money into a fund from the same account or a different account.
            elif action == "T":
                transferFrom = int(myList[1][0:4])
                fundTrasferFrom = int(myList[1][4:])
                amount = int(myList[2])
                transferTo = int(myList[3][0:4])
                fundTrasferTo = int(myList[3][4:])
                # change it to small O(n)
                cTransferFrom = clients.get(transferFrom)
                cTransferTo = clients.get(transferTo)
                if cTransferFrom is not None and cTransferTo is not None:
                    if not cTransferFrom[fundTrasferFrom].withDraw(amount):
                        amountInTheFund = cTransferFrom[fundTrasferFrom].getAmount()
                        dif = amount - amountInTheFund
                        cTransferFrom[fundTrasferFrom].withDraw(amountInTheFund)
                        if fundTrasferFrom == 0:
                            # Check fund 1
                            if cTransferFrom[1].withDraw(dif) == False:
                                print("Error: Not enough fund to withdraw $" + str(amount) + " from " +
                                      first + " " + last + " " + c[0].getFundName())
                                history = Transaction("W", transferFrom, amount, False)
                                cTransferFrom[fundTrasferFrom].appendHistory(history)
                                cTransferFrom[fundTrasferFrom].deposit(amountInTheFund)
                            # Success
                            else:
                                cTransferTo[fundTrasferTo].deposit(amount)
                                history = Transaction("T", transferFrom, amountInTheFund, True)
                                history2 = Transaction("T", transferFrom, dif, True)
                                historyTo = Transaction("T", transferTo, amount, True)
                                cTransferFrom[fundTrasferFrom].appendHistory(history)
                                historyTo = Transaction("T", transferTo, amount, True)
                                cTransferTo[fundTrasferTo].appendHistory(historyTo)
                                cTransferFrom[1].appendHistory(history2)
                            # When the fund is 1
                        elif fundTrasferFrom == 1:
                            # Check the fund 0
                            if cTransferFrom[0].withDraw(dif) == False:
                                #print("Your fund is not sufficient!")
                                print("Error: Not enough fund to withdraw $" + str(amount) + " from " +
                                      first + " " + last + " " + c[1].getFundName())
                                history = Transaction("W", transferFrom, amount, False)
                                cTransferFrom[fundTrasferFrom].appendHistory(history)
                                cTransferFrom[fundTrasferFrom].deposit(amountInTheFund)
                            # Success
                            else:
                                cTransferTo[fundTrasferTo].deposit(amount)
                                history = Transaction("W", transferFrom, amountInTheFund, True)
                                history2 = Transaction("W", transferFrom, dif, True)
                                cTransferFrom[fundTrasferFrom].appendHistory(history)
                                cTransferFrom[1].appecdHistory(history2)
                                historyTo = Transaction("T", transferTo, amount, True)
                                cTransferTo[fundTrasferTo].appendHistory(historyTo)
                        # When the fund is 2
                        elif fundTrasferFrom == 2:
                            if c[3].withDraw(amount) == False:
                                print("Error: Not enough fund to withdraw $" + str(amount) + " from " +
                                      first + " " + last + " " + c[2].getFundName())
                                history = Transaction("W", transferFrom, amount, False)
                                cTransferFrom[fundTrasferFrom].appendHistory(history)
                                cTransferFrom[fundTrasferFrom].deposit(amountInTheFund)
                            # Success
                            else:
                                cTransferTo[fundTrasferTo].deposit(amount)
                                history = Transaction("W", transferFrom, amountInTheFund, True)
                                history2 = Transaction("W", transferFrom, dif, True)
                                cTransferFrom[fundTrasferFrom].appendHistory(history)
                                cTransferFrom[3].appendHistory(history2)
                                historyTo = Transaction("T", transferTo, amount, True)
                                cTransferTo[fundTrasferTo].appendHistory(historyTo)
                        elif fundTrasferFrom == 3:
                            if c[2].withDraw(amount) == False:
                                print("Error: Not enough fund to withdraw $" + str(amount) + " from " +
                                      first + " " + last + " " + c[3].getFundName())
                                history = Transaction("W", transferFrom, amount, False)
                                cTransferFrom[fundTrasferFrom].appendHistory(history)
                                cTransferFrom[fundTrasferFrom].deposit(amountInTheFund)
                            else:
                                cTransferTo[fundTrasferTo].deposit(amount)
                                history = Transaction("W", transferFrom, amountInTheFund, True)
                                history2 = Transaction("W", transferFrom, dif, True)
                                cTransferFrom[fundTrasferFrom].appendHistory(history)
                                cTransferFrom[2].appendHistory(history2)
                                historyTo = Transaction("T", transferTo, amount, True)
                                cTransferTo[fundTrasferTo].appendHistory(historyTo)
                        else:
                            print("Error: Not enough fund to withdraw $" + str(amount) + " from " +
                                  first + " " + last + " " + c[fundTrasferFrom].getFundName())
                            history = Transaction("W", transferFrom, amount, False)
                            cTransferFrom[fundTrasferFrom].appendHistory(history)
                            cTransferFrom[fundTrasferFrom].deposit(amountInTheFund)
                    else:
                        cTransferTo[fundTrasferTo].deposit(amount)
                        historyFrom = Transaction("T", transferFrom, amount, True)
                        historyTo = Transaction("T", transferTo, amount, True)
                        # Adding histories in each fund
                        cTransferFrom[fundTrasferFrom].appendHistory(historyFrom)
                        cTransferTo[fundTrasferTo].appendHistory(historyTo)
                elif transferFrom == None:
                    print("Error: Account " + str(transferFrom) + " was not found!")
                else:
                    print("Error: Account " + str(transferTo) + " was not found!")

            elif action == "H":
                if len(myList[1]) == 4:
                    # print all the history in the account
                    accountNum = int(myList[1])
                    c = clients.get(accountNum)
                    if c != None:
                        print()
                        print("Transaction history for " + first + " " + last + ":")
                        for i in range(10):
                            if c[i].getHistoryLen() != 0:
                                print(c[i].getFundName() + ": $" + str(c[i].getAmount()))
                                c[i].printHistoryInFund()
                    else:
                        print("Account " + str(accountNum) + " was not found!")
                else:
                    # print history just in the specific fund
                    accountNum = int(myList[1][:4])
                    fund = int(myList[1][4:])
                    c = clients.get(accountNum)
                    if c != None:
                        print()
                        print("Transaction history for " + first + " " + last + " " + c[fund].getFundName() +
                              ": $" + str(c[fund].getAmount()))
                        c[fund].printHistoryInFund()
                    else:
                        print("Account " + str(accountNum) + " was not found!")
        return True

    def printAllAccount(self):
        return clients.inorderTraversal(print)

    def __str__(self):
        return

    def __repr__(self):
        return self.__str__()


# This is a transaction class to hold an object of a transaction record
class Transaction:
    def __init__(self, transactionType, accountNum, amount, success):
        self.__transactionType = transactionType
        self.__accountNum = accountNum
        self.__amount = amount
        self.__success = success

    def getTransactionType(self):
        return self.__transactionType

    def getAccountNum(self):
        return self.__accountNum

    def getAmount(self):
        return self.__amount

    def getSuccess(self):
        return self.__success

    def __str__(self):
        return str(self.__transactionType) + " " + \
               str(self.__accountNum)+ " $"+ str(self.__amount)+ " "+ str(self.__success)

    def __repr__(self):
        return str(self.__transactionType) + " " + \
               str(self.__accountNum) + " $" + str(self.__amount) + " " + str(self.__success)
