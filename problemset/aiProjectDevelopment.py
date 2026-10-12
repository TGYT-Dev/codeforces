from math import *
tmp = 0
counter = int(input())
inputs= []
tmp = counter

while tmp != 0:
    tmp -= 1
    inputs.append(input().split())

if __name__ == "__main__":
    while counter != 0:
        counter -= 1
        n = int(inputs[0][0])
        x = int(inputs[0][1])
        y = int(inputs[0][2])
        z = int(inputs[0][3])
        totalHoursWithoutAI = ceil(n / (x + y))
        if x * z >= n:
            totalHoursWithAI = ceil(n / x)
        else:
            totalHoursWithAI = z + ceil((n - x * z) / (x + 10 * y))
        print(min(totalHoursWithoutAI, totalHoursWithAI))
        inputs.pop(0)