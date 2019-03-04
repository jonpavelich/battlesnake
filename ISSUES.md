# Bugs
- When chasing its tail the snake stays immediately behind it, so it collides with its tail immediately after consuming food when the tail fails to move
- No move sanity checks are performed, so unsafe or deadly moves are possible
- Pathfinding will always find a path, even across heavily negative boundaries, so if a snake cuts the board in half and food is on the other side, we pathfind through the body instead of giving up

# Improvements
- Pathfind to all viable targets, and choose the one with the lowest gscore instead of the nearest Manhattan distance
- Evolve our tactics as the game progresses (e.g. behave differently during a 1v1)
- Logging output should be muted in production
