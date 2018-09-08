from __future__ import print_function
from __future__ import division
import math
import numpy as np

class BranchBound(object):
    
    def __init__(self,string1, string2, g=0):
        
        """
        - g: set to 0, will help keep track of cost per operation
        - bound: sets bound to be length of longest string and keeps updating 
                      as the recursive calls are made
        """

        self.bound = max(len(string1),len(string2)) 
        self.g = g
        
        
    def edit_dist_bb1(self,string1,string2,g=0):
        
        """
        - 
        - 
        
        """

        _op = []
     
        h = abs(len(string1)-len(string2))
        f = h + g


        if len(string1) == 0: 
            if f <= self.bound:
                self.bound = f
                if h:
                    for i in range(0,h):
                        _op.append("Insertion")   

            return f,_op    


        elif len(string2) == 0:
            if f <= self.bound:
                self.bound = f 
                if h:
                    for i in range(0,h):
                        _op.append("Deletion")

            return f,_op      


        else:

            while f < self.bound:   

                delta = 1 if string1[-1] != string2[-1] else 0
                x,_x = self.edit_dist_bb1(string1[:-1], string2[:-1], g + delta)
                y,_y = self.edit_dist_bb1(string1[:-1], string2, g+1)
                z,_z = self.edit_dist_bb1(string1, string2[:-1], g+1)

                o = min(x,y,z)

                if o == x:
                    if string1[-1] == string2[-1]:
                        _x.append("Nothing")
                    else:
                        _x.append("Substitution")
                    return x,_x

                elif o == y:
                    _y.append("Deletion")
                    return y,_y

                elif o == z:
                    _z.append("Insertion")
                    return z,_z



        return f,[""]
    def align(self,s1,s2):
   
        middle = []
        _, op = self.edit_dist_bb1(s1,s2)

        if len(s1) < len(s2):
            
            for i in range(0,len(s2)):
                
                if op[i] == "Insertion":
                    s1 = s1[:i] + '-' + s1[i:]
                    middle.append(" ")
                    
                elif op[i] == "Nothing":
                    middle.append("|")
                   
                elif op[i] == "Substitution":
                    middle.append(" ")
        
        else:

            for i in range(0,len(s1)):
                if  op[i] == "Deletion":
                    s2 = s2[:i] + '-' + s2[i:]
                    middle.append(" ")
                    
                elif op[i] == "Nothing":
                    middle.append("|") 
                    
                elif op[i] == "Substitution":
                    middle.append(" ")
                    
        
        
        print("\n", s1, "\n", ''.join(middle), "\n", s2) 

if __name__  == "__main__":
    A = "baath"
    B = "aanhg"
    algo = BranchBound(A,B)
    algo.align(A,B)    
    
