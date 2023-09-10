import sys, os
os.chdir(sys.path[0])



with open("ascii.txt", "r") as f:
    data = f.readlines()

# with open("test.txt", "a+") as f:
for i in data:
    i=i.strip()
    if i=='0':
        continue
    print(chr(int(i)))
    # f.write(chr(int(i)))