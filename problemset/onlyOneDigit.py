tmp = 0
counter = int(input())
inputs= []
tmp = counter

while tmp != 0:
    tmp -= 1
    inputs.append(input())

if __name__ == "__main__":
    while counter != 0:
        counter -= 1
        print(sorted(str(inputs[0]))[0])
        inputs.pop(0)