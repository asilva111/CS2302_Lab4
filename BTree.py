'''
Created on Wed Mar 15 20:55:43 2019
CS 2302 - Andres Silva
> Teacher: Olac Fuentes
> TAs: Anindita Nath  & Maliheh Zargaran
> Lab #4
> The purpose of this lab is to work with B-trees and understand their structure.
> LAST MODIFIED: MARCH 8th, 2019
'''
# Code to implement a B-tree 
# Programmed by Olac Fuentes
# Last modified February 28, 2019
import math
import random
class BTree(object):
    # Constructor
    def __init__(self,item=[],child=[],isLeaf=True,max_items=5):  
        self.item = item
        self.child = child 
        self.isLeaf = isLeaf
        if max_items <3: #max_items must be odd and greater or equal to 3
            max_items = 3
        if max_items%2 == 0: #max_items must be odd and greater or equal to 3
            max_items +=1
        self.max_items = max_items

def FindChild(T,k):
    # Determines value of c, such that k must be in subtree T.child[c], if k is in the BTree    
    for i in range(len(T.item)):
        if k < T.item[i]:
            return i
    return len(T.item)
             
def InsertInternal(T,i):
    # T cannot be Full
    if T.isLeaf:
        InsertLeaf(T,i)
    else:
        k = FindChild(T,i)   
        if IsFull(T.child[k]):
            m, l, r = Split(T.child[k])
            T.item.insert(k,m) 
            T.child[k] = l
            T.child.insert(k+1,r) 
            k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
            
def Split(T):
    #print('Splitting')
    #PrintNode(T)
    mid = T.max_items//2
    if T.isLeaf:
        leftChild = BTree(T.item[:mid]) 
        rightChild = BTree(T.item[mid+1:]) 
    else:
        leftChild = BTree(T.item[:mid],T.child[:mid+1],T.isLeaf) 
        rightChild = BTree(T.item[mid+1:],T.child[mid+1:],T.isLeaf) 
    return T.item[mid], leftChild,  rightChild   
      
def InsertLeaf(T,i):
    T.item.append(i)  
    T.item.sort()

def IsFull(T):
    return len(T.item) >= T.max_items

def Insert(T,i):
    if not IsFull(T):
        InsertInternal(T,i)
    else:
        m, l, r = Split(T)
        T.item =[m]
        T.child = [l,r]
        T.isLeaf = False
        k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
        
        
def height(T):
    if T.isLeaf:
        return 0
    return 1 + height(T.child[0])
        
        
def Search(T,k):
    # Returns node where k is, or None if k is not in the tree
    if k in T.item:
        return T
    if T.isLeaf:
        return None
    return Search(T.child[FindChild(T,k)],k)
                  
def Print(T):
    # Prints items in tree in ascending order
    if T.isLeaf:
        for t in T.item:
            print(t,end=' ')
    else:
        for i in range(len(T.item)):
            Print(T.child[i])
            print(T.item[i],end=' ')
        Print(T.child[len(T.item)])    
 
def PrintD(T,space):
    # Prints items and structure of B-tree
    if T.isLeaf:
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
    else:
        PrintD(T.child[len(T.item)],space+'   ')  
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
            PrintD(T.child[i],space+'   ')
    
def SearchAndPrint(T,k):
    node = Search(T,k)
    if node is None:
        print(k,'not found')
    else:
        print(k,'found',end=' ')
        print('node contents:',node.item)
 
    
def GetHeight(T):
    if T.isLeaf:
        return 0
    else:
        return 1 + GetHeight(T.child[0])
    
def Min(T,d):
    if d == 0:
        return T.item[0]
    if T == None:
        return
    else:
        return Min(T.child[0],d-1)

def Max(T,d):
    if d == 0:
        return T.item[-1]
    if T == None:
        return
    else:
        return Max(T.child[-1],d-1)

       
  
    
def MaxedNodes(T): 
    c = 0 # Counter of Nodes whose length is equal to the max ammount of elements allowed.
    
    if T is None: #If T is None, return.
        return
    
    if not T.isLeaf and len(T.item) == T.max_items: #Increase counter by one if condition is true.
        c += 1
    
    for i in range(0,len(T.child)): #Traverse entire tree
        c += MaxedNodes(T.child[i])

    return c #Return count.

    
def MaxedLeaves(T): #Do the same as above, but only increase counter when the node is a leaf
    c = 0 # Counter of leaves whose length is equal to the max ammount of elements allowed.
    
    if T is None: #If T is None, return.
        return
    
    if T.isLeaf and len(T.item) == T.max_items: #Increase counter by one if condition is true.
        c += 1
    
    for i in range(0,len(T.child)): #Traverse entire tree
        c += MaxedLeaves(T.child[i])

    return c #Return count.

def Extract(T):  #####NOT FINISHED####
    
    if (len(T.item) < 1 or T.child[0] == None):
        return []
    else:     
#        print(T.child[0].item)
        List = Extract(T.child[0]) + T.item  #Concatenate the left child, the current node, and the right child.
        return List #return glued list.
    
def NodesAtD(T,d): #####NOT FINISHED####
    if T is None:
        return 
    if d == 0:
        return len(T.item)
    elif d > 0:
        return NodesAtD(T.child[0],d-1)  + NodesAtD(T.child[-1],d-1)   
    
def PrintAtD(T,d): #####NOT FINISHED####
    if T is None:
        return 
    if d == 0:
        return print(T.item)
    elif d > 0:
        return NodesAtD(T.child[0],d-1)  + NodesAtD(T.child[-1],d-1) 
    
