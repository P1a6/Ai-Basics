import random
from  planning.planning_problem import Planning_Problem 
from collections import deque
import heapq

class Planner():
    """
        Planner class with different planning method implementations
    """

    @classmethod
    def random_search(cls, start_state):
        """
            Implementation of random search.

            returns (path, step_count) where path is a list of actions to the goal and step_count is the number of states extended
        """

        open_list = [(start_state,[])] 
        start_state["path"]  = [] 
        step_count = 0
        
        while len(open_list) > 0:
            state, path = random.choice(open_list)
            step_count+= 1

            for action in Planning_Problem.actions:
                next_state = Planning_Problem.state_transition(state,action)
                next_path = path + [action]

                if Planning_Problem.goal(next_state):
                    return next_path, step_count
                else:
                    open_list.append((next_state,next_path))

        return None, step_count
    

    @classmethod
    def breadth_first_search(cls, start_state):
        """
            Implementation of Breadth First Search

            returns (path, step_count) where path is a list of actions to the goal and step_count is the number of states extended
        """

        def key(state):
            return (state["toaster_has_power"], state["toaster_is_on"],state["bread_location"], state["bread_state"])

             
        step_count = 0
        to_visit = deque([(start_state, [])])
        visited = {key(start_state)}


        while to_visit:
             state, path = to_visit.popleft()
             if Planning_Problem.goal(state):
                 return path, step_count
             step_count += 1


             for action in Planning_Problem.actions:
                next_state = Planning_Problem.state_transition(state, action)
                if key(next_state) not in visited:
                    visited.add(key(next_state))
                    to_visit.append((next_state, path + [action]))
 



        return None, step_count
    

    @classmethod
    def shortest_toast_time_search(cls, start_state):
        """
            Implementation of a search algorithm that also optimized for the time it takes to toast a slice of bread.
            This time is measured within the state in attribute ["time"]

            returns (path, step_count) where path is a list of actions to the goal and step_count is the number of states extended
        """
        step_count = 0
        
        def key(state):
            return (state["toaster_has_power"], state["toaster_is_on"],state["bread_location"], state["bread_state"])

        counter = 0 
        to_visit = [(start_state["time"], counter, start_state, [])]
        best_time = {key(start_state): start_state["time"]} 

        while to_visit:
            time, number, state, path = heapq.heappop(to_visit) 
            if time > best_time[key(state)]:
                continue 
            if Planning_Problem.goal(state):
                return path, step_count
            step_count += 1

            for action in Planning_Problem.actions:
                next_state = Planning_Problem.state_transition(state, action)
                next_time = next_state["time"]
                if key(next_state) not in best_time or next_time < best_time[key(next_state)]:
                    best_time[key(next_state)] = next_time
                    counter += 1
                    heapq.heappush(to_visit, (next_time, counter, next_state, path + [action]))



        return None, step_count