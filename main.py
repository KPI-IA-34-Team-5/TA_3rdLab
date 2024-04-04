from io import TextIOWrapper
import statistics
import sys
from loguru import logger

# https://github.com/Delgan/loguru/issues/138#issuecomment-1491571574
# min_level = "DEBUG"
min_level = "INFO"

def min_level_filter(record):
    return record["level"].no >= logger.level(min_level).no

logger.remove()
logger.add(sys.stderr, format="[{time:HH:mm:ss.SSS} | <level>{level: <8}</level>] {message}", filter=min_level_filter)

def partition(array, low, high):
    counter = 0
    pivot = array[high]
    i = low - 1
    for j in range(low, high):
        if array[j] <= pivot:
            i = i + 1
            (array[i], array[j]) = (array[j], array[i])
        counter = counter + 1
    (array[i + 1], array[high]) = (array[high], array[i + 1])
    return i + 1, counter
 
 
def quick_sort(array, low=0, high=None):
    if high == None:
        high = len(array) - 1
    counter_1 = 0
    counter_2 = 0
    counter_3 = 0
    if low < high:
        pi, counter_1 = partition(array, low, high)
        counter_2 = quick_sort(array, low, pi - 1)
        counter_3 = quick_sort(array, pi + 1, high)
    return counter_1 + counter_2 + counter_3


def quick_sort_modified(array):
    if len(array) <= 3:
        return quick_sort(array)
    a = array[0]
    b = array[len(array)-1]
    c = array[len(array) // 2]
    
    pivot = statistics.median([a,b,c])
    
    less = []
    equal = []
    greater = []
    
    counter = 0
    
    for x in array:
        if x == pivot:
            equal.append(x)
            counter = counter + 1
            continue
        if x < pivot:
            less.append(x)
            counter = counter + 2
            continue
        greater.append(x)
        counter = counter + 2    
    return counter + quick_sort_modified(less) + quick_sort_modified(greater)

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
    logger.info("Starting to work..")
    inp = file_reader(open("./input.txt"))
    logger.debug("Working with quicksort..")
    qs_out = quick_sort(list(inp))
    logger.debug("Working with quicksort modified..")
    qs_m_out = quick_sort_modified(list(inp))
    logger.info("Finsihed working. Writing to file.")
    out = str(qs_out) + " " + str(qs_m_out)
    f = open("./output.txt", "w")
    f.write(out)
    f.close()
