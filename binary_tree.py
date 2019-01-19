class Node:
    def __init__(self, key, content):
        self.key = key
        self.val = content
        self.leftChild = None
        self.rightChild = None

    def getChildren(self):
        children = []
        if(self.leftChild != None):
            children.append(self.leftChild)
        if(self.rightChild != None):
            children.append(self.rightChild)
        return children

class BST:
    def __init__(self):
        self.root = None

    def setRoot(self, pair):
        key, content = pair
        self.root = Node(key, content)

    def insert(self, pair):

        if(self.root is None):
            self.setRoot(pair)
        else:
            self.insertNode(self.root, pair)

    def insertNode(self, currentNode, pair):

        key, cnt = pair

        if(key <= currentNode.key):
            if(currentNode.leftChild):
                self.insertNode(currentNode.leftChild, pair)
            else:
                currentNode.leftChild = Node(key, cnt)

        elif(key > currentNode.key):
            if(currentNode.rightChild):
                self.insertNode(currentNode.rightChild, pair)
            else:
                currentNode.rightChild = Node(key, cnt)

    def find(self, key):
        return self.findNode(self.root, key)

    def findNode(self, currentNode, key):

        if(currentNode is None):
            assert(False)

        elif(key == currentNode.key):
            return currentNode.val

        elif(key < currentNode.key):
            return self.findNode(currentNode.leftChild, key)

        else:
            return self.findNode(currentNode.rightChild, key)

# class CmpBST:
#
#     # cmp is the <
#     def __init__(self, cmp):
#         self.root = None
#         self.cmp = cmp
#
#     def setRoot(self, val):
#         self.root = Node(val)
#
#     def insert(self, val):
#         if(self.root is None):
#             self.setRoot(val)
#         else:
#             self.insertNode(self.root, val)
#
#     def insertNode(self, currentNode, val):
#
#         if(self.cmp(val, currentNode.val) or val == currentNode.val):
#             if(currentNode.leftChild):
#                 self.insertNode(currentNode.leftChild, val)
#             else:
#                 currentNode.leftChild = Node(val)
#         else:
#             if(currentNode.rightChild):
#                 self.insertNode(currentNode.rightChild, val)
#             else:
#                 currentNode.rightChild = Node(val)
#
#     def find(self, val):
#         return self.findNode(self.root, val)
#
#     def findNode(self, currentNode, val):
#         if(currentNode is None):
#             return False
#         elif(val == currentNode.val):
#             return True
#         elif(self.cmp(val, currentNode.val)):
#             return self.findNode(currentNode.leftChild, val)
#         else:
# return self.findNode(currentNode.rightChild, val)
