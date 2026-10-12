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
        a1 = int(inputs[0][0])
        a2 = int(inputs[0][1])
        b1 = int(inputs[0][2])
        b2 = int(inputs[0][3])
        matchA = (a1 > b1) + (a2 > b2) > (a1 < b1) + (a2 < b2)
        matchB = (a1 > b2) + (a2 > b1) > (a1 < b2) + (a2 < b1)
        print(2 * (matchA + matchB))
        wins = 0
        inputs.pop(0) 