

with open("lettercombinations.txt", "r") as combinations:
    lines = combinations.readlines()
    comb = []
    for i in lines:
            comb.append(i.strip())
    print(comb)
           
           