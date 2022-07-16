# f = open("c:\port.txt", "r")

with open(r"c:\port.txt", 'r') as fp:  # In practice, you’ll use the with statement to close the file automatically.
    x = (len(fp.readlines()))
    print('Total lines:', x)  # 6

with open(r"c:\port.txt", 'r') as fp:
    num_lines = sum(1 for line in fp if line.rstrip())
    print('Total lines:', num_lines)  # 3
