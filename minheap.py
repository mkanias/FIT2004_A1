class MinHeap:
    def __init__(self):
        self.heap = []

    def parent(self, i):
        return (i - 1) // 2 # O(1)

    def left_child(self, i): 
        return 2 * i + 1 # O(1)

    def right_child(self, i): 
        return 2 * i + 2 # O(1)

    def insert(self, value, priority):
        """
        Function description: Inserts a new element into the heap with the given priority.
        
        Input:
            value: The value to insert.
            priority: The priority of the value.
        
        Output: None
        
        Time complexity: O(log N)
        
        Time complexity analysis: Inserting an element involves appending it to the end of the list (O(1)) and then performing a heapify-up operation (O(log N)).
        
        Space complexity: O(1)
        
        Space complexity analysis: The space used is proportional to the size of the heap, but this does not count towards auxiliary space complexity.
        """
        # Insert the new element at the end of the heap
        self.heap.append((value, priority)) # O(1)
        # Move the new element to its correct position
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self):
        """
        Function description: Extracts and returns the minimum element from the heap.
        
        Input: None
        
        Output:
            The minimum element (root of the heap).
        
        Time complexity: O(log N)
        
        Time complexity analysis: Extracting the minimum involves replacing the root with the last element (O(1)) and then performing a heapify-down operation (O(log N)).
        
        Space complexity: O(1)
        
        Space complexity analysis: The space used is for the root element, and does not count towards auxiliary space complexity.
        """
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

    def _heapify_up(self, i):
        """
        Function description: Moves the element at index i up the heap to its correct position to maintain the heap property.
        
        Input:
            i: The index of the element to move up.
        
        Output: None
        
        Time complexity: O(log N)
        
        Time complexity analysis: The process of moving an element up involves potentially swapping it with its parent multiple times, which is logarithmic in terms of the number of elements.
        
        Space complexity: O(1)
        
        Space complexity analysis: No additional space is used beyond the existing heap.
        """
        # Move the element at index i up the heap to its correct position
        # Checking if the index is greater than 0 and if the parent of our current priority is greater than the current priority itself 
        # This ensures we are maintaining the minheap property.

        while i > 0 and self.heap[self.parent(i)][1] > self.heap[i][1]: # O(log(N))
            # Swapping with parent if the current element's priority is smaller
            self.heap[i], self.heap[self.parent(i)] = self.heap[self.parent(i)], self.heap[i] # O(1)
            i = self.parent(i)

    def _heapify_down(self, i):
        """
        Function description: Moves the element at index i down the heap to its correct position to maintain the heap property.
        
        Input:
            i: The index of the element to move down.
        
        Output: None
        
        Time complexity: O(log N)
        
        Time complexity analysis: The process of moving an element down involves potentially swapping it with its children multiple times, which is logarithmic in terms of the number of elements.
        
        Space complexity: O(1)
        
        Space complexity analysis: No additional space is used beyond the existing heap.
        """
        # Move the element at index i down the heap to its correct position
        current_smallest_index = i
        left_child_index = self.left_child(i)
        right_child_index = self.right_child(i)

        # Checking if left_child_index and right_child_index children exist and if so checking if their value is smaller than our current smallest value
        # If both these conditions are true then we swap these two indices so that minheap is maintained

        if left_child_index < len(self.heap) and self.heap[left_child_index][1] < self.heap[current_smallest_index][1]:
            current_smallest_index = left_child_index # O(1)

        if right_child_index < len(self.heap) and self.heap[right_child_index][1] < self.heap[current_smallest_index][1]:
            current_smallest_index = right_child_index # O(1)

        if current_smallest_index != i:
            # Swap and continue heapifying down
            self.heap[i], self.heap[current_smallest_index] = self.heap[current_smallest_index], self.heap[i]
            self._heapify_down(current_smallest_index) # recursive call O(log(N))

    def is_empty(self):
        return len(self.heap) == 0