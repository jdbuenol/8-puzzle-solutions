# Best-First-Search Greedy implementation for the 8-puzzle using Levenstein distance as Heuristic function
class state:
    def __init__(self, value: str, parent):
        self.value = value
        self.parent = parent
    
    def get_value(self):
        return self.value
    
    def get_parent(self):
        return self.parent

def get_neighbours_states(value: str):
    idx_z: int = value.find("0")
    idx_neighbours: list = []
    if(idx_z - 1 not in [-1, 2, 5]):
        idx_neighbours.append(idx_z - 1)
    if(idx_z + 1 not in [3, 6, 9]):
        idx_neighbours.append(idx_z + 1)
    if(idx_z - 3 >= 0):
        idx_neighbours.append(idx_z - 3)
    if(idx_z + 3 <= 8):
        idx_neighbours.append(idx_z + 3)
    neighbours_states: list = []
    for x in range(len(idx_neighbours)):
        new_value: str = ""
        idx_current: int = idx_neighbours[x]
        if(idx_current < idx_z):
            new_value += value[:idx_current] + '0' + value[idx_current + 1:idx_z] + value[idx_current] + value[idx_z + 1:]
        else:
            new_value += value[:idx_z] + value[idx_current] + value[idx_z + 1:idx_current] + '0' + value[idx_current + 1:]
        neighbours_states.append(new_value)
    return neighbours_states

def new_state_check(new_state: str, old_states: list):
    for state in old_states:
        if state.get_value() == new_state:
            return False
    return True

def levenstein_distance(value1: str, value2: str):
    dist: int = 0
    for x in range(9):
        if value1[x] != value2[x]:
            dist += 1
    return dist

if __name__ == '__main__':
    starting_state: str = input("Starting state: ")
    start_state: state = state(starting_state, None)
    goal_state: str = '123456780'
    old_states: list = []
    solution_node: state = None
    goal_achieved: bool = False
    while True:
        states_queue: list = []
        states_values: list = []
        if start_state == None:
            break
        if start_state.get_value() == goal_state:
            goal_achieved = True
            solution_node = start_state
            break
        print(start_state.get_value())
        old_states.append(start_state)
        for state_n in get_neighbours_states(start_state.get_value()):
            if new_state_check(state_n, old_states):
                new_state: state = state(state_n, start_state)
                states_queue.append(new_state)
                states_values.append(levenstein_distance(goal_state, state_n))
        if len(states_queue) == 0:
            old_states.append(start_state)
            start_state = start_state.get_parent()
            continue
        idx_lowest: int = 0
        lowest: int = 8
        for x in range(len(states_queue)):
            if states_values[x] < lowest:
                lowest = states_values[x]
                idx_lowest = x
        start_state = states_queue[idx_lowest]
    if(goal_achieved):
        print("SOLUTION FOUND: ")
    solution_queue: list = []
    while(solution_node != None):
        solution_queue.append(solution_node.get_value())
        solution_node = solution_node.get_parent()
    while(len(solution_queue) > 0):
        current_solution: str = solution_queue.pop()
        if len(solution_queue) == 0:
            print(current_solution)
            break
        current_idx_z: int = current_solution.find('0')
        next_idx_z: int = solution_queue[-1].find('0')
        if next_idx_z - current_idx_z == 1:
            current_solution += " RIGHT"
        if next_idx_z - current_idx_z == -1:
            current_solution += " LEFT"
        if next_idx_z - current_idx_z == 3:
            current_solution += " DOWN"
        if next_idx_z - current_idx_z == -3:
            current_solution += " UP"
        current_solution += " " + str(len(solution_queue))
        print(current_solution)
    if(not goal_achieved):
        print("NOT SOLUTION FOUND")