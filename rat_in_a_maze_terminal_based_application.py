import random
from queue import PriorityQueue
from colorama import Fore, Style, init
init() 
walls = Fore.RED + '\u2588' + Style.RESET_ALL

# Function to generate a random maze of size n x n
def generate_maze(n, wall_percent):

    maze = [[Fore.BLUE + '◌' + Style.RESET_ALL for _ in range(n)] for _ in range(n)]

    # Place walls randomly based on wall_percent
    for row in maze:
        for i in range(n):
            if random.randint(1, 100) < wall_percent:
                row[i] = walls  # Representing walls

    # Set start and end points
    maze[0][0] = Fore.GREEN + 'S' + Style.RESET_ALL  # Mark start point
    maze[n - 1][n - 1] = Fore.GREEN + 'E' + Style.RESET_ALL  # Mark end point

    return maze

# Function to calculate the shortest path using Dijkstra's algorithm
def dijkstra(maze, n):

    distance = [[float('inf')] * n for _ in range(n)]
    distance[0][0] = 0

    pq = PriorityQueue()
    pq.put((0, (0, 0)))

    # Move in all directions (up, down, left, right)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while not pq.empty():
        dist, (r, c) = pq.get()

        if r == n - 1 and c == n - 1:
            break

        for dr, dc in directions:
            new_r, new_c = r + dr, c + dc
            if 0 <= new_r < n and 0 <= new_c < n and maze[new_r][new_c] != walls:
                if dist + 1 < distance[new_r][new_c]:
                    distance[new_r][new_c] = dist + 1
                    pq.put((dist + 1, (new_r, new_c)))

    
    # Check if there is no path
    if distance[n - 1][n - 1] == float('inf'):
        print("No feasible path exists.")
        return 0

    # Mark the shortest path in the maze with a green color
    r, c = n - 1, n - 1
    while (r, c) != (0, 0):
        maze[r][c] = Fore.GREEN + "◍" + Style.RESET_ALL
        min_dist = distance[r][c]

        for dr, dc in directions:
            new_r, new_c = r + dr, c + dc
            if 0 <= new_r < n and 0 <= new_c < n and distance[new_r][new_c] == min_dist - 1:
                r, c = new_r, new_c
                break

    maze[0][0] = Fore.GREEN + 'S' + Style.RESET_ALL  # Mark start point
    maze[n - 1][n - 1] = Fore.GREEN + 'E' + Style.RESET_ALL  # Mark end point

    return maze

# Function to print the maze
def print_maze(maze):

    border = Fore.RED + '+' + '-' * (3 * len(maze[0])) + '+' + Style.RESET_ALL
    print(border)
    
    for row in maze:
        for cell in row:
            print('|', end='')
            print(f' {cell}', end='')
        print(' |')
        print(border)


def copy_maze(maze):
    return [[cell for cell in row] for row in maze]


n=int(input("Enter the size of the maze(n x n): "))
wall_percentage = 20 #number of random walls should be restricted to be less than or equal to 25%
my_maze = generate_maze(n, wall_percentage)
print("Generated Maze:")
print_maze(my_maze)

while 1:

    print("1.Print the path\n2.Generate another puzzle\n3.Exit the Game")
    choice=input("Enter your choice (1/2/3): ")

    if choice=='1':
        print("Maze with Path:")
        
        maze_copy = copy_maze(my_maze)
        path=dijkstra(maze_copy, n)
        if path:
            print_maze(path)
        break

    elif choice=='2':
        my_maze = generate_maze(n, wall_percentage)
        print("Generated Maze:\n\n")
        print_maze(my_maze)
    else:
        print("Exiting the Rat_Maze game...\n\n")
        break
