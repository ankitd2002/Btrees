# Implementation of B+-tree functionality.

from index import *




##### Helper functions ####
def Notfull(index,key,i):
    index.nodes[i].keys = KeySet((index.nodes[i].keys.keys[0], key))
    j = i
    while(j*3+2 < len(index.nodes)):
        index.nodes[i].pointers = PointerSet((i*3+1,i*3+2,0))
        index.nodes[j*3+2] = KeySet((index.nodes[j*3+2].keys.keys[0], key))
        j = j *3+2
    
    ##handle the pointers
    if(i%3 == 0):
        parent = int((i-3)/3)
        index.nodes[parent].pointers = PointerSet(
            (index.nodes[parent].pointers.pointers[0], index.nodes[parent].pointers.pointers[1],i))
    elif(i%3 ==1):
        parent = int((i-2)/3)
        index.nodes[parent].pointers = PointerSet(
            (index.nodes[parent].pointers.pointers[1],i, index.nodes[parent].pointers.pointers[2]))
    else:
        parent = int((i-1)/3)
        index.nodes[parent].pointers = PointerSet(
            (i,index.nodes[parent].pointers.pointers[1], index.nodes[parent].pointers.pointers[2]))
    return index

           

##Helper function ##
def  Full(index, key, i, list1):

    ##updating the pointers
     if(i%3 == 0):
         parent = int((i-3)/3)
     elif(i%3 ==1):
         parent = int((i-2)/3)
     else:
         parent = int((i-1)/3)

     bool = False

     if(index.nodes[parent].keys.keys[0] == -1 or index.nodes[parent].keys.keys[1] == -1):
         bool = True
    
     if(index.nodes[i].pointers.pointers[0] == 0 or index.nodes[i].pointers.pointers[1] == 0):
         while((i)*3+4 > len(index.nodes) and index.nodes[i].keys.keys != (-1,-1) and bool == False):
              index.nodes.append(Node())
     else:
         while((i+1)*3+4 > len(index.nodes) and index.nodes[i].keys.keys != (-1, -1) and bool == False):
             index.nodes.append(Node())
     if(bool == False):
         if(index.nodes[parent].keys.keys[0] != -1 or index.nodes[parent].keys.keys[1] != -1):
             index.nodes[i].pointers = PointerSet((3*i+1,3*i+2,0))
             index.nodes[3*i+1].pointers = PointerSet((0,0,3*i+2))
     else:
          list2 = []
          if(index.nodes[parent].keys.keys[0]>0):
              list2.append(index.nodes[parent].keys.keys[0])
          if(index.nodes[parent].keys.keys[1]>0):
              list2.append(index.nodes[parent].keys.keys[1])
          if(index.nodes[parent].keys.keys[0]>0):
              list2.append(index.nodes[parent].keys.keys[0])
          if(index.nodes[parent].keys.keys[0]>0):
              list2.append(index.nodes[parent].keys.keys[1])
          list2 = list(dict.fromKeys(list2))
          list2 = sorted(list2)

          new= Index([Node()]*1)
          new.nodes[0] = Node(
              KeySet((new, list2[1])),
              PointerSet((0, 0, 0)))

          newl = Index([Node()]*1)
          newl.nodes[0] = Node(
              KeySet((newl, list2[0])),
              PointerSet((0, 0, 0)))

          newr = Index([Node()]*1)
          newr.nodes[0] = Node(
              KeySet((newr, list2[1])),
              PointerSet((0, 0, 0)))
          
          newr = Index([Node()]*1)
          newr.nodes[0] = Node(
              KeySet((newr, list2[2])),
              PointerSet((0, 0, 0)))

          index.nodes[parent] = new
          index.nodes[parent*3+1] = newl
          index.nodes[parent*3+2] = newr
    
     return index
         

# You should implement all of the static functions declared
# in the ImplementMe class and submit this (and only this!) file.
class ImplementMe:

    

    # Returns a B+-tree obtained by inserting a key into a pre-existing
    # B+-tree index if the key is not already there. If it already exists,
    # the return value is equivalent to the original, input tree.
    #
    # Complexity: Guaranteed to be asymptotically linear in the height of the tree
    # Because the tree is balanced, it is also asymptotically logarithmic in the
    # number of keys that already exist in the index.
    @staticmethod


    def InsertIntoIndex( index, key ):
        i = 0
        list1 = []
        length = len(index.nodes)


        ## if the key is empty
        if(key == -1):
            return index


        ##inserting keys into the empty tree ##
        if(length == 0):
            index = Index([Node()]*1)
            index.nodes[0] = Node(\
                KeySet((key,-1)),\
                PointerSet((0,0,0)))


        ##check to see if there are duplicate keys in tree of height 1##
        if(length ==1):
            if(key in index.nodes[0].keys.keys):
                index = index
        while(i < length):
              
                if(key in index.nodes[0].keys.keys):
                    return index

    
                if(index.nodes[i].pointers.pointers[0] == 0 or index.nodes[i].pointers.pointers[1] == 0): ## checks if the tree is a leaf
                  if(index.nodes[i].keys.keys[0] != -1 or index.nodes[i].keys.keys[1] != -1):   ## check if the node is not full
                      index1 = Notfull(index, key, i)
                      index = index1
                  else:
                       index2 = Full(index,key,i,list1)
                       index = index2
                          
                i = i+1
                        
        return index

    # Returns a boolean that indicates whether a given key
    # is found among the leaves of a B+-tree index.
    #
    # Complexity: Guaranteed not to touch more nodes than the
    # height of the tree
    @staticmethod
    def LookupKeyInIndex( index, key ):
        i = 0
        while (i < len(index.nodes)):
            if(key in index.nodes[i].keys.keys):
                return True
            if (key < index.nodes[i].keys.keys[0]):
                 i = 3*i + 1
            elif(key < index.nodes[i].keys.keys[1]):
                 i = 3*i + 2
            elif(key > index.nodes[i].keys.keys[1]):
                i = 3*i + 3
            else:
                return False
        return False
    

    # Returns a list of keys in a B+-tree index within the half-open
    # interval [lower_bound, upper_bound)
    #
    # Complexity: Guaranteed not to touch more nodes than the height
    # of the tree and the number of leaves overlapping the interval.
    @staticmethod
    def RangeSearchInIndex( index, lower_bound, upper_bound ):
        i = 0
        list1 = []
        while (i < len(index.nodes)):

            flag = False ## this ensures the programme will run of the loop 
            for key in index.nodes[i].keys.keys :
                if(lower_bound <= key < upper_bound):
                   list1.append(key)
                elif(key >= upper_bound):
                    flag = True
               
            if(flag == True and i != 0):
                i = len(index.nodes)

            if(i== 0):
                if (lower_bound <= index.nodes[i].keys.keys[0]):
                    i = 3*i + 1     
                elif(lower_bound > index.nodes[i].keys.keys[0] and lower_bound <= index.nodes[i].keys.keys[1]):
                    i = 3*i +2
                else:
                    i = 3*i+3
            else:    
               i = i+1
            
    
        list1 = list(dict.fromkeys(list1))
        list1 = sorted(list1)
        return list1
