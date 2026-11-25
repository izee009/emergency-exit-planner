# Mini Emergency Exit Planner

AI Fundamentals Final Project. Aizere Zarkkankyzy, Group 6

## Idea
There is a fire in a building. The program helps a student go from the classroom to an exit.
The shortest way goes through Hall C. Hall C has a smoke sensor and may be blocked.

## Algorithms
1. **A\*** finds the shortest route to an exit. h = Manhattan distance to the closest exit.
2. **Bayes** updates P(Hall C blocked) after the sensor reading.
   Prior 0.20, P(alarm | blocked) = 0.90, P(alarm | clear) = 0.15.
3. **MDP** compares Proceed and Detour. Q = −steps + 0.9 · (P(safe) · 100 + P(danger) · (−100)).
4. If the decision is Detour, **A\*** runs again without Hall C.
5. The program also prints the **risk threshold**: the agent goes the short way only if P(blocked) < 0.103.

## Map (6×6)
```
. . . . . E2
. # . . . .
. # . . . .
. # # # # .
S . C C . .
. . # # . E1
```
S = start, E1/E2 = exits, # = wall, C = Hall C

## Run
```
python emergency_exit.py
```
- Press **Enter**: runs the 2 test cases (alarm / no alarm).
- Type **y**: interactive mode. You enter the prior and say if the sensor beeped.

The program draws the map: `*` = route, `X` = blocked Hall C, `C` = Hall C, `E` = exit.

Interesting case: prior = 0.5 and no alarm gives P(blocked) = 0.105. This is just above the threshold, so the agent still chooses Detour.

## Output (2 test cases)
| Sensor | P(blocked) | Q(Proceed) | Q(Detour) | Decision | Route |
|---|---|---|---|---|---|
| Alarm | 0.60 | 4.8 | 63.0 | Detour | 9 steps to E2 |
| No alarm | 0.0286 | 71.66 | 63.0 | Proceed | 6 steps to E1 |

Full output is in `output.txt`.

## Web demo
Open `web/index.html` in any browser (no installation, works offline).
It is a visual demo of the same three algorithms (rewritten in JavaScript):
a colored map with the route, a sensor switch, a prior slider and live Bayes / MDP numbers.
The main implementation is `emergency_exit.py`.

## Assumptions
All probabilities and rewards are made up for a toy model. No real data.

## Future work

More sensors, value iteration for the full MDP, a real floor plan.

## AI use
I used Claude to help write and check the code. I checked all numbers by hand.
