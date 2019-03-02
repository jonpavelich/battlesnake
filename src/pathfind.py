import random

"""
Board is the entire board object.
Weights is a weighted n x n list. Bigger = better suntanning
startPos is a {x , y}, this is the head of our snake
endPos is [{x, y}, {x, y}] this is a list of targets, pick the closest
"""
def find_path(board, weights, startPos, endPos):
    width = board['width']
    height = board['height']
    print(board)
    directions = ['up', 'down', 'left', 'right']
    return random.choice(directions)