# Homework 8: ADJ Solutions

## 2.1 Design an Algorithm to Identify and List the Peaks of Interest During a Video

### Analysis
The goal of this problem is to identify all points in time (seconds) during a video that constitute "peaks of interest" to serve as candidates for thumbnail generation. The input is an array data of length S, where each index i represents the screen intensity at second i, taking values between 0 and 100.

To formulate a sound algorithmic solution, we state the following explicit assumptions:
1. **Absence of Interest:** An intensity value of 0 indicates an absence of interesting content. Therefore, any index with a value of 0 can never be considered a peak, regardless of its surrounding values.

2. **Local Peak Definition:** For an interior frame at index i (0 < i < S - 1), the index is a peak if and only if data[i] > 0, data[i] > data[i - 1], and data[i] > data[i + 1].

3. **Boundary Conditions:** Elements at the boundaries have only one neighbor. The initial second (i = 0) is considered a peak if data[0] > 0 and data[0] > data[1] (or simply data[0] > 0 if the video length S = 1). Similarly, the terminal second (i = S - 1) is a peak if data[S - 1] > 0 and data[S - 1] > data[S - 2].

4. **Plateaus:** If adjacent frames possess identical positive intensity values, neither strictly exceeds the other. In keeping with the goal of selecting distinct thumbnails and avoiding visual redundancy, only strictly dominant local maxima are treated as peaks.

### Design
The algorithm performs a single forward traversal over the data array from index 0 to S - 1. For each index, it verifies whether the intensity is strictly positive and strictly greater than any existing immediate neighbors. Qualifying indices are collected into a result list and returned.

```text
Algorithm findPeaks(data, S):
    peaks = empty list
    
    if S == 0:
        return peaks
        
    if S == 1:
        if data[0] > 0:
            peaks.append(0)
        return peaks

    for i from 0 to S - 1:
        if data[i] == 0:
            continue
            
        isLeftValid = (i == 0) or (data[i] > data[i - 1])
        isRightValid = (i == S - 1) or (data[i] > data[i + 1])
        
        if isLeftValid and isRightValid:
            peaks.append(i)
            
    return peaks
```

### Justification
- **Correctness:** The algorithm directly evaluates the strict local maximum criteria established in the analysis. By utilizing short-circuit conditional checks, boundary elements at indices 0 and S - 1 are evaluated against their single adjacent neighbor without causing out-of-bounds index errors. Zero-intensity frames are eliminated immediately. The algorithm correctly satisfies all expected outcomes from the prompt: returning an empty list for [0, 0, 0, 0, 0], returning [2] for [0, 50, 100, 50, 0], and returning [0, 4] for [75, 0, 0, 0, 75].

- **Time Complexity:** The algorithm runs in O(S) time. It performs a single pass through the array of length S, executing a constant number of comparison operations per index (O(1) work per iteration). This is asymptotically optimal, as inspecting every element at least once is strictly necessary (Ω(S)) to prevent omitting valid peaks.

- **Space Complexity:** The auxiliary space complexity is O(1), excluding the memory required to store the returned list of peak indices.

---

## 2.2 Design an Efficient Algorithm to Merge Two Priority Queues

### Analysis
The objective is to design an efficient procedure to merge two existing binary max-priority queues into a single valid priority queue. Document K specifies a standard 1-indexed binary heap structure maintaining parallel arrays `Key[] keys` and `Value[] values` with size `N`, alongside internal procedures `less(i, j)`, `swim(k)`, `sink(k)`, `insert(k, v)`, and `delMax()`.

We state the following explicit assumptions:
1. **Type Compatibility:** Both input priority queues store keys of identical, mutually comparable types and values of compatible types.

2. **Structural Compliance:** Both input priority queues (PQ_1 and PQ_2) strictly adhere to the 1-indexed binary heap implementation provided in document K, with respective entry counts N_1 and N_2.

3. **Queue Creation:** The merge operation produces a new priority queue containing all N = N_1 + N_2 elements, preserving the original data without corrupting the underlying representations.

### Design
A naive solution would extract all elements from one queue and insert them into the other, requiring O(N_2 log(N_1 + N_2)) time. To achieve optimal linear performance, we combine the entries into a newly allocated priority queue of capacity N = N_1 + N_2 and then apply bottom-up heap construction (Floyd's algorithm) using the existing `sink(k)` routine provided in document K.

```text
Algorithm mergePQs(PQ1, PQ2):
    // Step 1: Instantiate the merged priority queue
    mergedPQ = new PriorityQueue()
    N = PQ1.N + PQ2.N
    mergedPQ.N = N
    mergedPQ.keys = new Key[N + 1]
    mergedPQ.values = new Value[N + 1]

    // Step 2: Copy entries from PQ1 (indices 1 to N1)
    for i from 1 to PQ1.N:
        mergedPQ.keys[i] = PQ1.keys[i]
        mergedPQ.values[i] = PQ1.values[i]

    // Step 3: Copy entries from PQ2 (indices N1 + 1 to N)
    for i from 1 to PQ2.N:
        mergedPQ.keys[PQ1.N + i] = PQ2.keys[i]
        mergedPQ.values[PQ1.N + i] = PQ2.values[i]

    // Step 4: Bottom-up heapify using sink(k) defined in document K
    for k from floor(N / 2) down to 1:
        mergedPQ.sink(k)

    return mergedPQ
```

### Justification
- **Correctness:** In a 1-indexed binary heap of size N, all nodes at indices k > \lfloor N / 2 \rfloor are leaf nodes with no children, and therefore trivially satisfy the heap invariant. By iterating k backwards from \lfloor N / 2 \rfloor down to 1, each invocation of sink(k) operates on a node whose left and right subtrees are already valid binary heaps. Consequently, sink(k) successfully sifts down the key until the max-heap property is established for the subtree rooted at k. By mathematical induction, when k = 1 is processed, the entire array satisfies the binary max-heap property.

- **Time Complexity:**
  - Copying elements from PQ1 and PQ2 into the contiguous arrays requires \Theta(N1 + N2) operations.
  - Sifting down internal nodes depends on node height. A binary heap of size N contains at most \lceil N / 2^{h+1} \rceil nodes at height h. The total time spent in sink calls is proportional to \sum_{h=0}^{\lfloor \log_2 N \rfloor} \lceil \frac{N}{2^{h+1}} \rceil O(h) = O(N \sum_{h=0}^{\infty} \frac{h}{2^h}) = O(N).
  - Since N = N1 + N2, the overall runtime is O(N1 + N2) linear time. This is strictly superior to the naive repeated insertion approach.
- **Space Complexity:** The auxiliary space complexity is O(N1 + N2) to allocate the combined keys and values arrays for the newly merged priority queue.
