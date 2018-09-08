from __future__ import print_function, division
import numpy as np


class LinearSpaceAlignment(object):
    """

    """

    def __init__(self, string1, string2):

        self.A  = string1
        self.B = string2
        self.m = len(string1)
        self.n = len(string2)
        self.forward_matrix = np.zeros((2, len(string2) + 1))
        self.backward_matrix = np.zeros((2, len(string2) + 1))
        self.edit_distance = None
        self.row1 = ""
        self.row2 = ""
        self.row3 = ""

    def forward_pass(self, p1, p2, q1, q2):

        self.forward_matrix[0, q1:q2 + 1] = np.arange(0, q2 - q1 + 1)
        penalty = lambda i, j: 1 if self.A[i - 1] != self.B[j - 1] else 0
        for i in range(p1 + 1, p2 + 1):
            if i != p1 + 1:
                self.forward_matrix[0, :] = self.forward_matrix[1, :]
            self.forward_matrix[1, q1] = self.forward_matrix[0, q1] + 1
            for j in range(q1 + 1, q2 + 1):
                self.forward_matrix[1, j] = min(
                    self.forward_matrix[0, j - 1] + penalty(i, j),
                    self.forward_matrix[1, j - 1] + 1,
                    self.forward_matrix[0, j] + 1)

    def backward_pass(self, p1, p2, q1, q2):

        self.backward_matrix[1, q1:q2 + 1] = np.arange(q2, q1 - 1, -1)
        penalty = lambda i, j: 1 if self.A[i] != self.B[j] else 0
        for i in range(p2 - 1, p1 - 1, -1):
            if i != p2 - 1:
                self.backward_matrix[1, :] = self.backward_matrix[0, :]
            self.backward_matrix[0, q2] = self.backward_matrix[1, q2] + 1
            for j in range(q2 - 1, q1 - 1, -1):
                self.backward_matrix[0, j] = min(
                    self.backward_matrix[1, j + 1] + penalty(i, j),
                    self.backward_matrix[1, j] + 1,
                    self.backward_matrix[0, j + 1] + 1)

    def align(self, p1=None, p2=None, q1=None, q2=None):
        """
        p1 : int, starting index of the first string
        p2 : int, ending index of the first string
        q1 : int, starting index of the second string
        q2 : int, ending index of the second string

        At first iteration method shound be called without arguments.
        
        At furher iterations arguments will be applied recursively.

        """
        if p1 == None:
            p1 = 0
            p2 = self.m
            q1 = 0
            q2 = self.n

        if p2 == p1:  # self.A is an empty string

            for i in range(q1, q2):

                self.row1 += "-"
                self.row2 += " "
                self.row3 += self.B[i]

        elif q2 == q1:  # self.B is an empty string

            for i in range(p1, p2):

                self.row1 += self.A[i]
                self.row2 += " "
                self.row3 += "-"

        elif p2 - 1 == p1:  # self.A is a one character and self.B is not empty

            char = self.A[p1]
            idx = q1
            for i in range(q1 + 1, q2):
                if self.B[i] == char:
                    idx = i
            for i in range(q1, q2):
                if i == idx:
                    self.row1 += char
                    if self.B[i] == char:
                        self.row2 += "|"
                    else:
                        self.row2 += " "
                else:
                    self.row1 += "-"
                    self.row2 += " "
                self.row3 += self.B[i]

        else:  # p2>p1+1, self.A has at least 2 chars, divide and conquer self.A

            h_split = np.floor((p1 + p2) / 2).astype(int)
            self.forward_pass(p1, h_split, q1, q2)
            self.backward_pass(h_split, p2, q1, q2)
            middle_vector = np.add(self.forward_matrix[1, q1:q2 + 1],
                                   self.backward_matrix[0, q1:q2 + 1])
            v_split = np.argmin(middle_vector) + q1

            if self.edit_distance is None:
                self.edit_distance = middle_vector[v_split].astype(int)

            self.align(p1, h_split, q1, v_split)
            self.align(h_split, p2, v_split, q2)

    def get_edit_distance(self, print_distance=False):

        if print_distance:
            print(self.edit_distance)

        else:
            return self.edit_distance

    def print_alignment(self):

        print(self.row1)
        print(self.row2)
        print(self.row3)

if __name__ == "__main__": 
    A = "baath"
    B = "aanhg"
    algo = LinearSpaceAlignment(A, B)
    algo.align()
    algo.get_edit_distance(print_distance=True)
    algo.print_alignment()

