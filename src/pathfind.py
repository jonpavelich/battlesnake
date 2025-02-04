import random
from queue import PriorityQueue
import logging

"""
Board is the entire board object.
Weights is a weighted n x n list. Bigger = better suntanning
startPos is a {x , y}, this is the head of our snake
endPos is [{x, y}, {x, y}] this is a list of targets, pick the closest
"""
def find_path(board, weights, startPos, endPos):
    width = board['width']
    height = board['height']

    graph = graphify(weights, width, height)
    
    s_x = startPos['x']
    s_y = startPos['y']
    mindist = 100000
    end = endPos[0]
    for e in endPos:
        if manhattan_dist(s_x, s_y, e['x'], e['y']) < mindist:
            mindist = manhattan_dist(s_x, s_y, e['x'], e['y'])
            end = e
    e_x = end['x']
    e_y = end['y']
    logging.info(f"selected target {e_x}, {e_y}")

    start = cart_to_abs(s_x, s_y, width)
    end = cart_to_abs(e_x, e_y, width)
    path = a_star(graph, start, end, width)
    pretty_path = [abs_to_cart(x, width) for x in path]

    logging.debug(f"path is {pretty_path}")
    logging.info(f"we will move from {abs_to_cart(path[-1], width)} to {abs_to_cart(path[-2], width)}")
    pt = abs_to_cart(path[-2], width)
    x = pt[0]
    y = pt[1]

    if x < s_x:
        logging.info("Moving left")
        return "left"
    if x > s_x:
        logging.info("Moving right")
        return "right"
    if y < s_y:
        logging.info("Moving up")
        return "up"
    if y > s_y:
        logging.info("Moving down")
        return "down"
    
    logging.error("Path doesn't correspond to a valid move!")
    directions = ['up', 'down', 'left', 'right']
    return random.choice(directions)

"""
Convert a cartesian coordinate to a single value
"""
def cart_to_abs(x, y, width):
    return y*width + x

"""
Convert a single value to a cartesian coordinate
"""
def abs_to_cart(z, width):
    x = z % width
    y = z // width
    return (x, y)

"""
Find the Manhattan Distance between two points (x1, y1) and (x2, y2)
"""
def manhattan_dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

"""
Builds an weighted graph (as an adjacency list) from a weight matrix
"""
def graphify(weights, width, height):
    graph = dict()
    for x in range(width):
        for y in range(height):
            neighbors = set()
            
            for i,j in [(x+1,y), (x-1, y), (x, y-1), (x, y+1)]:
                if i >= 0 and i < width and j >= 0 and j < height:
                    neighbors.add(cart_to_abs(i, j, width))
            graph[cart_to_abs(x, y, width)] = (weights[x][y], neighbors)
    return graph

"""
Perform A* search to find an optimal path from start to goal on graph
"""
def a_star(graph, start, goal, width):
    logging.debug(f"pathfinding from {abs_to_cart(start, width)} to {abs_to_cart(goal, width)}")

    closed_set = set()              # set of already evaluated nodes
    came_from = {}                  # for each node, which node it can most efficiently be reached from
    gscore = {}                     # for each node, the cost of getting from the start node to that node
    for i in range(len(graph)):
        gscore[i] = 1000000
    gscore[start] = 0
    fscore = {}                     # For each node, the total cost of getting from the start node to the goal by passing by that node
    fscore[start] = heuristic_cost_estimate(start, goal, width)
    open_set_q = PriorityQueue()      # set of discovered nodes yet to be evaluated
    open_set_q.put((fscore[start], start))
    open_set = set()
    open_set.add(start)
    
    while not open_set_q.empty():
        current = open_set_q.get()
        current = current[1]
        open_set.remove(current)
        logging.debug(f"  current is {current}")
        if current == goal:
            logging.info("Pathfinding reached goal")
            logging.debug(f"gscores: {gscore}")
            logging.debug(f"fscores: {fscore}")
            return reconstruct_path(came_from, current)
        
        closed_set.add(current)

        for neighbor in graph[current][1]:
            logging.debug(f"    check neighbour {neighbor}")
            if neighbor in closed_set:
                continue
            
            tentative_gscore = gscore[current] + dist_between(current, neighbor, width) - graph[neighbor][0]

            if tentative_gscore >= gscore[neighbor]:
                continue
            
            came_from[neighbor] = current
            gscore[neighbor] = tentative_gscore
            fscore[neighbor] = gscore[neighbor] + heuristic_cost_estimate(neighbor, goal, width)
            if neighbor not in open_set:
                open_set.add(neighbor)
                open_set_q.put((fscore[neighbor], neighbor))

def heuristic_cost_estimate(neighbor, goal, width):
    neighbor_pt = abs_to_cart(neighbor, width)
    goal_pt = abs_to_cart(goal, width)
    return manhattan_dist(neighbor_pt[0], neighbor_pt[1], goal_pt[0], goal_pt[1])

def dist_between(a, b, width):
    a = abs_to_cart(a, width)
    b = abs_to_cart(b, width)
    return manhattan_dist(a[0], a[1], b[0], b[1])

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    logging.debug(f"path is {total_path}")
    return total_path
