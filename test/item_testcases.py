import os
import filecmp

# Comparison between two output file to check their similarity
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

# Different test case parameter in form of input array (these inputs represent user ID)
input_arr = ["34","547","650","14 12"]

# Parameter to monitor which test case failed
flag = 0

# Returns the status of the test case and sumarizes the scenario 
for i in range(len(input_arr)):
    os.system("python3 Code/item_based.py %s > item_original_output%s.txt" %(input_arr[i],i))
    os.system("python3 Code/item_based_test.py %s > item_test_output%s.txt" %(input_arr[i],i))
    file1="item_original_output"+str(i)+".txt"
    file2="item_test_output"+str(i)+".txt"
    comp=check_diff(file1,file2)
    
    # 
    if comp:
        print("Test case "+str(i+1)+" passed")
        flag+=1
    else:
        print("Test case "+str(i+1)+" failed")
        
if flag == len(input_arr):      
    print("All Test cases passed")
else:
    print(str(flag)+" out of "+str(len(input_arr))+" Test cases passed")
