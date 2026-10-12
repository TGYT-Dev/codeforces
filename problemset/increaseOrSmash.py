tmp = 0
counter = int(input())
inputs= []
tmp = counter

while tmp != 0:
    tmp -= 1
    input() # why tf you get the length???
    inputs.append(input().split())

if __name__ == "__main__":
    while counter != 0:
        counter -= 1
        print((len(set(inputs[0])) * 2) - 1)
        inputs.pop(0)