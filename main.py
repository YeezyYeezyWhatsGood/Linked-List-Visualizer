import linked_list_cycle
from random import randint

# After you get this working add support to removing nth node from a linked list and for reversed linked list
'''
introduction = "Hello! The purpose of this project is to provide an interactive visualization for different linked list algorithms. Enter C for finding a [c]ycle in a linked list, R for [r]eversing a linked list, or D for [d]eleting the nth node from a linked list: "
problem = input(introduction).upper()

while problem != "R" and problem != "C" and problem != "D":
    problem = input("Please enter R, C, or D: ")
'''
problem = "C"
print("This project will let us look at two different approaches to checking if a linked list has a cycle. You can find this on leetcode at https://leetcode.com/problems/linked-list-cycle/\nFirst let's input the linked list")
if problem == "C":
    linked_list_values = input(
        "\nEnter the values of the linked list as a list of integers seperated by spaces, or enter R for a [r]andom list, or enter D for the [d]efault linked list ([3, 2, 0, -4], cycle at index 1): "
    ).upper()
    if linked_list_values == "R":
        linked_list_values = [randint(0, 100) for _ in range(randint(1, 20))]
        cycle_location = randint(-1, len(linked_list_values)-1)
    elif linked_list_values == "D":
        linked_list_values = [3, 2, 0, -4]
        cycle_location = 1
    else:
        linked_list_values = [int(x) for x in linked_list_values.split()]
        cycle_location = int(
            input(
                "\nEnter the location of the cycle as a single integer (if there is no cycle enter -1): "
            ))
    
    algorithm = ""
    while algorithm != "F" and algorithm != "B":
        algorithm = input(
            "\nEnter F to visualize [F]loyd's algorithm or enter B to visualize [B]rent's algorithm: "
        ).upper()
    
    if algorithm == "F":
        print("""CONTROLS:\n 
        ENTER to go to the next step \n
        BACKSPACE to go to the previous step \n
        F to follow the fast pointer\n
        S to follow the slow pointer\n
        A to skip to the beginning of the list \n
        C to skip to where the cycle happens \n
        D to skip to the end of the list \n
        R to restart \n
        ARROWKEYS to move freely around the surface \n
        1, 2, and 3 set the speed to Slow, Medium, and Fast respectively \n
        Note: Make sure you click on the game window first and have fun!
        """)
        linked_list_cycle.run(linked_list_values, cycle_location, linked_list_cycle.floyd)

    if algorithm == "B":
        print("""CONTROLS:\n 
        ENTER to go to the next step \n
        BACKSPACE to go to the previous step \n
        F to follow the [f]ast hare pointer\n
        S to follow the [s]low tortoise pointer\n
        A to skip to the beginning of the list \n
        C to skip to where the cycle happens \n
        D to skip to the end of the list \n
        R to restart \n
        ARROWKEYS to move freely around the space \n
        1, 2, and 3 set the speed to Slow, Medium, and Fast respectively \n
        Note: Make sure you click on the game window first and have fun!
        """)
        linked_list_cycle.run(linked_list_values, cycle_location, linked_list_cycle.brent)
    
    
