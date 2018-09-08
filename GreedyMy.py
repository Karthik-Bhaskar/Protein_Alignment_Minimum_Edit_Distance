from __future__ import print_function
from __future__ import division

class Greedy(object):
    
    def __init__(self, string1, string2):
        
        """
        
        """
        
        self.A = string1
        self.B = string2
        self.C = ""

    
    def ed_greedy(self):
        n = len(self.A)
        m = len(self.B)
        op = []  # List to keep operations made during the program #
        i = 0  # iteration #
        d = 0  # number of doing insertion #
        cost = 0  # Cost of each operation #

        if self.A == "":
            for j in range(0, m):
                op.append("Insert")
            cost = m
        elif self.B == "":
            for j in range(0, n):
                op.append("Delete")
            cost = 0
        elif self.A == self.B:
            for j in range(0, m):
                op.append("Nothing")
            cost = 0
        else:
            while i <= (n - 1) and i <= (m - 1):
                if m - i - d > 2:  # We have 2 further available indexes to check #
                    if self.A[i] != self.B[i + d] and self.A[i] != self.B[i+d+1] and self.A[i] != self.B[i+d+2]:  # 1-1-1 #
                        op.append("Substitute") # for position self.A[i+d] with value self.B[i+d]
                        cost += 1
                    elif self.A[i] != self.B[i+d] and self.A[i] != self.B[i+d+1] and self.A[i] == self.B[i+d+2]:  # 1-1-0 #
                        op.append("Substitute") # for position self.A[i+d] with value self.B[i+d]
                        cost += 1
                    elif self.A[i] != self.B[i + d] and self.A[i] == self.B[i+d+1] and self.A[i] != self.B[i+d+2]:  # 1-0-1 #
                        if n + d < m:
                            op.append("Insert") # Insert value self.B[i+d] before self.A[i+d] #
                            op.append("Nothing")
                            cost += 1
                            d += 1
                        else:
                            op.append("Substitute") # for position self.A[i+d] with value self.B[i+d]
                            cost += 1

                    elif self.A[i] != self.B[i + d] and self.A[i] == self.B[i+d+1] and self.A[i] == self.B[i+d+2]: # 1-0-0 #
                        if m - (n + d) >= 2:
                            op.append("Insert") # Insert value self.B[i+d] and self.B[i+1+d] before self.A[i+d] #
                            op.append("Insert")
                            op.append("Nothing")
                            cost += 2
                            d += 2
                        elif m - (n + d) == 1:
                            op.append("Insert") # Insert value self.B[i+d] before self.A[i+d] #
                            op.append("Nothing")
                            cost += 1
                            d += 1
                        else:
                            op.append("Substitute") # for position self.A[i+d] with value self.B[i+d]
                            cost += 1
                    elif self.A[i] == self.B[i + d] and self.A[i] == self.B[i+d+1] and self.A[i] != self.B[i+d+2]: # 0-0-1
                        if m - (n + d) >= 2:
                            op.append("Nothing")
                            op.append("Insert")  # Insert value self.B[i+1+d] and self.B[i+2+d] after self.A[i+d] #
                            op.append("Insert")
                            cost += 2
                            d += 2
                        elif m - (n + d) == 1:
                            op.append("Insert")  # Insert value self.B[i+d] before self.A[i+d] #
                            op.append("Nothing")
                            cost += 1
                            d += 1
                        else:
                            op.append("Nothing") # Identical characters
                    elif self.A[i] == self.B[i+d] and self.A[i] != self.B[i+d+1] and self.A[i] != self.B[i+d+2]:  # 0-1-1 #
                        op.append("Nothing")
                    elif self.A[i] == self.B[i+d] and self.A[i] == self.B[i+d+1] and self.A[i] != self.B[i+d+2]:  # 0-1-0 #
                        op.append("Nothing")
                    elif self.A[i] == self.B[i+d] and self.A[i] == self.B[i+d] and self.A[i] == self.B[i+d]: # 0-0-0 #
                        op.append("Nothing")
                elif m - (i + d) == 2:  # We have 1 further available index to check #
                    if self.A[i] != self.B[i+d] and self.A[i] != self.B[i+d+1]:  # 1-1 #
                        op.append("Substitute")
                        cost += 1
                    elif self.A[i] != self.B[i+d] and self.A[i] == self.B[i+d+1]:  # 1-0 #
                        if n + d < m:
                            op.append("Insert") # Insert value self.B[i+d] before self.A[i+d] #
                            op.append("Nothing")
                            cost += 1
                            d += 1
                        else:
                            op.append("Substitute")
                            cost += 1
                    elif self.A[i] == self.B[i + d] and self.A[i] != self.B[i+d+1]:  # 0-1 #
                        op.append("Nothing")

                    elif self.A[i] == self.B[i + d] and self.A[i] == self.B[i+d+1]:  # 0-0 #
                        op.append("Nothing")

                else:  # We only have current index to check #
                    if self.A[i] != self.B[i + d]:  # 1 #
                        op.append("Substitute")
                        cost += 1
                    else:  # 0 -> self.A[i] = self.B[i+d] #
                        op.append("Nothing")

                i += 1
            if m - (d + n) < 0:
                for j in range(i, (n + d)):
                    op.append("Delete")
                    cost += 1
            elif m - (d + n) > 0:
                for j in range(i, m):
                    op.append("Insert") # Insert remaining characters of self.B into self.A to make them equal #
                    cost += 1

        return cost,op

    def align(self):

        jo = "" 
        op = self.ed_greedy()[1]
        al = []
        

        if len(self.A) < len(self.B):

            for i in range(0,len(self.B)):

                if op[i] == "Insert":
                    self.A = self.A[:i] + '-' + self.A[i:]
                    al.append(" ")

                elif op[i] == "Nothing":
                    al.append("|")

                elif op[i] == "Substitute":
                    al.append(" ")

        else:

            for i in range(0,len(self.A)):

                if  op[i] == "Delete":
                    self.B = self.B[:i] + '-' + self.B[i:]
                    al.append(" ")

                elif op[i] == "Nothing":
                    al.append("|") 

                elif op[i] == "Substitute":
                    al.append(" ")



        print("\n", self.A, "\n", ''.join(al), "\n", self.B)

if __name__ == "__main__": 
    A = "baath"
    B = "aanhg"
    algo = Greedy(A,B)
    print(algo.ed_greedy()[0])
    algo.align()
