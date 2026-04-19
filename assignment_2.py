# -------- TASK 1 --------
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

arr = [10,20,40,70,89,100]
print("Binary Search",binary_search(arr, 89))

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


arr2 = [10,20,32,11,3,6,52]
print("Merge Sort:",merge_sort(arr2))

# -------- TASK 2 --------
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)
print("Quick Sort: ",quick_sort(arr2))

# -------- TASK 3 --------
def knapsack_01(weights, values, W):
    n = len(weights)
    dp = [[0]*(W+1) for _ in range(n+1)]
    for i in range(1, n+1):
        for w in range(W+1):
            if weights[i-1] <= w:
                dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
    return dp[n][W]

print("Knapsack: ",knapsack_01([10,20,30],[60,100,120],50))


# -------- TASK 4 --------
import functools

def fib_naive(n):
    if n <= 1:
        return n
    return fib_naive(n-1) + fib_naive(n-2)

@functools.lru_cache(None)
def fib_memo(n):
    if n <= 1:
        return n
    return fib_memo(n-1) + fib_memo(n-2)

def fib_dp(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, a+b
    return b

print("DP ",fib_dp(10))
print("Naive ",fib_naive(10))
print("Memo ",fib_memo(10))

# Fibonacci time comparison graph
n_values = [5, 10, 15, 20, 25, 28]
naive_times, memo_times, dp_times = [], [], []

for n in n_values:
    start = time.perf_counter()
    fib_naive(n)
    naive_times.append(time.perf_counter() - start)

    fib_memo.cache_clear()
    start = time.perf_counter()
    fib_memo(n)
    memo_times.append(time.perf_counter() - start)

    start = time.perf_counter()
    fib_dp(n)
    dp_times.append(time.perf_counter() - start)

'''
plt.plot(n_values, naive_times, marker='o', label='Naive')
plt.plot(n_values, memo_times, marker='o', label='Memoized')
plt.plot(n_values, dp_times, marker='o', label='DP')
plt.xlabel('n')
plt.ylabel('Time (seconds)')
plt.title('Fibonacci Time Comparison')
plt.legend()
plt.grid(True)
plt.show()

'''


# -------- TASK 5 --------
import itertools
import math

def euclidean_dist(c1, c2):
    return math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2)

def build_dist_matrix(cities):
    n = len(cities)
    dist = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dist[i][j] = euclidean_dist(cities[i], cities[j])
    return dist

def tour_length(tour, dist):
    return sum(dist[tour[i]][tour[i+1]] for i in range(len(tour)-1)) + dist[tour[-1]][tour[0]]

def tsp_brute_force(dist):
    n = len(dist)
    cities = list(range(1, n))
    best_len = float('inf')
    best_tour = None
    for perm in itertools.permutations(cities):
        tour = [0] + list(perm)
        length = tour_length(tour, dist)
        if length < best_len:
            best_len = length
            best_tour = tour
    return best_len, best_tour

def tsp_nearest_neighbour(dist, start=0):
    n = len(dist)
    visited = [False]*n
    tour = [start]
    visited[start] = True
    for _ in range(n-1):
        current = tour[-1]
        nearest = min((j for j in range(n) if not visited[j]), key=lambda j: dist[current][j])
        tour.append(nearest)
        visited[nearest] = True
    return tour_length(tour, dist), tour

def tsp_held_karp(dist):
    n = len(dist)
    INF = float('inf')
    FULL = (1<<n) - 1

    dp = [[INF]*n for _ in range(1<<n)]
    parent = [[-1]*n for _ in range(1<<n)]

    dp[1][0] = 0

    for mask in range(1<<n):
        for u in range(n):
            if not (mask & (1<<u)): continue
            for v in range(n):
                if mask & (1<<v): continue
                new_mask = mask | (1<<v)
                new_cost = dp[mask][u] + dist[u][v]
                if new_cost < dp[new_mask][v]:
                    dp[new_mask][v] = new_cost
                    parent[new_mask][v] = u

    best_len = INF
    last = -1
    for u in range(1, n):
        cost = dp[FULL][u] + dist[u][0]
        if cost < best_len:
            best_len = cost
            last = u

    tour = []
    mask = FULL
    while last != -1:
        tour.append(last)
        prev = parent[mask][last]
        mask ^= (1<<last)
        last = prev
    tour.reverse()

    return best_len, tour


# TSP output
cities = [(0, 0), (1, 5), (5, 2), (6, 6)]
dist = build_dist_matrix(cities)

print("TSP Brute Force:", tsp_brute_force(dist))
print("TSP Nearest Neighbour:", tsp_nearest_neighbour(dist))
print("TSP Held Karp:", tsp_held_karp(dist))# -------- TASK 1 --------
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# -------- TASK 2 --------
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)


# -------- TASK 3 --------
def knapsack_01(weights, values, W):
    n = len(weights)
    dp = [[0]*(W+1) for _ in range(n+1)]
    for i in range(1, n+1):
        for w in range(W+1):
            if weights[i-1] <= w:
                dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
    return dp[n][W]


# -------- TASK 4 --------
import functools

def fib_naive(n):
    if n <= 1:
        return n
    return fib_naive(n-1) + fib_naive(n-2)

@functools.lru_cache(None)
def fib_memo(n):
    if n <= 1:
        return n
    return fib_memo(n-1) + fib_memo(n-2)

def fib_dp(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, a+b
    return b


# -------- TASK 5 --------
import itertools
import math

def euclidean_dist(c1, c2):
    return math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2)

def build_dist_matrix(cities):
    n = len(cities)
    dist = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dist[i][j] = euclidean_dist(cities[i], cities[j])
    return dist

def tour_length(tour, dist):
    return sum(dist[tour[i]][tour[i+1]] for i in range(len(tour)-1)) + dist[tour[-1]][tour[0]]

def tsp_brute_force(dist):
    n = len(dist)
    cities = list(range(1, n))
    best_len = float('inf')
    best_tour = None
    for perm in itertools.permutations(cities):
        tour = [0] + list(perm)
        length = tour_length(tour, dist)
        if length < best_len:
            best_len = length
            best_tour = tour
    return best_len, best_tour

def tsp_nearest_neighbour(dist, start=0):
    n = len(dist)
    visited = [False]*n
    tour = [start]
    visited[start] = True
    for _ in range(n-1):
        current = tour[-1]
        nearest = min((j for j in range(n) if not visited[j]), key=lambda j: dist[current][j])
        tour.append(nearest)
        visited[nearest] = True
    return tour_length(tour, dist), tour

def tsp_held_karp(dist):
    n = len(dist)
    INF = float('inf')
    FULL = (1<<n) - 1

    dp = [[INF]*n for _ in range(1<<n)]
    parent = [[-1]*n for _ in range(1<<n)]

    dp[1][0] = 0

    for mask in range(1<<n):
        for u in range(n):
            if not (mask & (1<<u)): continue
            for v in range(n):
                if mask & (1<<v): continue
                new_mask = mask | (1<<v)
                new_cost = dp[mask][u] + dist[u][v]
                if new_cost < dp[new_mask][v]:
                    dp[new_mask][v] = new_cost
                    parent[new_mask][v] = u

    best_len = INF
    last = -1
    for u in range(1, n):
        cost = dp[FULL][u] + dist[u][0]
        if cost < best_len:
            best_len = cost
            last = u

    tour = []
    mask = FULL
    while last != -1:
        tour.append(last)
        prev = parent[mask][last]
        mask ^= (1<<last)
        last = prev
    tour.reverse()

    return best_len, tour