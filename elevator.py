# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 21:10:47 2023

@author: galgo
"""

import numpy as np

# Elevator Simulation Parameters
parameter = 0.15 # Default parameter to control the frequency of people arriving at each floor

# Person Class
class Person:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.info_list = [self.name, self.weight]

    def __str__(self):
        return self.name + ', weight ' + str(self.weight)

# Floor Class
class Floor:
    def __init__(self, height, persons):
        self.height = height
        self.persons = persons
        weight = 0
        weight_breakdown = []
        for person in self.persons:
            weight += person.weight
            weight_breakdown.append(person.weight)
        self.weight = weight
        self.weight_breakdown = weight_breakdown
        
    def __str__(self):
        persons_descriptions = [str(person_obj) for person_obj in self.persons]
        return f"Floor of height {self.height} with people: {', '.join(persons_descriptions)}"

    def get_persons(self):
        list = []
        for person in self.persons:
            list.append(person.info_list)
        return list
    

def knapsack(values, weights, capacity):
    '''
    Function that solves the knapsack problem using dynamic programming.
    Inputs:
        - values: List containing the value of each element
        - weights: List containing the weight of each element
        - capacity: Maximum capacity of the knapsack
    Outputs:
        - selected_elements: List of indices of the elements in the knapsack
        - total_value: Total value of the elements in the knapsack
    '''
        
    n = len(values)
    matrix = [[0] * (capacity + 1) for i in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                matrix[i][w] = max(matrix[i - 1][w], matrix[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                matrix[i][w] = matrix[i - 1][w]
    total_value = matrix[n][capacity]
    selected_elements = []
    remaining_capacity = capacity
    for i in (range(n, -1, -1)):
        if matrix[i][remaining_capacity] != matrix[i - 1][remaining_capacity]:
            selected_elements.append(i - 1)
            remaining_capacity -= weights[i - 1]
    return selected_elements, total_value

# Elevator Class
class Elevator:
    def __init__(self, capacity, content, position, building, instructions=[]):
        self.capacity = capacity
        self.content = content
        self.position = position
        self.building = building
        self.instructions = instructions
        content_weights = [person.weight for person in self.content]
        self.content_weights = content_weights
        weight_per_floor = []
        for floor in self.building:
            persons_weights = []
            for persons in floor.persons:
                persons_weights.append(persons.weight)
            weight_per_floor.append([floor.height, persons_weights, floor.weight])
        self.weight_per_floor = weight_per_floor
        
    def __str__(self):
        return (f'The building has an elevator of capacity {self.capacity},' 
                f' at the floor {self.position}.')
    
    # Method to get current state of people on the floors and their descriptions
    def floor_info(self):
        info = []
        for floor in self.building:
            sublist = []
            sublist.append(floor.height)
            persons_list = [person.info_list for person in floor.persons]
            sublist.append(persons_list)
            info.append(sublist)
        return info
    
    # Method to check if there are people left on the floors
    def remaining_people(self):
        for floor in self.building:
            if floor.weight != 0:
                return True
        return False

    # Method to empty the elevator and reset its position
    def empty_elevator(self):
        self.position = 0
        self.content = []
        print('All passengers have been dropped off.')
        
    # Method to pick up people from a floor
    def pick_up(self, floor_num):
        self.position = floor_num
        people_to_pick = self.building[floor_num - 1].persons
        weight_to_pick =  self.building[floor_num - 1].weight
        if self.building[floor_num - 1].persons != []:
            picked_people = [str(person) for person in self.building[floor_num - 1].persons]
            print(f"Picked up {', '.join(picked_people)} on floor {self.position}")
            self.content.extend(self.building[floor_num - 1].persons)
            self.building[floor_num - 1].persons = []
            self.building[floor_num - 1].weight = 0
        else:
            print(f'There was no one on floor {self.position}')
            self.building[floor_num - 1].weight = 0
        content_weights = [person.weight for person in self.content]
        self.content_weights = content_weights
        return people_to_pick, weight_to_pick
            
    # Method to pick up people according to capacity or maximum weight
    def pick_up_max(self, floor_num, capacity):
        if capacity == 0:
            return [], 0
        elif capacity >= self.building[floor_num - 1].weight:
            return self.pick_up(floor_num)
        else:
            picked_people = []
            total_weight = 0
            if capacity >= min(self.building[floor_num - 1].weight_breakdown):
                indices, total_weight = knapsack(self.building[floor_num - 1].weight_breakdown, self.building[floor_num - 1].weight_breakdown, capacity)
                quiet_people = []
                for index, person in enumerate(self.building[floor_num - 1].persons):
                    if index in indices:
                        print(f'The person {person} gets in')
                        picked_people.append(person)
                    else:
                        quiet_people.append(person)
                        print(f'The person {person} stays out')
                self.content.extend(picked_people)
                self.building[floor_num - 1].persons = quiet_people
                weight = 0
                weight_breakdown = []
                for person in self.building[floor_num - 1].persons:
                    weight += person.weight
                    weight_breakdown.append(person.weight)
                self.building[floor_num - 1].weight_breakdown = weight_breakdown
                self.building[floor_num - 1].weight = weight
            return picked_people, total_weight
    
    # Method to execute a list of instructions
    def execute_instructions(self, instructions=None):
        if instructions is None:
            instructions = self.instructions
        steps = [str(step) for step in instructions]
        print(f"Floors to visit: {', '.join(steps)}")
        for instruction in instructions:
            self.pick_up(instruction)
        self.empty_elevator()
    
    # Method to pick up people from all floors in a specific order
    def pick_up_in_order(self):
        instructions = []
        remaining_capacity = self.capacity
        while self.remaining_people():
            print(instructions, self.remaining_people())
            for floor_num in range(len(self.building)):
                if self.building[floor_num].weight != 0:
                    picked_people, picked_weight = self.pick_up_max(floor_num + 1, remaining_capacity)
                    if picked_weight != 0:
                        instructions.append(floor_num + 1)
                        remaining_capacity -= picked_weight
            self.empty_elevator()
            instructions.append(0)
            remaining_capacity = self.capacity
        return instructions                
                
    # Method to check if instructions are valid
    def valid_instructions(self, instructions=None):
        print(instructions)
        if instructions is None:
            instructions = self.instructions
        total_weight = 0
        for floor in self.building:
            if floor.height in instructions:
                total_weight += floor.weight
        if total_weight > self.capacity:
            return False
        return True


# Function to Create Elevator
def Create_Elevator(height, potential_people, capacity, frequency=None):
    if frequency is None:
        frequency = [parameter] * len(potential_people)
    people = []
    for floors in range(0, height):
        people_in_floor = []
        for freq in frequency:
            num = np.random.poisson(freq)
            people_in_floor.append(num)
        people.append(people_in_floor)
    building = []
    for i in range(0, len(people)):
        people_in_floor = []
        for j in range(0, len(people[i])):
            people_in_floor.append([potential_people[j]] * people[i][j])
        people_in_floor = [element for sublist in people_in_floor for element in sublist]
        building.append(people_in_floor)
    building = [Floor(i + 1, sublist) for i, sublist in enumerate(building)]
    elevator = Elevator(capacity, [], 0, building)
    return elevator



