from __future__ import print_function
from __future__ import division




class Recursive(object):
    """docstring for Recursive"""
    def __init__(self):
        pass
         

    def get_edit_distance(self,s1,s2,g=0):
        

        _op = []
        
        if len(s1) == 0: 
            for i in range(0,len(s2)):
                _op.append("Insertion") 
                g += len(s2)    
            return g,_op    
        
        
        elif len(s2) == 0:
            for i in range(0,len(s1)):
                _op.append("Deletion")
                g += len(s1)
     
            return g,_op      
        
        
        else:
            
            while len(s1)!= 0 and len(s2)!= 0:   

                delta = 1 if s1[-1] != s2[-1] else 0
                x,_x = self.get_edit_distance(s1[:-1], s2[:-1], g + delta)
                y,_y = self.get_edit_distance(s1[:-1], s2, g+1)
                z,_z = self.get_edit_distance(s1, s2[:-1], g+1)
                
                o = min(x,y,z)
                
                if o == x:
                    if s1[-1] == s2[-1]:
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
    

    def align(self,s1,s2, op = None):

        middle = []
        _,op = self.get_edit_distance(s1,s2)

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

if __name__ == "__main__": 
    A = "baath"
    B = "aanhg"
    algo = Recursive()
    algo.align(A,B)
    