import re
from collections import deque

class Valve:
    def __init__(self, id, flow, neighbors):
        self.id = id
        self.flow = flow
        self.neighbors = neighbors
    
    def __repr__(self):
        return f"ID: {self.id}, Flow: {self.flow}, Neighbors: {self.neighbors}"

class State:
    valve_list = []
    max_time = 0
    n_agents = 1

    def __init__(self, n_agents, agent_init, valve_dict, dist_mtx, state=0, score=0):
        self.agents = [agent_init] * n_agents
        self.valve_dict = valve_dict
        self.dist_mtx = dist_mtx
        self.valve_state = state
        self.score = score 

    def get_new_positions(self, agent_id):
        agent_pos, agent_time = self.agents[agent_id]
        return filter(
            lambda valve: (
                self.valve_state & (1 << self.valve_list.index(valve)) == 0 and
                agent_time + (self.dist_mtx[agent_pos][valve] + 1) <= State.max_time
            ),
            self.valve_list
        )
    
    def open_valve(self, valve_id, agent_id):
        try:
            valve_num = self.valve_list.index(valve_id)
        except ValueError:
            raise ValueError("Valve ID not found: {}".format(valve_id))
        
        dist = self.dist_mtx[self.agents[agent_id][0]][valve_id]
        newstate = self.copy()
        if newstate.agents[agent_id][1] + dist + 1 > State.max_time:
            # This move is not possible
            return None
        
        newstate.agents[agent_id] = (valve_id, self.agents[agent_id][1] + dist + 1)
        newstate.valve_state |= (1 << valve_num)
        t_remaining = State.max_time - newstate.agents[agent_id][1]
        newstate.score += self.valve_dict[valve_id].flow * t_remaining
        # Sort agents by time to next one to move is always at the front
        newstate.agents.sort(key = lambda agent: agent[1])

        return newstate
        
    def copy(self):
        # Return a new State with the same parameters as this one
        newstate = State(
            len(self.agents), ("AA", 0), self.valve_dict, self.dist_mtx, 
            self.valve_state, self.score
        )
        for i in range(len(self.agents)):
            newstate.agents[i] = self.agents[i]
        return newstate

    def __hash__(self):
        return hash((self.valve_state, tuple(self.agents)))

    def __repr__(self):
        return (
            f"""Agents:\n{self.agents}, """
            f"""Valve state: {bin(self.valve_state)}, """
            f"""Score: {self.score}"""
        )


def read_puzzle(fname):
    valves = dict()
    # Read in puzzle data
    for line in map(str.strip, open(fname).readlines()):
        flow = int(re.findall("[0-9]+", line)[0])
        valve_names = re.findall("[A-Z]{2}", line)
        valve_id, neighbors = valve_names[0], valve_names[1:]
        valves[valve_id] = Valve(valve_id, flow, neighbors)

    return valves


def compute_distance_matrix(valves, init_valve="AA", prune_zeros=True):
    # Compute the distance matrix for this graph.
    init_distance = len(valves)+1 # "infinity" in Floyd-Warshall algorithm
    dist = dict()
    # Initialize all off-diagonal distances to infinity
    for key_outer in valves:
        dist[key_outer] = dict()
        for key_inner in valves:
            if key_inner in valves[key_outer].neighbors:
                dist[key_outer][key_inner] = 1
            else:
                dist[key_outer][key_inner] = init_distance
        # Initialize on-diagonal distances to 0
        dist[key_outer][key_outer] = 0

    # Compute off-diagonal distances
    for k in valves:
        for i in valves:
            for j in valves:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    if not prune_zeros: return dist

    # Since there is no reason to visit a valve with flow rate 0, remove zero-flow
    # valves from the distance matrix, but keep the init node as a source.
    zero_flow_valves = [key for key in valves if valves[key].flow == 0]
    for zf in zero_flow_valves:
        if zf != init_valve:
            dist.pop(zf)
    for source in dist:
        for zf in zero_flow_valves:
            dist[source].pop(zf)
        if source != init_valve:
            dist[source].pop(source)
    
    return dist

def get_high_score_bfs(init_state):
    Q = deque()
    best_scores = dict()

    Q.append(init_state)
    best_scores[init_state] = init_state.score
    high_score = init_state.score

    while len(Q) > 0:
        cur_state = Q.popleft()

        next_agent = 0
        new_positions = cur_state.get_new_positions(next_agent)
        for np in new_positions:
            new_state = cur_state.open_valve(np, next_agent)
            # Accept the new state if it is not seen before OR
            # if it is higher-scoring than the last time this
            # state was seen.
            if (
                new_state not in best_scores or
                new_state.score > best_scores[new_state]
            ):
                Q.append(new_state)
                best_scores[new_state] = new_state.score
                high_score = max(high_score, new_state.score)
    
    # All paths have been explored, return the max score
    return high_score


# Read in data and prune zero-flow valves from the distance matrix
init_valve = "AA"
valve_dict = read_puzzle("2022/d16_input.txt")
valve_dist = compute_distance_matrix(valve_dict, init_valve=init_valve)

# Set constants in the state class
State.valve_list = list(sorted(valve_dist.keys()))
State.valve_list.remove(init_valve)
State.max_time = 30

init_state = State(1, (init_valve, 0), valve_dict, valve_dist)

high_score = get_high_score_bfs(init_state)
print("Part 1:", high_score)

# Part 2 - now there are two agents.
State.max_time = 26
init_state = State(2, (init_valve, 0), valve_dict, valve_dist)

# path_state = init_state.open_valve("JJ", 0)
# print(path_state)
high_score = get_high_score_bfs(init_state)
print("Part 2:", high_score)
