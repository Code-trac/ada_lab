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