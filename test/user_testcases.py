#importing the required modules
import os
import filecmp

#defining the variables for test cases 
input_arr = ["34","547","650","14 12"]
flag = 0

#defining the function to compare the output generated to expected output
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

#for loop to go through all the test case variables and generate output files
for i in range(len(input_arr)):
    os.system("python3 Code/user_based.py %s > user_original_output%s.txt" %(input_arr[i],i))
    os.system("python3 Code/user_based_test.py %s > user_test_output%s.txt" %(input_arr[i],i))
    file1="user_original_output"+str(i)+".txt"
    file2="user_test_output"+str(i)+".txt"
    comp=check_diff(file1,file2)
    
    #for every test case passed
    if comp:
        print("Test case "+str(i+1)+" passed")
        flag+=1
    #if a test case fails
    else:
        print("Test case "+str(i+1)+" failed")
        
#print statements for the test cases 
if flag == len(input_arr):      
    print("All Test cases passed")
else:
    print(str(flag)+" out of "+str(len(input_arr))+" Test cases passed")
