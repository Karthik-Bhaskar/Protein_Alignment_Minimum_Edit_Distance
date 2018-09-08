from __future__ import print_function
from __future__ import division
import numpy as np



class DynamicProgrammingAlignment(object):
    """

    """
    def __init__(self, string1, string2):

        self.A = string1
        self.B = string2
        self.pref_matrix = np.empty((len(string1)+1, len(string2)+1),dtype=np.int32)
        self.pref_matrix[0, :] = np.arange(len(string2) + 1)
        self.pref_matrix[:, 0] = np.arange(len(string1) + 1)
        self.edit_distance = None
        self.got_matrix = False
        self.row1 = ""
        self.row2 = ""
        self.row3 = ""


    def compute_matrix(self):
        
#        for i in range(1, len(self.A) + 1):
#            for j in range(1, len(self.B) + 1):
#                delta =  1 if self.A[i - 1] != self.B[j - 1] else 0
#                self.pref_matrix[i, j] = min(
#                                        self.pref_matrix[i - 1, j - 1] + delta,
#                                        self.pref_matrix[i - 1, j] + 1,
#                                        self.pref_matrix[i, j - 1] + 1)


        for i in range(1,len(self.A) + 1):
            for j in range(1,len(self.B) + 1):
                if self.A[i-1] == self.B[j-1]:
                    self.pref_matrix[i,j] = self.pref_matrix[i-1,j-1]
                else:
                    self.pref_matrix[i,j] = min(self.pref_matrix[i,j-1],
                                                self.pref_matrix[i-1,j],
                                                self.pref_matrix[i-1,j-1]) + 1 


        self.edit_distance = self.pref_matrix[len(self.A), len(self.B)].astype(int)
        self.got_matrix = True

        return self.pref_matrix


    def print_alignment(self, i=None, j=None):
        """
        
        """
        if i == None and j == None:
            i = len(self.A) 
            j = len(self.B)


        if not self.got_matrix:
            self.compute_matrix()

        if i > 0 and j > 0:
            delta = self.pref_matrix[i - 1][j - 1]
            delta_symbol = "|"

            if self.A[i - 1] != self.B[j - 1]:
                delta += 1  
                delta_symbol = " "
            
            if self.pref_matrix[i, j] == delta:
                self.row1 = self.A[i - 1] + self.row1
                self.row2 = delta_symbol + self.row2
                self.row3 = self.B[j - 1] + self.row3
                self.print_alignment(i - 1,j - 1)

            elif self.pref_matrix[i, j] == self.pref_matrix[i - 1, j] + 1:

                self.row1 = self.A[i - 1] + self.row1
                self.row2 = " " + self.row2
                self.row3 = "-" + self.row3
                self.print_alignment(i - 1, j)

            else:
                self.row1 = "-" + self.row1
                self.row2 = " " + self.row2
                self.row3 = self.B[j - 1] + self.row3
                self.print_alignment(i, j - 1)

        elif i > 0:
            self.row1 = self.A[i - 1] + self.row1
            self.row2 = " " + self.row2
            self.row3 = "-" + self.row3
            self.print_alignment(i - 1, j)

        elif j > 0:
            self.row1 = "-" + self.row1
            self.row2 = " " + self.row2
            self.row3 = self.B[j - 1] + self.row3
            self.print_alignment(i, j - 1)
        else:
            print("\n", self.row1, "\n", self.row2, "\n", self.row3)

    def get_edit_distance(self, print_distance = False):

        if not self.got_matrix: 
            self.compute_matrix()

        if print_distance:
            print(self.edit_distance)
        else:
            return self.edit_distance   
if __name__ == "__main__": 
    A = "baath"
    B = "aanhg"
    algo = DynamicProgrammingAlignment(A, B)
    algo.get_edit_distance(print_distance = True)
    algo.print_alignment()
