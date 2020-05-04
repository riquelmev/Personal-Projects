import requests
import sys
import urllib.request
import re
from bs4 import BeautifulSoup

class WordBST(object):
    def __init__(self):
        self.root = None
        deletereturn = 0
        
    #Inserts a node with specified data if it doesn't already exists
    def insert(self, data):
        if self.root:
            return self.root.insert(data)
        else:
            self.root = Node(data)
            return True

    #Checks if it contains a certain node    
    def find(self, data):
        if self.root:
            return self.root.find(data)
        else:
            return False
    #helper for delete
    def delete(self, target):
        return self.delete1(self.root, target)

    # deletes a given node     
    def delete1(self, node, target):
        if node is None:
            return False
        elif node.data == target:
            if node.right is None and node.left is None:
                node = None
                return True
            elif node.left and node.right is None:
                node.data = node.left.data
                node.count = node.left.count
                return True
            elif node.left is None and node.right:
                node.data = node.right.data
                node.count = node.right.count
                return True
            else:
                tempnode = findLargest(self.root.left)
                node = tempnode
        elif target < node.data:
            return self.delete1(node.left, target)
        else:
            return self.delete1(node.right, target)
        
    #helper for printwords    
    def printwords(self, threshold):
        self.printwords1(self.root, threshold)
        print ("\n")
    # prints all words in tree in alphabetical order
    def printwords1(self,localroot, threshold):
        if localroot is not None:
            self.printwords1(localroot.left, threshold)
            if localroot.count >= threshold:
                print(localroot.data + ": " + str(localroot.count))
            self.printwords1(localroot.right, threshold)
    
    
    
class Node(object):
    def __init__(self,data):
        self.data=data
        self.right = None
        self.left = None
        self.count = 1
    
    #inserts node with specified data
    def insert(self, data):
        if self.data == data:
            self.count += 1
            return False
        elif data < self.data:
            if self.left:
                return self.left.insert(data)
            else:
                self.left = Node(data)
                return True
        else:
            if self.right:
                return self.right.insert(data)
            else:
                self.right = Node(data)
                return True
            
    #returns largest node in subtree
    def findLargest(self,localroot):
        if localroot.right.right is None:
            tempnode = localroot.right
            localroot.right = localroot.right.left
            return tempnode
        else:
            return findLargest(localroot.right)

    #returns smallest node in subtree
    def findSmallest(self,localroot):
        if localroot.left.left is None:
            tempnode = localroot.left
            localroot.left = localroot.left.right
            return tempnode
        else:
            return findSmallest(localroot.left)
    #finds certain node              
    def find(self, data):
        if self.data == data:
            return True
        elif data < self.data and self.left:
            return self.left.find(data)
        elif data > self.data and self.right:
            return self.right.find(data)
        else:
            return False

bst = WordBST()
ignore = WordBST()

with open("ignore.txt","r") as ign:

    lines1 = ign.readlines()
    for lines1 in lines1:
        lines1 = lines1.lower()
        lines1 = lines1.split()
        ignore.insert(lines1[0])
        
link = sys.argv[1]
thresh = int(sys.argv[2])

page = requests.get(link)
soup = BeautifulSoup(page.content, 'html.parser')
with open('webpage.txt', 'w') as filehandle:
    filehandle.writelines("%s\n" % word for word in soup.find_all('p'))
with open("webpage.txt","r") as file:
    lines = file.readlines()
    for lines in lines:
        lines = lines.lower()
        words = lines.split()
        i = 0
        while i < len(words):
            if len(words[i]) > 0:
                cleanString = re.sub('\W+','', words[i])
                if ignore.find(cleanString) is False:
                    bst.insert(cleanString)
            i+=1
bst.printwords(thresh)
    

            
            
            
            
                
        
        
        
    
    
