from __future__ import print_function
from __future__ import division
import numpy as np
import pandas as pd
from six.moves import cPickle as pickle
lm = pickle.load(open("misc/lm_prot_2.sav", 'rb'))


class K_Strip_Model(object):
    
        
    def __init__(self, string1, string2):
        
        """
        - k: lenght of the strip
        - Dimensions of the infinity matrix using math.inf will depend on the lenghts of
          string1 and string2.
        
        """
        
        self.A_ = string1
        self.B_ = string2
        self.A = ' '+ string1
        self.B = ' '+ string2
        self.min = min(len(self.A),len(self.B))
        self.max = max(len(self.A),len(self.B))
        
        self.pref_matrix = np.ones(shape = (len(self.B),len(self.A)))*float("inf")
        self.pref_matrix_dyna = np.zeros((len(self.B), len(self.A)),dtype=np.int8)
        self.edit_distance = None
        self.got_matrix = False
        self.best = False
        self.row1 = ""
        self.row2 = ""
        self.row3 = ""
        self.dyna = 0
        self.k = 0    
    
    def compute_matrix(self):
        """
        The compute matrix function computes the optimal edit distance for any two given strings
        using the dynamic approach. This distance will be required by the 'best_k' method to
        select a k value so as to arrive at the optimal edit distance. 
        """

        self.pref_matrix_dyna = np.zeros(shape = (len(self.B),len(self.A)))
        self.pref_matrix_dyna[0,:]=range(0,len(self.pref_matrix_dyna[0,:]))
        self.pref_matrix_dyna[:,0]=range(0,len(self.pref_matrix_dyna[:,0]))
    

        for i in range(1,len(self.B)):
            for j in range(1,len(self.A)):
                if self.B[i] == self.A[j]:
                    self.pref_matrix_dyna[i,j] = self.pref_matrix_dyna[i-1,j-1]

                else:
                    self.pref_matrix_dyna[i,j] = min(self.pref_matrix_dyna[i,j-1],self.pref_matrix_dyna[i-1,j],self.pref_matrix_dyna[i-1,j-1]) + 1


        return self.pref_matrix_dyna,self.pref_matrix_dyna[-1][-1] 

        
       
    def k_strip(self):
        
        if self.best == False:
            # If k_strip method is called then k is calculated based on linear model and 
            # cost is displayed 
            test = pd.DataFrame({"Dummy": [1], "Str_len":[self.max]})
            test = test[["Str_len", "Dummy"]]
            self.k = round(float(lm.predict(test)))
            
        
        """
        - In the first case length of string1 is greater than string2. 
        - In the second else case length of string2 is greater than string1.
        - In both the cases j iterates over the columns of the matrix and i iterates over
          the rows of the matrix.
        """

        
        if len(self.A) > len(self.B):  
        
            for j in range(0,len(self.A)):    
                i = (j*self.min)//self.max

                for i in range (max(int(i-self.k),0),min(len(self.B),int(i+self.k+1))):

                    if j == 0 and i == 0:
                        self.pref_matrix[i,j] = 0
                    elif j == 0:
                        self.pref_matrix[i,j] = i
                    elif i == 0:
                        self.pref_matrix[i,j] = j

                    else:
                        if self.B[i] == self.A[j]:
                            self.pref_matrix[i,j] = self.pref_matrix[i-1,j-1]

                        else:
                            self.pref_matrix[i,j] = min(self.pref_matrix[i,j-1],
                                                        self.pref_matrix[i-1,j],
                                                        self.pref_matrix[i-1,j-1]) + 1
        
            
        else:                    
            
                
       
            for i in range(0,len(self.B)):
                j = (i*self.min)//self.max

                for j in range (int(max(j-self.k,0)),min(len(self.A),int(j+self.k+1))):

                    if j == 0 and i == 0:
                        self.pref_matrix[i,j] = 0
                    elif j == 0:
                        self.pref_matrix[i,j] = i
                    elif i == 0:
                        self.pref_matrix[i,j] = j

                    else:
                        if self.B[i] == self.A[j]:
                            self.pref_matrix[i,j] = self.pref_matrix[i-1,j-1]

                        else:
                            self.pref_matrix[i,j] = min(self.pref_matrix[i,j-1],
                                                        self.pref_matrix[i-1,j],
                                                        self.pref_matrix[i-1,j-1]) + 1

            
                 
        self.edit_distance = self.pref_matrix[-1, -1].astype(int)
        self.got_matrix = True
        
        return self.pref_matrix[-1][-1],self.k,self.pref_matrix
                    
      
    
    def best_k(self):
        """
        The K strip algorithm would require the optimal edit distance computed using the 
        dynamic approach to choose a k value that would yeild the same distance
        """
        self.dyna = self.compute_matrix()[1]
        i = -1
        strip = 0
        self.best = True
        while strip != self.dyna:
            i +=1
            self.k = i
            strip,p,y = self.k_strip()
            
        return i


    def print_alignment(self, i=None, j=None):
        """
        
        """
        transpose = np.transpose(self.pref_matrix)
        
        if i == None and j == None:
            i = len(self.A_)
            j = len(self.B_)


        if not self.got_matrix:
            self.k_strip()

        if i > 0 and j > 0:
            delta = transpose[i - 1][j - 1]
            delta_symbol = "|"
            if self.A_[i - 1] != self.B_[j - 1]:
                delta += 1  
                delta_symbol = " "  

            if transpose[i, j] == delta:
                self.row1 = self.A_[i - 1] + self.row1
                self.row2 = delta_symbol + self.row2
                self.row3 = self.B_[j - 1] + self.row3
                self.print_alignment(i - 1,j - 1)

            elif transpose[i, j] == transpose[i - 1, j] + 1:

                self.row1 = self.A_[i - 1] + self.row1
                self.row2 = " " + self.row2
                self.row3 = "-" + self.row3
                self.print_alignment(i - 1, j)

            else:
                self.row1 = "-" + self.row1
                self.row2 = " " + self.row2
                self.row3 = self.B_[j - 1] + self.row3
                self.print_alignment(i, j - 1)

        elif i > 0:
            self.row1 = self.A_[i - 1] + self.row1
            self.row2 = " " + self.row2
            self.row3 = "-" + self.row3
            self.print_alignment(i - 1, j)

        elif j > 0:
            self.row1 = "-" + self.row1
            self.row2 = " " + self.row2
            self.row3 = self.B_[j - 1] + self.row3
            self.print_alignment(i, j - 1)
            
        else:
            print("\n", self.row1, "\n", self.row2, "\n", self.row3)


if __name__ == "__main__": 
    A = "baath"
    B = "aanhg"
    algo = K_Strip_Model(A, B)
    print(algo.k_strip()[0].astype(int))
    algo.print_alignment()