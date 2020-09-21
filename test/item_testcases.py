import os
import filecmp

def check_diff(file1,file2):
    check = {}
    for file in [file1,file2]:
        with open(file,'r',  encoding = "ISO-8859-1") as f:
            check[file] = []
            for line in f:
                check[file].append(line)
    diff = set(check[file1]) - set(check[file2])
    if diff:
        return(0)
    return(1)

input_arr = ["34","547","650","14 12"]
flag = 0
for i in range(len(input_arr)):
    os.system("python3 Code/item_based.py %s > item_test_output%s.txt" %(input_arr[i],i))
    os.system("cp ../SE21-project/test/item_original_output%s.txt item_original_output%s.txt" %(i,i))
    os.system("cat item_original_output%s.txt" %(i))
    os.system("cat item_test_output%s.txt" %(i))
    file1="item_original_output"+str(i)+".txt"
    file2="item_test_output"+str(i)+".txt"
    comp=check_diff(file1,file2)
    
    if comp:
        print("Test case "+str(i+1)+" passed")
        flag+=1
    else:
        print("Test case "+str(i+1)+" failed")
        
if flag == len(input_arr):      
    print("All Test cases passed")
else:
    print(str(flag)+" out of "+str(len(input_arr))+" Test cases passed")
