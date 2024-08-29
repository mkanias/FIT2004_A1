class MinHeap:
    def __init__(self):
        self.heap = []

    def parent(self, i):
        return (i - 1) // 2

    def left_child(self, i):
        return 2 * i + 1

    def right_child(self, i):
        return 2 * i + 2

    def insert(self, value, priority):
        # Insert the new element at the end of the heap
        self.heap.append((value, priority))
        # Move the new element to its correct position
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self):
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        # The root of the heap (minimum element)
        root = self.heap[0]
        # Replace the root with the last element in the heap
        self.heap[0] = self.heap.pop()
        # Heapify down from the root to maintain the heap property
        self._heapify_down(0)

        return root

    def decrease_key(self, value, new_priority):
        # Find the index of the element to decrease its key
        index = None
        for i in range(len(self.heap)):
            if self.heap[i][0] == value:
                index = i
                break
        
        if index is None:
            return

        # Update the priority and heapify up to maintain the heap property
        self.heap[index] = (value, new_priority)
        self._heapify_up(index)

    def _heapify_up(self, i):
        # Move the element at index i up the heap to its correct position
        while i > 0 and self.heap[self.parent(i)][1] > self.heap[i][1]:
            # Swap with parent if the current element's priority is smaller
            self.heap[i], self.heap[self.parent(i)] = self.heap[self.parent(i)], self.heap[i]
            i = self.parent(i)

    def _heapify_down(self, i):
        # Move the element at index i down the heap to its correct position
        smallest = i
        left = self.left_child(i)
        right = self.right_child(i)

        if left < len(self.heap) and self.heap[left][1] < self.heap[smallest][1]:
            smallest = left

        if right < len(self.heap) and self.heap[right][1] < self.heap[smallest][1]:
            smallest = right

        if smallest != i:
            # Swap and continue heapifying down
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self._heapify_down(smallest)

    def is_empty(self):
        return len(self.heap) == 0