def DepthOfK(T,k):  #####NOT FINISHED####
    if T is None:
        return -1
    else:
        for i in range(0,len(T.item)): #Compare k to every element of current node.
            if k == T.item[i]:
                return 1
    
    if k > T.item[len(T.item)//2]:
        return 1 + DepthOfK(T.child[-1],k)
    else:
        return 1 + DepthOfK(T.child[0],k)
    
#T = BTree()    
#for i in range(13):
#    Insert(T,random.randint(0,100)) 
#PrintD(T,'') 
##print(GetHeight(T))
#print(Extract(T))

          

#L = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,25,25]
#L = [17,8,12,28,34,4,7,9,11,13,15,16,24,27,30,33,37,40,42,50]

T = BTree()    
#for i in L:
#    Insert(T,i)
    

for i in range(0,33):
    Insert(T,random.randint(0,1000))

PrintD(T,' ')


#print(GetHeight(T))

#print(Min(T,1))
#print(Max(T,1))
#print(Extract(T))
#print(NodesAtD(T,2))
#print(MaxedNodes(T))
#print(MaxedLeaves(T))
print(DepthOfK(T,1))












#def MaxedLeaves(T):
#    c = 0
#   
#    if T.isLeaf and T.item == T.max_items:
#        c += 1
#    
#     elif not T.isLeaf:
#        for i in range(0,len(T.child)):
#           return MaxedLeaves(T.child[i])



























































#def LargestAtDepthD(T,d): # Returns largest item at depth d in b-tree with root T,
## or -infinity if the tree has no items with depth d
#    if d==0:
#        return T.item[-1]
#    if T.isLeaf:
#        return -math.inf
#    else:
#        LargestAtDepthD(T.child[-1], d-1)
    
#def FullNodes(T): # Returns number of nodes in b-tree with root T that are full
#    count = 0
#    if not T.isLeaf:
#        for c in T.child:
#            count += FullNodes(c)
#    if len(T.item) == T.max_items:
#        count += 1
#    return count
        
#def FullNodes(T): # Returns number of nodes in b-tree with root T that are full
#    if T.isLeaf:
#        return 0
#    if len(T.item) == T.max_items:
#        return 1
#    if len(T.item) == T.max_items:
#        return 1 + FullNodes(T.child[len(T.item)])

#def FullNodes(T):
#    if T.isLeaf:
#        return 0
#    if len(T.item) == T.max_items:
#        return 1 + FullNodes(T.child[len(T.item)])
    
#def NumItems(T): # Returns number of items in b-tree with root T
#    if T.isLeaf:
#        return len(T.item)
#    return NumItems(T.child[-1]) + NumItems(T.child[0]) + NumItems(T.child[1])
    
#def NumItems(T): # Returns number of items in b-tree with root T
#    s = 0
#    if T.isLeaf:
#        return (len(T.item))
#    else:
#        s += len(T.item)
#        for i in range(len(T.child)):
#            NumItems(T.child[i])
#        return s

#def NumItems(T): # Returns number of items in b-tree with root T
#    s = 0
#    if T.isLeaf:
#        return (len(T.item))
#    else:
#        for i in range(len(T.child)):
#            s+= NumItems(T.child[i])
#        return s
#
#def FindDepth(T,k): # Returns th depth of item k in b-tree with root T, or -1 if
## k is not in the tree
#    if k in T.item:
#        return 0
#    if T.isLeaf:
#        return -1
#    depth = 0
#    for i in range(len(T.child)):
#        depth+=1
#        return depth + FindDepth(T.child[i], k)
        
#def FindDepth(T, k): # Returns th depth of item k in b-tree with root T, or -1 if
## k is not in the tree
#    if k in T.item:
#        return 0
#    if T.isLeaf:
#        return -1
#    if k>T.item[-1]:
#        FindDepth(T.child[-1],k)
#    else:
#        for i in range(len(T.item)):
#            if k < T.item[i]:
#                FindDepth(T.child[i],k)
        
#def FindDepth(T, k): # Returns th depth of item k in b-tree with root T, or -1 if
## k is not in the tree
#    if k in T.item:
#        return 0
#    if T.isLeaf:
#        return -1
#    if k>T.item[-1]:
#        d = FindDepth(T.child[-1],k)
#    else:
#        for i in range(len(T.item)):
#            if k < T.item[i]:
#                d = FindDepth(T.child[i],k)
#    return d + 1
        
#def FindDepth(T, k): # Returns the depth of item k in b-tree with root T, or -1 if
## k is not in the tree
#    if k in T.item:
#        return 0
#    if T.isLeaf:
#        return -1
#    if k>T.item[-1]:
#        d = FindDepth(T.child[-1],k)
#    else:
#        for i in range(len(T.item)):
#            if k < T.item[i]:
#                d = FindDepth(T.child[i],k)
#    if d == -1:
#        return -1
#    return d + 1
        
#def PrintAtDepthD(T,d): # Prints all items in b-tree with root T that have depth d
#    if d ==0:
#        for t in T.item:
#            print(t,end=' ')
#    if not T.isLeaf:
#        for i in range(len(T.child)):
#            PrintAtDepthD(T.child[i],d-1)
##
##L = [25,30,31,35]
#L = [17,8,12,28,34,4,7,9,11,13,15,16,24,27,30,33,37,40,42,50]
#T = BTree()    
#for i in L:
#    Insert(T,i)
    
    #Print(T)