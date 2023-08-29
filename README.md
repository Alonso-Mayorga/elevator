# Elevator Simulation

This project simulates the behavior of an elevator in a building with multiple floors and passengers. It includes classes for `Person`, `Floor`, and `Elevator`, along with various methods and functions to interact with and simulate the elevator's behavior.


## Classes

### Person

Represents a person with a name and weight.

### Floor

Represents a floor in the building with a height and a list of people on that floor.

### Elevator

Represents the elevator in the building. It has attributes for capacity, current content, position, building layout, and instructions. This class includes methods for picking up passengers, executing instructions, checking remaining people, and more.

## Functions

### Knapsack

A dynamic programming solution for the knapsack problem, used within the Elevator class to optimize passenger selection based on capacity.

### Create_Elevator

Creates a random building with the parameters given

## Usage

1. Create instances of `Person` with names and weights.
2. Create instances of `Floor` with heights and lists of people.
3. Create an instance of `Elevator` with capacity, initial content, position, and building layout.
4. Interact with the elevator using its methods to pick up passengers, execute instructions, and more.
5. Use Create_Elevator if needed

## Examples

```python
# Create persons
person1 = Person("Alice", 60)
person2 = Person("Bob", 70)

# Create floors with people
floor1 = Floor(1, [person1])
floor2 = Floor(2, [person2])

# Create building with floors
building = [floor1, floor2]

# Create an elevator
elevator = Elevator(150, [], 0, building)

# Pick up people and execute instructions
instructions = [1, 2, 0]
elevator.execute_instructions(instructions)
```

## Contributing

Feel free to contribute to this repository by suggesting improvements, reporting issues, or adding new methods for solving linear equations.

## License

This project is licensed under the [MIT License](license.txt).
