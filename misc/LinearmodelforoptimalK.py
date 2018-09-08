import math
import pandas as pd
import numpy as np
import random, string
from matplotlib import pylab
import pickle

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

len_str = [i for i in range(0,299)] # Lenght of the strings; the strings are of equal length
optimal_k = [] # List for optimal k values 

"""
Below are functions necessary to obtain a list of best k values for generated strings
dia_k_strip : Calculates the cost matrix using the k-strip approach 
dyna_edit   : Calculates the cost matrix using the dynamic approach
best_k      : Calculates value of k to arrive at optimal cost
randomword  : random string generator 
cal_opt_k   : Stores best k values within a list optimal_k 
"""

def dia_k_strip(s1,s2,k): # string s1 is converted to s2
    
    
    s1 = ' ' + s1
    s2 = ' ' + s2
    m = min(len(s1),len(s2))
    n = max(len(s1),len(s2))
    
    if len(s1) > len(s2):       # in this senario j is the outer loop as it iterates over s1
       
        c = np.ones(shape = (len(s2),len(s1)))*math.inf # create infinity matrix
        
        for j in range(0,len(s1)):    
            i = (j*m)//n
                
            for i in range (max(i-k,0),min(len(s2),i+k+1)):
     
                if j == 0 and i == 0:
                    c[i,j] = 0
                elif j == 0:
                    c[i,j] = i
                elif i == 0:
                    c[i,j] = j
                    
                else:
                    if s2[i] == s1[j]:
                        c[i,j] = c[i-1,j-1]
                   
                    else:
                        c[i,j] = min(c[i,j-1],c[i-1,j],c[i-1,j-1]) + 1
                        
                        
    else:                    # in this senario i is the outer loop as it iterates over s2
       
        c = np.ones(shape = (len(s2),len(s1)))*math.inf # create infinity matrix       
       
        for i in range(0,len(s2)):
            j = (i*m)//n
                
            for j in range (max(j-k,0),min(len(s1),j+k+1)):
                
                if j == 0 and i == 0:
                    c[i,j] = 0
                elif j == 0:
                    c[i,j] = i
                elif i == 0:
                    c[i,j] = j
                    
                else:
                    if s2[i] == s1[j]:
                        c[i,j] = c[i-1,j-1]
                   
                    else:
                        c[i,j] = min(c[i,j-1],c[i-1,j],c[i-1,j-1]) + 1
        
                
    return  c,c[-1][-1] 


def dyna_edit(s1,s2):
    
    s1 = ' '+s1
    s2 = ' '+s2
    c = np.zeros(shape = (len(s2),len(s1)))
    c[0,:]=range(0,len(c[0,:]))
    c[:,0]=range(0,len(c[:,0]))
    
    
    for i in range(1,len(s2)):
        for j in range(1,len(s1)):
            if s2[i] == s1[j]:
                c[i,j] = c[i-1,j-1]
                
            else:
                c[i,j] = min(c[i,j-1],c[i-1,j],c[i-1,j-1]) + 1
                

    return c,c[-1][-1] 


def best_k(s1,s2):
 
    x,dyna = dyna_edit(s1,s2)
    i = -1
    strip = 0
    while strip != dyna:
        i +=1
        y,strip = dia_k_strip(s1,s2,i)

    return i,dia_k_strip(s1,s2,i)[1]


def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def cal_opt_k():
    global optimal_k
    for i in range(1,300):
        s1 = randomword(i)
        s2 = randomword(i)
        optimal_k.append(best_k(s1,s2)[0])


cal_opt_k()

# Plotting the k values against string lengths

fig = pylab.gcf()
fig.set_size_inches(18.5,10.5)
pylab.scatter(len_str,optimal_k)
pylab.xlabel("String lengths")
pylab.ylabel("K values")
plt.show()


# In[20]:

# creating a dataframe out of optimal_k, len_str and dummy variable

dummy = [1 for i in range(0,299)] 
Opt_kdf = pd.DataFrame({"K_val":optimal_k,"Str_len": len_str, "Dummy":dummy})


# Creating and storing linear model within instance 'lm'
 
X = Opt_kdf[['Str_len','Dummy']]
y = Opt_kdf['K_val']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=101)
lm = LinearRegression() 
lm.fit(X_train,y_train) 


# Storing the linear model to make predictions within another file
filename = 'lm_prot_2.sav'
pickle.dump(lm, open(filename, 'wb'),protocol=2)

