import numpy as np
import matplotlib.pyplot as plt # 3.4.3
import math

def fast_hist(array, bins):
    min_val = min(array)
    max_val = max(array)
    delta = (max_val - min_val) / bins
    
    labels = list(np.arange(min_val + delta / 2, max_val, delta))
    n = len(labels)
    
    counts = [0] * (n)
    for value in array:
        counts[min(math.floor((value - min_val) / delta), n - 1)] += 1
    
    return (counts, labels)

def check_fast_hist():
    array = np.random.randint(10, size=10)
    print(array)

    plt.hist(array, bins=len(set(array)), rwidth=0.5)
    plt.show()

    value_counts, bins_names = fast_hist(array, bins=len(set(array)))
    plt.bar(bins_names, value_counts, color='red')
    plt.show()

