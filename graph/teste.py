a = [1, 2, 3, 4]

for n in a:
    n = n + 1

for i, n in enumerate(a):
    a[i] = n + 1

for i in range(len(a)):
    a[i] = a[i] + 1

print(a)

