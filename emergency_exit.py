# Mini Emergency Exit Planner
# AI Fundamentals Final Project - Aizere Zarkkankyzy, Group 6
# A* + Bayes + MDP

import heapq

# ---------- MAP ----------
# 0 = free, 1 = wall
grid = [
    [0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0],
]
start = (4, 0)                 # classroom
exits = [(5, 5), (0, 5)]       # exit 1 (main door), exit 2 (back stairs)
hall_c = [(4, 2), (4, 3)]      # corridor with the smoke sensor


# ---------- 1. A* SEARCH ----------
def h(cell):
    # Manhattan distance to the closest exit
    return min(abs(cell[0] - e[0]) + abs(cell[1] - e[1]) for e in exits)


def a_star(blocked):
    open_list = [(h(start), 0, start, [start])]   # (f, g, cell, path)
    visited = set()
    while open_list:
        f, g, cell, path = heapq.heappop(open_list)
        if cell in exits:
            return path
        if cell in visited:
            continue
        visited.add(cell)
        r, c = cell
        for nr, nc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
            if 0 <= nr < 6 and 0 <= nc < 6 and grid[nr][nc] == 0 and (nr, nc) not in blocked:
                new_g = g + 1
                heapq.heappush(open_list, (new_g + h((nr, nc)), new_g, (nr, nc), path + [(nr, nc)]))
    return None


# ---------- 2. BAYES ----------
p_alarm_blocked = 0.90    # P(Alarm | Blocked)
p_alarm_clear = 0.15      # P(Alarm | Clear) - false alarm


def bayes(alarm, prior):
    if alarm:
        top = p_alarm_blocked * prior
        bottom = top + p_alarm_clear * (1 - prior)
    else:
        top = (1 - p_alarm_blocked) * prior
        bottom = top + (1 - p_alarm_clear) * (1 - prior)
    return top / bottom


# ---------- 3. MDP ----------
gamma = 0.9
V_safe, V_danger = 100, -100


def Q(steps, p_safe):
    # Q = reward + gamma * (P(safe)*V(safe) + P(danger)*V(danger))
    return -steps + gamma * (p_safe * V_safe + (1 - p_safe) * V_danger)


def mdp(p_blocked, steps_short, steps_long):
    q_proceed_clear = Q(steps_short, 0.95)
    q_proceed_blocked = Q(steps_short, 0.30)
    q_detour = Q(steps_long, 0.90)          # detour does not use Hall C

    q_proceed = (1 - p_blocked) * q_proceed_clear + p_blocked * q_proceed_blocked
    print("   Q(Proceed | Clear)   =", round(q_proceed_clear, 2))
    print("   Q(Proceed | Blocked) =", round(q_proceed_blocked, 2))
    print("   Q(Proceed)           =", round(q_proceed, 2))
    print("   Q(Detour)            =", round(q_detour, 2))

    # NEW: risk threshold where Proceed and Detour are equal
    threshold = (q_proceed_clear - q_detour) / (q_proceed_clear - q_proceed_blocked)
    print("   Risk threshold: the agent goes the short way only if P(blocked) <",
          round(threshold, 3))

    if q_proceed > q_detour:
        return "Proceed"
    return "Detour"


# ---------- NEW: DRAW THE MAP ----------
def draw(path, blocked_hall):
    # S = start, E = exit, # = wall, * = route, X = blocked Hall C, C = Hall C
    for r in range(6):
        row = ""
        for c in range(6):
            cell = (r, c)
            if cell == start:
                ch = "S"
            elif cell in exits:
                ch = "E"
            elif grid[r][c] == 1:
                ch = "#"
            elif cell in path:
                ch = "*"
            elif cell in hall_c:
                ch = "X" if blocked_hall else "C"
            else:
                ch = "."
            row += ch + " "
        print("   " + row)


# ---------- RUN ALL TOGETHER ----------
def run(alarm, prior):
    print("\n========== Sensor alarm:", alarm, "| prior =", prior, "==========")

    path = a_star(blocked=[])
    print("1) A* shortest route:", len(path) - 1, "steps")
    draw(path, blocked_hall=False)

    p = bayes(alarm, prior)
    print("2) Bayes: P(Hall C blocked) =", round(p, 4))

    detour_path = a_star(blocked=hall_c)
    print("3) MDP:")
    action = mdp(p, len(path) - 1, len(detour_path) - 1)
    print("   Decision:", action)

    if action == "Detour":
        path = detour_path
    print("4) Final route:", len(path) - 1, "steps -> exit", path[-1])
    draw(path, blocked_hall=(action == "Detour"))


def ask(question, default):
    # reads an answer; uses the default if the user just presses Enter
    try:
        answer = input(question).strip().lower()
    except EOFError:
        return default
    return answer if answer else default


if __name__ == "__main__":
    print("MINI EMERGENCY EXIT PLANNER")
    mode = ask("Interactive mode? (y/n, Enter = n): ", "n")
    if mode == "y":
        prior = float(ask("How likely is Hall C blocked before the sensor? (0-1, Enter = 0.2): ", "0.2"))
        alarm = ask("Did the smoke sensor beep? (y/n): ", "y") == "y"
        run(alarm, prior)
    else:
        run(alarm=True, prior=0.20)    # test case 1
        run(alarm=False, prior=0.20)   # test case 2
