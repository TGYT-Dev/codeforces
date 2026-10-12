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
        if inputs[0].lower() == "yes":
            print("YES")
            inputs.pop(0) 
        else:
            print("NO")
            inputs.pop(0)
