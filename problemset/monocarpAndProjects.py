# i = k
# total for ALL months
# Range()??

tmp = 0
counter = int(input())
inputs= []
tmp = counter

while tmp != 0:
    tmp -= 1
    inputs.append(list(map(int, input().split()))) # W/o list() it gets fucky???

if __name__ == "__main__":
    while counter != 0:
        counter -= 1
        employees = inputs[0][0]
        projects = inputs[0][1]
        monocarp = 0
        for month in range(inputs[0][2]):
            monocarp += (projects + month) % (employees + month)
        inputs.pop(0)    
        print(monocarp)
        