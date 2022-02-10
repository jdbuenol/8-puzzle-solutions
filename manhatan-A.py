# A* algorithm implementation for the 8-puzzle using Manhatan distance as Heuristic Function
class state:
    def __init__(self, value: str, parent):
        self.value = value
        self.parent = parent
    
    def get_value(self):
        return self.value
    
    def get_parent(self):
        return self.parent
    
    def get_path_cost(self):
        if self.parent == None:
            return 0
        return 0.5 + self.parent.get_path_cost()
    
    def set_parent(self, new_parent):
        self.parent = new_parent

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

def new_state_check(new_state: str, old_states: list, frontier: list, new_state_path_cost: int, goal_state: str, new_parent: state):
    for state in old_states:
        if new_state == state.get_value():
            if new_state_path_cost < state.get_path_cost():
                state.set_parent(new_parent)
            return -1
    for x in range(len(frontier)):
        if frontier[x].get_value() == new_state:
            if new_state_path_cost < frontier[x].get_path_cost():
                frontier.pop(x)
                return x
            return -1
        if new_state_path_cost + manhatan_distance(new_state, goal_state) < frontier[x].get_path_cost() + manhatan_distance(frontier[x].get_value(), goal_state):
            return x
    return len(frontier)
    

def manhatan_distance(value1: str, value2: str):
    dist: int = 0
    for x in range(9):
        char: str = value1[x]
        dist += abs(x - value2.find(char))
    return dist

if __name__ == '__main__':
    starting_state: str = input("Starting state: ")
    start_state: state = state(starting_state, None)
    states_queue: list = [start_state]
    goal_state: str = '123456780'
    old_states: list = []
    solution_node: state = None
    goal_achieved: bool = False
    while True:
        if len(states_queue) == 0:
            break
        start_state = states_queue.pop(0)
        print(start_state.get_value() + ' ' + str(manhatan_distance(start_state.get_value(), goal_state)))
        if(start_state.get_value() == goal_state):
            solution_node = start_state
            goal_achieved = True
            break
        old_states.append(start_state)
        for n_state in get_neighbours_states(start_state.get_value()):
            new_state: state = state(n_state, start_state)
            state_check: int = new_state_check(n_state, old_states, states_queue, new_state.get_path_cost(), goal_state, start_state)
            if state_check != -1:
                states_queue.insert(state_check, state(n_state, start_state))
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