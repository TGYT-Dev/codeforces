counter = int(input())

while counter != 0: 
    counter -= 1
    tmp = sorted(list(set((map(int, input().split())))), reverse=True)
    if len(tmp) == 3:
        print(tmp[0] - tmp[1])
    else:
        print(0)      
