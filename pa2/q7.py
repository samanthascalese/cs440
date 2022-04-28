# FOR QUESTION 7

from colorama import Fore
import numpy as np

# for debugging
DEBUG = False


# STATES
S1 = 0
S2 = 1
S3 = 2
S4 = 3

# ACTIONS
UP = 0    #a1
RIGHT = 1 #a2
DOWN = 2  #a3
LEFT = 3  #a4

# REWARDS --> S3 is goal state
MAP = [0, 0, 1, 0]
POLICY = [-2, -2, -1, -2] #default + / -

# TRANSITION MODEL --> T[STATE][ACTION], if fails - remains in same state
# initialize
T = [[[(-1, -1)] for i in range(4)] for j in range(4)]
# S1
T[S1][UP] = [(0.8, S2)]
T[S1][RIGHT] = [(0.8, S4)]
# S2
T[S2][RIGHT] = [(0.8, S3)]
T[S2][DOWN] = [(0.8, S1)]
# S3 - #TODO: is this one necessary?
T[S3][LEFT] = [(1, S2)]
T[S3][DOWN] = [(1, S4)]
# S4
T[S4][UP] = [(0.9, S3)]
T[S4][LEFT] = [(0.8, S1)]


def print_value_grid(values):

    color = []
    for val in values:
        if val <= 0.25:
            color.append(Fore.LIGHTRED_EX)
        elif val <= 0.75:
            color.append(Fore.LIGHTGREEN_EX)
        elif val <= 1:
            color.append(Fore.GREEN)

    if (DEBUG): print(f'values in grid = {values}')
    
    print('Value Function Grid:')
    print(f'| {color[1]}{values[S2]:.3f}{Fore.RESET} | {color[2]}{values[S3]:.3f}{Fore.RESET} |')
    print(f'| {color[0]}{values[S1]:.3f}{Fore.RESET} | {color[3]}{values[S4]:.3f}{Fore.RESET} |')
    print()

    return


def print_policy_grid(values):

    color = []
    for val in values:
        if val <= 0.25:
            color.append(Fore.LIGHTRED_EX)
        elif val <= 0.75:
            color.append(Fore.LIGHTGREEN_EX)
        elif val <= 1:
            color.append(Fore.GREEN)

    direction = []
    for dir in POLICY:
        if dir == -1:
            direction.append('+')
        if dir == -2:
            direction.append('-')
        if dir == UP:
            direction.append('\u2191')
        if dir == RIGHT:
            direction.append('\u2192')
        if dir == DOWN:
            direction.append('\u2193')
        if dir == LEFT:
            direction.append('\u2190')

    if (DEBUG): print(f'actions in policy = {POLICY}')
    
    print('Policy Grid:')
    print(f'| {color[1]}{direction[1]}{Fore.RESET} | {color[2]}{direction[2]}{Fore.RESET} |')
    print(f'| {color[0]}{direction[0]}{Fore.RESET} | {color[3]}{direction[3]}{Fore.RESET} |')
    print()

    return



def value_iteration(threshold=0.0001, gamma=0.8):

    def calulate_v(v, state, action):

        [(prob, next_state)] = T[state][action]
        #V(s) = R(s) + P(s, a, s') * gamma * V(s')
        val = MAP[state] + (prob * gamma * v[next_state])

        return val
    

    # initialize map
    v_prime = [0, 0, 1, 0]
    i = 0

    # print starting grid
    print(f'Iteration: {i}')
    print('- - - - - - - - -')
    print_policy_grid(MAP)
    print_value_grid(MAP)
    print('- - - - - - - - - - - - - - - - - - - - - - - - -')
    print()


    # start iterating!
    while True:

        v = v_prime

        # re-initialize
        v_prime = [0, 0, 1, 0]
        i += 1
        j = 0
        delta = [0]*3

        # iterate through all states
        for state in range(len(MAP)):

            if state == S3: continue

            action_rewards = [0, 0, 0, 0] #initialize [A1, A2, A3, A3]

            # assign actions
            actions = []
            if state == S1: actions = [UP, RIGHT]
            if state == S2: actions = [RIGHT, DOWN]
            if state == S4: actions = [UP, LEFT]

            # iterate through all actions
            for action in actions:

                action_rewards[action] = calulate_v(v, state, action)

            # maximize rewards
            best_action = np.max(action_rewards)
            action_index = action_rewards.index(best_action)
            v_prime[state] = best_action

            # update policy
            POLICY[state] = action_index

            # update delta
            delta[j] = np.abs(best_action - v[state])
            j += 1

        # check for convergence
        if np.max(delta) < threshold:
            break

        # print for each iteration
        print(f'Iteration: {i}')
        print('- - - - - - - - -')
        print_policy_grid(v_prime)
        print_value_grid(v_prime)
        print(f'Change in Value Function (Delta): {np.max(delta):.5f}')
        print('- - - - - - - - - - - - - - - - - - - - - - - - -')
        print()


    # final print
    print(f'Done! Iteration: {i}')
    print('- - - - - - - - -')
    print_policy_grid(v_prime)
    print_value_grid(v_prime)
    print(f'Change in Value Function (Delta): {np.max(delta):.5f}')
    print('- - - - - - - - - - - - - - - - - - - - - - - - -')
    print()

    return



if __name__ == "__main__":

    value_iteration()
