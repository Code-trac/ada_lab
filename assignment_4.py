# Backtracking - Assign flights to crew without overlap

flights = [('F1', 9, 11), ('F2', 10, 12), ('F3', 12, 14)]
crew = ['C1', 'C2']

assignment = {}

def is_valid(flight, crew_member):
    for f, c in assignment.items():
        if c == crew_member:
            if not (flight[2] <= f[1] or flight[1] >= f[2]):
                return False
    return True

def backtrack(i):
    if i == len(flights):
        return True
    
    for c in crew:
        if is_valid(flights[i], c):
            assignment[flights[i]] = c
            if backtrack(i + 1):
                return True
            del assignment[flights[i]]
    
    return False

backtrack(0)
print("\nAssignment 4 - Task 1 (Backtracking: Flight-Crew Assignment)")
print(assignment)

# Branch and Bound - Minimize crew usage

best = float('inf')
best_assign = {}

def count_used(assign):
    return len(set(assign.values()))

def branch_and_bound(i, current):
    global best, best_assign
    
    if i == len(flights):
        cost = count_used(current)
        if cost < best:
            best = cost
            best_assign = current.copy()
        return
    
    if count_used(current) >= best:
        return
    
    for c in crew:
        valid = True
        for f, cc in current.items():
            if cc == c:
                if not (flights[i][2] <= f[1] or flights[i][1] >= f[2]):
                    valid = False
                    break
        
        if valid:
            current[flights[i]] = c
            branch_and_bound(i + 1, current)
            del current[flights[i]]

branch_and_bound(0, {})
print("\nAssignment 4 - Task 2 (Branch and Bound: Minimize Crew Usage)")
print(best_assign)

# Naive string matching with comparison count

def naive_search(text, pattern):
    n, m = len(text), len(pattern)
    count = 0
    
    for i in range(n - m + 1):
        match = True
        for j in range(m):
            count += 1
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            print("Pattern found at index", i)
    
    print("Comparisons:", count)

text = "ABABDABACDABABCABAB"
pattern = "ABABCABAB"

print("\nAssignment 4 - Task 3 (Naive String Matching)")
naive_search(text, pattern)

# Compare time for increasing text size

import time

def test(size):
    text = "A" * size + "B"
    pattern = "AB"
    
    start = time.time()
    naive_search(text, pattern)
    end = time.time()
    
    return end - start

print("\nAssignment 4 - Task 4 (Naive Search Time Comparison)")
for size in [100, 500, 1000]:
    print(f"Text size {size}: {test(size):.6f} seconds")


