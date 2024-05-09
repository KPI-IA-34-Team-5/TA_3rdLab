from io import TextIOWrapper
import statistics
import sys
import os
from loguru import logger

# https://github.com/Delgan/loguru/issues/138#issuecomment-1491571574
# min_level = "DEBUG"
min_level = "INFO"

def min_level_filter(record):
    return record["level"].no >= logger.level(min_level).no

logger.remove()
logger.add(sys.stderr, format="[{time:HH:mm:ss.SSS} | <level>{level: <8}</level>] {message}", filter=min_level_filter)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    count = 0
    for j in range(low, high):
        count += 1
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1, count

def quick_sort(arr, low, high):
    if low < high:
        pi, local_count = partition(arr, low, high)
        left_count = quick_sort(arr, low, pi - 1)
        right_count = quick_sort(arr, pi + 1, high)
        return local_count + left_count + right_count
    return 0

def quick_sort_modified(arr):
    count = 0
    def partition_mod(arr, low, high):
        mid = (low + high) // 2
        pivot_candidates = [(arr[low], low), (arr[mid], mid), (arr[high], high)]
        pivot_candidates.sort()
        median_value, median_index = pivot_candidates[1]
        arr[median_index], arr[high] = arr[high], arr[median_index]
        return partition(arr, low, high)
    def sort(arr, low, high):
        nonlocal count
        if low < high:
            pi, local_count = partition_mod(arr, low, high)
            count += local_count
            sort(arr, low, pi - 1)
            sort(arr, pi + 1, high)
    sort(arr, 0, len(arr) - 1)
    return count

def file_reader(file: TextIOWrapper):
    lines = file.readlines()
    info = int(lines[0])
    arr = []
    if len(lines) != info+1:
        raise Exception("Invalid input was provided. The length of the array is not correct.") 
    for i in range(1,info+1):
        inputting = int(lines[i])
        if (inputting in arr):
            raise Exception("Invalid input was provided. Duplicates were found.") 
        arr.append(inputting)
    return arr

if __name__ == "__main__":
    directory = os.getcwd() + "\\input"

    for filename in os.listdir(directory):
        if filename.startswith('input'):
            with open(directory + "\\" + filename, 'r') as file:
                logger.info(f"Starting to work with {filename}")
                inp = file_reader(file)
                logger.debug("Working with quicksort..")
                qs_out = quick_sort(list(inp), 0, len(inp) - 1)
                logger.debug("Working with quicksort modified..")
                qs_m_out = quick_sort_modified(list(inp))
                logger.info(f"Finsihed working. Writing to file {filename.replace('input', 'output')}.")
                out = str(qs_out) + " " + str(qs_m_out)
                with open(os.getcwd() + "\\output\\" + filename.replace('input', 'output'), "w") as f:
                    f.write(out)