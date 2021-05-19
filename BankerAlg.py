#Importing necessary libraries
import numpy as np

#Needed functions
# Function that applies the Safety Algorithm
def SafetyCheck(processes, resources, available_vec, need, allocation):
    finish = [0]*processes #finish vector
    finished = [0]         #list of finished processes so far
    work = available_vec   #work vector
    safe_seq = []          #safe sequence
    i = 0                  #loop index
    flag = 1               #Safety flag
    #Check for valid form of matrices
    if not(np.all(np.greater_equal(need, np.zeros((processes, resources))))):
        return None, 0

    while np.sum(finish) < processes:
        for ind in range(processes):
            if(finish[ind] == 0):
                if np.all(np.less_equal(need[ind], work)):
                    work = work + allocation[ind]
                    finish[ind] = 1
                    safe_seq.append(ind)    
        i += 1
        finished.append(np.sum(finish))
        if i == processes:
            if finished[i] == finished[i-1]:
                flag = 0 #mark as unsafe and break
                safe_seq = None
                break
            else:
                i = 0 #continue the loop over the processes

    if flag:
        print("The system is safe =)")
    else:
        print("\nThe system is unsafe!!!")

    return safe_seq, flag

def ResourceRequest(request, process, processes, resources, available, need, allocation):
    if np.all(np.less_equal(request, need[process])):
        if np.all(np.less_equal(request, available)):
            avail_vec = available - request
            allocation[process] = allocation[process] + request
            need[process] = need[process] - request
            #Checking for safety
            safe_seq, safe = SafetyCheck(processes, resources, avail_vec, need, allocation)
            if safe:
                return safe_seq, 1
            else:
                return None, 0
        else:
            return None, 0
    else:
        return None, 0

def int_input(prompt):
    while True:
        try:
            integer = int(input(prompt))
            return integer
        except ValueError as e:
            print("Oops! That isn't a valid integer. Please try again...")

def matrix_input(n, m, prompt):
    while True:
        try:
            print("Enter values of " + prompt + " separated by spaces")
            matrix = list(map(int, input().split()))
            return np.array(matrix).reshape(n, m)
        except ValueError as e:
            print("Oops! You entered numbers in the wrong shape. Please try again...")

on = 'y'
while(on == 'y'):
    #Getting inputs from user
   
    processes = int_input("Enter number of processes\n")
    resources = int_input("Enter number of resources\n")

    available = matrix_input(1, resources, "Available vector")
    print(available)
    print("\n")
    alloc_mat = matrix_input(processes, resources, "Allocation matrix")
    print(alloc_mat)
    print("\n")
    max_mat = matrix_input(processes, resources, "Maximum matrix")
    print(max_mat)
    print("\n")

    #Calculating outputs
    need_mat = np.subtract(max_mat, alloc_mat)
    print("The Need Matrix is\n" + str(need_mat))

    flag = input("Do you want to enquire about safety? (y/n)")
    options = ["y", "n", "Y", "N"]
    while flag not in options:
        print("Please type 'y' for yes or 'n' for no")
        flag = input() 

    if flag == "y" or flag == "Y":
        safe_seq, safe = SafetyCheck(processes, resources, available, need_mat, alloc_mat)
        if safe:
            safe_enquiry = input("Do you want to see the safe sequence? (y/n)")
            if safe_enquiry == "y" or safe_enquiry == "Y":
                print("\nThe safe sequence is:\n")
                for i in range(processes): print("P" + str(safe_seq[i]) + " ")

    flag = input("Do you want to be granted a request? (y/n)")
    while flag not in options:
        print("Please type 'y' for yes or 'n' for no")
        flag = input() 

    if flag == "y" or flag == "Y":
        process_req = int_input("Process number?\n")
        request = matrix_input(1, resources, "request")
        safe_sq, safe = ResourceRequest(request, process_req, processes, resources, available, need_mat, alloc_mat)
        if safe:
            print("\nYour request can be granted\n")
            safe_enquiry = input("Do you want to see the safe sequence? (y/n)")
            if safe_enquiry == "y" or safe_enquiry == "Y":
                for i in range(processes): print("P" + str(safe_seq[i]) + " ")
        else:
            print("\nYour request cannot be granted")

    on = input("Do you want to start all over? (y/n)")
    while on not in options:
        print("Please type 'y' for yes or 'n' for no")
        on = input() 
        #0 1 0 2 0 0 3 0 2 2 1 1 0 0 2   
        #7 5 3 3 2 2 9 0 2 2 2 2 4 3 3 

#2 3 1 1 0 1 0 0 2 0 0 3 1 1 0 1 2 0 0 1 0 2 1 0 0 1 1 0 0 0 2 0 1 1 0    
#2 3 1 1 0 3 2 1 2 3 0 1 2 3 0 5 4 2 1 0 1 4 4 0 0 3 2 0 5 0 2 6 1 1 0    