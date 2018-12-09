# Shinya Aoi
# 12/08/2018
# Lab6

class BinarySearchTree:
    def __init__(self):
        self.__root = None
        self.__size = 0

    def getCount(self):
        return self.__size

    def set(self, value):
        self.__root = Node(value)

    def search(self, key):
        return self.searchNode(self.__root, key)

    def searchNode(self, node, key):
        if node == None:
            return False
        currentNode = node.getKey()
        if currentNode == None:
            return False
        elif key == currentNode:
            return True
        elif key < currentNode:
            return self.searchNode(node.leftChild, key)
        else:
            return self.searchNode(node.rightChild, key)

    def get(self, key):
        currentNode = self.__root
        while currentNode != None:
            if currentNode.getKey() == key:
                return currentNode.getValue()
            elif currentNode.getKey() > key:
                currentNode = currentNode.getLeftChild()
            else:
                currentNode = currentNode.getRightChild()
        return None

    # Overriding the get method
    def __getitem__(self, key):
        return self.get(key)

    def isEmpty(self):
        return self.getCount() == 0

    # putting the value into the key
    def put(self, key, value):
        if self.isEmpty():
            self.__root = Node(key, value)
            self.__size += 1
            return
        currentNode = self.__root
        while currentNode != None:
            if currentNode.getKey() == key:
                currentNode.setValue(value)
                return
            elif currentNode.getKey() > key:
                if currentNode.getLeftChild() == None:
                    newNode = Node(key, value)
                    currentNode.setLeftChild(newNode)
                    break
                else:
                    currentNode = currentNode.getLeftChild()
            else:
                if currentNode.getRightChild() == None:
                    newNode = Node(key, value)
                    currentNode.setRightChild(newNode)
                    break
                else:
                    currentNode = currentNode.getRightChild()
        self.__size += 1

    def __setitem__(self, key, value):
        self.put(key, value)

    def remove(self, key):
        if self.__root == None:
            return None
        if self.__root.getKey() == key:
            self.__size -= 1
            if self.__root.getLeftChild() == None:
                self.__root = self.__root.getRightChild()
                return
            elif self.__root.getRightChild() == None:
                self.__root = self.__root.getLeftChild()
                return
            else:
                replaceNode = self.__getAndRemoveRightSmall(self.__root)
                self.__root.setKey(replaceNode.getKey())
                self.__root.setValue(replaceNode.getValue())
                return
        else:
            currentNode = self.__root
            while currentNode != None:
                if currentNode.getLeftChild() and currentNode.getLeftChild().getKey() == key:
                    foundNode = currentNode.getLeftChild()
                    if foundNode.isLeaf():
                        currentNode.setLeftChild(None)
                    elif foundNode.getLeftChild() == None:
                        currentNode.setLeftChild(foundNode.getRightChild())
                    elif foundNode.getRightChild() == None:
                        currentNode.setLeftChild(foundNode.getLeftChild())
                    else:
                        replaceNode = self.__getAndRemoveRightSmall(foundNode)
                        if replaceNode == None:
                            temp = foundNode.leftChild
                            currentNode.leftChild = foundNode.rightChild
                            currentNode.leftChild.leftChild = temp
                        else:
                            foundNode.setKey(replaceNode.getKey())
                            foundNode.setValue(replaceNode.getValue())
                    self.__size -= 1
                    break
                elif currentNode.getRightChild() and currentNode.getRightChild().getKey() == key:
                    foundNode = currentNode.getRightChild()
                    if foundNode.isLeaf():
                        currentNode.setRightChild(None)
                    elif foundNode.getLeftChild() == None:
                        currentNode.setRightChild(foundNode.getRightChild())
                    elif foundNode.getRightChild() == None:
                        currentNode.setRightChild(foundNode.getLeftChild())
                    else:
                        replaceNode = self.__getAndRemoveRightSmall(foundNode)
                        if replaceNode == None:
                            temp = foundNode.leftChild
                            currentNode.leftChild = foundNode.rightChild
                            currentNode.leftChild.leftChild = temp
                        else:
                            foundNode.setKey(replaceNode.getKey())
                            foundNode.setValue(replaceNode.getValue())
                    self.__size -= 1
                    break
                elif currentNode.getKey() > key:
                    currentNode = currentNode.getLeftChild()
                else:
                    currentNode = currentNode.getRightChild()

    def __getAndRemoveRightSmall(self, node):
        currentNode = node.rightChild
        if currentNode.leftChild == None and currentNode.rightChild != None:
            return None
        while currentNode != None:
            if currentNode.leftChild.leftChild == None:
                   temp = currentNode.leftChild
                   currentNode.leftChild = None
                   return temp
            currentNode = currentNode.leftChild

    def isLeaf(self, node):
        if node.rightChild == None and node.leftChild == None:
            return True
        return False

    def inorderTraversal(self, func):
        self.__inOrderTraversalRec(self.__root, func)

    def __inOrderTraversalRec(self, theNode, func):
        if theNode != None:
            self.__inOrderTraversalRec(theNode.getLeftChild(), func)
            func("Account Number: ", theNode.getKey())
            for i in range(10):
                func(theNode.getValue()[i])
            print()
            self.__inOrderTraversalRec(theNode.getRightChild(), func)

    def __len__(self):
        return self.getCount()

    def __str__(self):
        return str(self.__root) + str(self.__size)


class Node:
    def __init__(self, key, value = None):
        self.__key = key
        self.__value = value
        self.leftChild = None
        self.rightChild = None

    def getLeftChild(self):
        return self.leftChild

    def getRightChild(self):
        return self.rightChild

    def setLeftChild(self, theNode):
        self.leftChild = theNode

    def setRightChild(self, theNode):
        self.rightChild = theNode

    def getValue(self):
        return self.__value

    def setValue(self, value):
        self.__value = value

    def getKey(self):
        return self.__key

    def setKey(self, key):
        self.__key = key

    def isLeaf(self):
        return self.getLeftChild() == None and self.getRightChild() == None

    def __str__(self):
        return str(self.__key) + " " + str(self.__value)

    def __repr__(self):
        return self.__str__()
