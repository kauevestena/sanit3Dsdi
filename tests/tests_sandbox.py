# import laspy
# import numpy as np

# my_data_xx, my_data_yy = np.meshgrid(np.linspace(-20, 20, 15), np.linspace(-20, 20, 15))
# my_data_zz = my_data_xx ** 2 + 0.25 * my_data_yy ** 2

# my_data = np.hstack((my_data_xx.reshape((-1, 1)), my_data_yy.reshape((-1, 1)), my_data_zz.reshape((-1, 1))))


# las = laspy.create(file_version="1.2", point_format=3)

# # las.header.offsets = np.min(my_data, axis=0)
# # las.header.scales = [0.1, 0.1, 0.1]

# sample_size = len(my_data[:, 0])

# print(len(my_data[:, 0]))
# print(my_data[:, 0])

# classes = np.ones(sample_size)

# classes[:200] = 4
# classes[:100] = 2
# classes[:50] = 3

# # print(np.array(list(map(int,(np.array(list(classes)))))))

# print(np.int_(classes))

# las.x = my_data[:, 0]
# las.y = my_data[:, 1]
# las.z = my_data[:, 2]
# las.classification = classes

# las.write("test_las.las")


# a = {'a':{}}
# a['a']['b'] = []

# a['a']['b'] = [1,2,3]

# print(a)

# import numpy as np


# a = np.array([1,2,3])

# b = [a,a,a]

# print(list(map(list,np.array(b))))

def reverse_order_list(a,b):
    l1 = list(range(-a+1,-b+1))

    return list(map(abs,l1))

print(reverse_order_list(8,4))



