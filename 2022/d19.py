# Following along with a cvxpy solution posted on topaz.github.io
# Seemed like a fun library to try :)

import re
import cvxpy as cp
import numpy as np

def read_puzzle(fname):
    blueprints = []
    with open(fname) as f:
        for line in map(str.strip, f.readlines()):
            nums_in_line = list(map(int, re.findall(r'\d+', line)))
            blueprints.append(np.transpose([
                # Column order is ore, clay, obsid, geode. Note that geode
                # is always zero.

                # Ore robot
                [nums_in_line[1], 0, 0, 0],
                # Clay robot
                [nums_in_line[2], 0, 0, 0],
                # Obsidian robot
                [nums_in_line[3], nums_in_line[4], 0, 0],
                # Geode robot
                [nums_in_line[5], 0, nums_in_line[6], 0]
            ]))
    
    return blueprints

def max_geodes_for_blueprint(bp, max_time):
    # Summary of constraints:
    # `resources` is a (max_time, 4) array of no. resources available at step i.
    # `robots` is a (max_time, 4) array of no. robots available at step i.
    # `production` is a (max_time, 4) array of boolean production decisions.

    resources = []
    robots = []
    production = []
    constraints = []

    for i in range(max_time+1):
        resources_var = cp.Variable(4)
        robots_var = cp.Variable(4)
        production_var = cp.Variable(4, boolean=True)
        if i == 0:
            # Init conditions
            # Start with no resources
            constraints.append(resources_var == 0)
            # Have one ore bot and nothing else
            constraints.append(robots_var[0] == 1)
            constraints.append(robots_var[1:] == 0)
            # Nothing gets made on minute 0.
            constraints.append(production_var == 0)
        else:
            prev_resources = resources[-1]
            # Current no. of robots must match previous production
            constraints.append(robots_var == robots[-1] + production[-1])

            # Can only make one robot
            constraints.append(cp.sum(production_var) <= 1)

            costs = bp @ production_var
            # Costs incurred from production must be <= previous resources
            constraints.append(costs <= prev_resources)
            # Current resources are added to by robots, subtracted by costs
            constraints.append(resources_var == (prev_resources + robots_var - costs))
        
        robots.append(robots_var)
        production.append(production_var)
        resources.append(resources_var)
    
    # Problem is defined, now solve
    # Max geodes in the final time step.
    objective = cp.Maximize(resources[-1][3])

    problem = cp.Problem(objective, constraints)

    problem.solve()
    # print(problem.value)
    return problem.value

blueprints = read_puzzle("2022/d19_input.txt")

part1_out = 0
part1_time = 24
for i in range(len(blueprints)):
    quality_level = (i+1) * max_geodes_for_blueprint(blueprints[i], part1_time)
    part1_out += quality_level
print("Part 1 answer:", part1_out)

part2_out = 1
part2_time = 32
for bp in blueprints[:3]:
    part2_out *= max_geodes_for_blueprint(bp, part2_time)
print("Part 2 answer:", part2_out)