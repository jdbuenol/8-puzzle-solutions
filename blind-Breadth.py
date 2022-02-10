# Breadth-First-Search Algorithm implementation for the 8-puzzle
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

def new_state_check(new_state: str, old_states: list, frontier: list):
    for state in old_states:
        if state.get_value() == new_state:
            return False
    for state in frontier:
        if state.get_value() == new_state:
            return False
    return True

if __name__ == '__main__':
    starting_state: str = input("Starting state: ")
    states_queue: list = [state(starting_state, None)]
    old_states: list = []
    solution_node: state = None
    goal_state: bool = False
    while(True):
        if len(states_queue) == 0:
            break
        current_state = states_queue.pop(0)
        print(current_state.get_value())
        if current_state.get_value() == '123456780':
            goal_state = True
            solution_node = current_state
            break
        old_states.append(current_state)
        for state_n in get_neighbours_states(current_state.get_value()):
            if new_state_check(state_n, old_states, states_queue):
                new_state: state = state(state_n, current_state)
                states_queue.append(new_state)
    if(goal_state):
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
    if(not goal_state):
        print("NOT SOLUTION FOUND")