import numpy as np

# index = np.arange(0.1, 1.0, 1.0 / 30)
# print("\n".join(map(str, index)))

x_array = np.random.randint(100, 10000, size = 30) / 100.0
print("\n".join(map(str, x_array)))
print('----------------')

r_array = np.random.randint(5, 50, size = 30) / 100.0
xr_array = x_array * r_array
print("\n".join(map(str, xr_array)))
print('----------------')
print("\n".join(map(str, r_array)))


# rr_array = np.random.randint(, 30, size = 30) / 100.0
# xrr_array = x_array * rr_array
# print("\n".join(map(str, xrr_array)))
# print('----------------')

# print("\n".join(map(str, rr_array)))


# ratio = np.random.randint(3000, 8000, size = 27)
# ratio = ratio / 10000.0
# downsize = my_array * ratio

# print("\n".join(map(str, downsize)))

