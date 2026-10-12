tmp = 0
counter = int(input())
inputs= []
tmp = counter

while tmp != 0:
    tmp -= 1
    input() # random bullshit number ion need
    inputs.append([int(x) for x in input().split()])
    
# mins and max ??? // 2 + 1 (basically ceil div)

if __name__ == "__main__":
    while counter != 0:
        counter -= 1
        minV = min(inputs[0])
        maxV = max(inputs[0])
        print((maxV - minV + 1) // 2)
        inputs.pop(0)