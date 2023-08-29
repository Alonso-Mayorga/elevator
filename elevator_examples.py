# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 21:47:57 2023

@author: galgo
"""

# Example usage of the classes and methods of elevator
# Copy and paste as needed

# Create a few example persons
person1 = Person("Alice", 60)
person2 = Person("Bob", 70)
person3 = Person("Carol", 50)

# Create floors with people
floor1 = Floor(1, [person1, person2])
floor2 = Floor(2, [person3])

# Create a building with floors
building = [floor1, floor2]

# Create an elevator with capacity 150 and starting at floor 0
elevator = Elevator(150, [], 0, building)

# Print elevator's information
print(elevator)

# Get information about people on the floors
floor_info = elevator.floor_info()
print("Floor information:", floor_info)

# Check if there are remaining people on the floors
remaining_people = elevator.remaining_people()
print("Remaining people:", remaining_people)

# Pick up people from a specific floor
picked_people, weight_picked = elevator.pick_up(1)
#print("Picked people:", picked_people)
print("Weight picked:", weight_picked)

# Pick up people according to capacity or maximum weight
picked_people_max, total_weight_picked = elevator.pick_up_max(2, 100)
#print("Picked people with max:", picked_people_max)
print("Total weight picked:", total_weight_picked)

# Execute a list of instructions
instructions = [1, 2, 0]
elevator.execute_instructions(instructions)

# Pick up people from all floors in order
pick_up_instructions = elevator.pick_up_in_order()
print("Pick up instructions:", pick_up_instructions)

# Check if instructions are valid
instructions_valid = elevator.valid_instructions(pick_up_instructions)
print("Instructions valid:", instructions_valid)

# Create an elevator using the Create_Elevator function
potential_people = [person1, person2, person3]
elevator2 = Create_Elevator(5, potential_people, 200)

# Print elevator's information
print(elevator2)