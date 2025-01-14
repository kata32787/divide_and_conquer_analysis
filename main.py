import random
import time
from memory_profiler import memory_usage

# Quick Sort Implementation
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# Merge Sort Implementation
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    while left and right:
        if left[0] <= right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    result.extend(left or right)
    return result

# Performance Testing
def measure_performance():
    datasets = {
        "sorted": list(range(1000)),
        "reverse_sorted": list(range(1000, 0, -1)),
        "random": [random.randint(0, 1000) for _ in range(1000)],
    }
    
    results = []
    for key, data in datasets.items():
        print(f"\nDataset: {key}")
        for algo, func in [("Quick Sort", quick_sort), ("Merge Sort", merge_sort)]:
            # Measure execution time
            start = time.time()
            func(data.copy())  # Use a copy to avoid side effects
            end = time.time()

            # Measure memory usage
            mem_usage = memory_usage((func, (data.copy(),)), max_usage=True)

            print(f"{algo} | Time: {end - start:.6f} seconds | Memory: {mem_usage:.2f} MB")
            results.append((key, algo, end - start, mem_usage))
    
    return results

if __name__ == "__main__":
    results = measure_performance()
import csv

def save_to_csv(results):
    with open('performance_metrics.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Dataset", "Algorithm", "Execution Time (seconds)", "Memory Usage (MB)"])
        writer.writerows(results)

if __name__ == "__main__":
    results = measure_performance()
    save_to_csv(results)
import pandas as pd
import matplotlib.pyplot as plt

def generate_graphs():
    # Read the CSV file
    data = pd.read_csv("performance_metrics.csv")

    # Group data by Dataset and Algorithm
    datasets = data["Dataset"].unique()
    algorithms = data["Algorithm"].unique()

    # Generate bar graphs for execution time
    for dataset in datasets:
        subset = data[data["Dataset"] == dataset]
        plt.bar(subset["Algorithm"], subset["Execution Time (seconds)"], color=["blue", "green"])
        plt.title(f"Execution Time for {dataset} Dataset")
        plt.xlabel("Algorithm")
        plt.ylabel("Time (seconds)")
        plt.savefig(f"{dataset}_execution_time.png")  # Save graph as an image
        plt.show()

    # Generate bar graphs for memory usage
    for dataset in datasets:
        subset = data[data["Dataset"] == dataset]
        plt.bar(subset["Algorithm"], subset["Memory Usage (MB)"], color=["blue", "green"])
        plt.title(f"Memory Usage for {dataset} Dataset")
        plt.xlabel("Algorithm")
        plt.ylabel("Memory (MB)")
        plt.savefig(f"{dataset}_memory_usage.png")  # Save graph as an image
        plt.show()

if __name__ == "__main__":
    # Generate graphs
    generate_graphs()
