
# 2.1 Video Peaks of Interest
def find_peaks(data):
    S = len(data)
    peaks = []
    if S == 0:
        return peaks
    if S == 1:
        if data[0] > 0:
            peaks.append(0)
        return peaks

    for i in range(S):
        if data[i] == 0:
            continue
        is_left_valid = (i == 0) or (data[i] > data[i - 1])
        is_right_valid = (i == S - 1) or (data[i] > data[i + 1])
        if is_left_valid and is_right_valid:
            peaks.append(i)
    return peaks


# 2.2 Priority Queue based on Document K
class PriorityQueue:
    def __init__(self, capacity=10):
        self.N = 0
        self.keys = [None] * (capacity + 1)
        self.values = [None] * (capacity + 1)

    def less(self, i, j):

        return self.keys[i] < self.keys[j]

    def exchange(self, i, j):
        self.keys[i], self.keys[j] = self.keys[j], self.keys[i]
        self.values[i], self.values[j] = self.values[j], self.values[i]

    def swim(self, k):

        while k > 1 and self.less(k // 2, k):
            parent = k // 2
            self.exchange(k, parent)
            k = parent

    def sink(self, k):

        while 2 * k <= self.N:
            j = 2 * k
            if j < self.N and self.less(j, j + 1):
                j += 1
            if not self.less(k, j):
                break
            self.exchange(k, j)
            k = j

    def insert(self, key, value):
        self.N += 1
        if self.N >= len(self.keys):
            self.keys.extend([None] * len(self.keys))
            self.values.extend([None] * len(self.values))
        self.keys[self.N] = key
        self.values[self.N] = value
        self.swim(self.N)

    def del_max(self):

        if self.N == 0:
            return None, None
        max_k = self.keys[1]
        max_v = self.values[1]
        self.exchange(1, self.N)
        self.N -= 1
        self.sink(1)
        return max_k, max_v


def merge_pqs(pq1, pq2):

    N = pq1.N + pq2.N
    merged = PriorityQueue(capacity=N)
    merged.N = N

    for i in range(1, pq1.N + 1):
        merged.keys[i] = pq1.keys[i]
        merged.values[i] = pq1.values[i]

    for i in range(1, pq2.N + 1):
        merged.keys[pq1.N + i] = pq2.keys[i]
        merged.values[pq1.N + i] = pq2.values[i]
    for k in range(N // 2, 0, -1):
        merged.sink(k)

    return merged


def run_tests():
    print("--- Running tests for Problem 2.1 ---")
    assert find_peaks([0, 0, 0, 0, 0]) == []
    print("Test 1 passed: [0,0,0,0,0] -> []")

    assert find_peaks([0, 50, 100, 50, 0]) == [2]
    print("Test 2 passed: [0,50,100,50,0] -> [2]")

    assert find_peaks([75, 0, 0, 0, 75]) == [0, 4]
    print("Test 3 passed: [75,0,0,0,75] -> [0, 4]")

    print("\n--- Running tests for Problem 2.2 ---")
    pq1 = PriorityQueue()
    for k, v in [(10, "A"), (30, "B"), (20, "C")]:
        pq1.insert(k, v)

    pq2 = PriorityQueue()
    for k, v in [(50, "D"), (5, "E"), (40, "F"), (25, "G")]:
        pq2.insert(k, v)

    merged = merge_pqs(pq1, pq2)
    assert merged.N == 7

    extracted = []
    while merged.N > 0:
        extracted.append(merged.del_max())

    expected_keys = [50, 40, 30, 25, 20, 10, 5]
    actual_keys = [item[0] for item in extracted]
    assert actual_keys == expected_keys, f"Expected {expected_keys}, got {actual_keys}"
    print(f"Test passed: Extracted elements in max-order: {actual_keys}")
    print("\nAll tests passed successfully!")


if __name__ == "__main__":
    run_tests()
