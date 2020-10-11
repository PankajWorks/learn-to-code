"""
Problem:
  Implement a queue from 2 stacks
Constraints:
  Do we want the method to be enqueue and dequeue? Yes
  Can we assume we have a stack class which cna be reused? Yes
  Can we push a none value to stack? No
  Can we assume it fits in memory? Yes
TestCases:
  Enqueue and dequeue on empty stack
  Enqueue and dequeue on non-empty stack
  Multiple enqueue in a row
  Multiple dequeue in a row
  Enqueue after a dequeue
  Dequeue after an enqueue
Algorithm:
  2 stacks
  Left for enqueue
  Right for dequeue
  To prevent multiple dequeue calls from needlessly shifting elements around 
  between the stacks, we'll shift elements in a lazy manner.

  Enqueue :
    If right stack is not empty Shift the elements of the right stack to the left stack
    Push the data to the left stack
    Complexity : O(n) O(n)
  Dequeue :
    If the left stack is not empty Shift the elements of the left stack to the right stack
    Pop from the right stack and return the data
  Shift Stacks:
    While the source stack has elements:
    Pop from the source stack and push the data to the destination stack
"""
import unittest

class Stack(object):
  def __init__(self):
    self._items = []

  def push(self, item):
    self._items.append(item)

  def pop(self):
    if not self.is_empty():
      return self._items.pop()
    else:
      return IndexError('Invalid pop: stack is empty.')

  def is_empty(self):
    return True if len(self._items) == 0 else False
  
  def peek(self):
    if not self.is_empty():
      return self._items[-1]
    else:
      return IndexError('Invalid peek: stack is empty.')
  
  def __repr__(self):
    return "[{}]".format(", ".join(map(str, self._items)))
  def __iter__(self):
    for i in self._items:
      yield i
      
class QueueFromStacks(object):
  def __init__(self):
    self.left_stack = Stack()
    self.right_stack = Stack()
  
  def shift_stacks(self, source, destination):
    while source.peek() is not None:
      destination.push(source.pop())
  
  def enqueue(self, data):
    self.shift_stacks(self.right_stack, self.left_stack)
    self.left_stack.push(data)
  
  def dequeue(self):
    self.shift_stacks(self.left_stack, self.right_stack)
    return self.right_stack.pop()

class TestQueueFromStacks(unittest.TestCase):
  def test_queue_from_stacks(self):
    print('Test: Dequeue on empty stack')
    queue = QueueFromStacks()
    self.assertEqual(queue.dequeue(), None)
    
    print('Test: Enqueue on empty stack')
    print('Test: Enqueue on non-empty stack')
    print('Test: Multiple enqueue in a row')
    
    num_items = 3
    for i in range(0, num_items):
      queue.enqueue(i)
    print('Test: Dequeue on non-empty stack')
    print('Test: Dequeue after an enqueue')
    self.assertEqual(queue.dequeue(), 0)

    print('Test: Multiple dequeue in a row')
    self.assertEqual(queue.dequeue(), 1)
    self.assertEqual(queue.dequeue(), 2)

    print('Test: Enqueue after a dequeue')
    queue.enqueue(5)
    self.assertEqual(queue.dequeue(), 5)
    print('Success: test_queue_from_stacks')

def main():
  test = TestQueueFromStacks()
  test.test_queue_from_stacks()


if __name__ == '__main__':
  main()