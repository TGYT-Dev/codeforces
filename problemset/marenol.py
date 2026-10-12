# pattern?? - idk man im hungry
# odds in b mus match in a and same for even??
# cool sep odd and evens -> sort -> compare?? 

counter =  int(input())

while counter != 0:
    counter -= 1
    input()
    strA = input()
    strB = input()
    strAodd = sorted(strA[1::2])
    strBodd = sorted(strB[1::2])
    strAeven = sorted(strA[::2])
    strBeven = sorted(strB[::2])

    if strAodd == strBodd and strAeven == strBeven:
        print("YES")
    else:    
        print("NO")