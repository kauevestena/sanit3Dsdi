import numpy as np

# a = np.array([[[2,3,4,5],[2,3,4,5],[2,3,4,5]],[[2,3,4,5],[2,3,4,5],[2,3,4,5]]])

# print(a)

# print(a)

a = np.array([[1,2,3],[4,5,6],[7,8,9]])

number_of_points = a.shape[0]


for i,point in enumerate(a):
    if (i > 0) and (i < (number_of_points - 1)):
        print(i)