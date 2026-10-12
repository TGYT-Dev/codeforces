for x in range(int(input())):
    inputs = list(map(int, list(input().split())))
    if inputs[1] <= inputs[0] and (inputs[0] - inputs[1]) % 2 == 0:
        print(inputs[0])
    elif inputs[1] <= inputs[0] + 1 and ((inputs[0] + 1) - inputs[1]) % 2 == 0:
        print(inputs[0] + 1)
    else:
        print("-1")
