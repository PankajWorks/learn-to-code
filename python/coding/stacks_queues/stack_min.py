"""
Problem:
  Implement a stack with push, pop, and min methods running O(1) time.
  Can we assume this is a stack of ints?  Yes
  Can we assume the input values for push are valid? Yes
  If we call this function on an empty stack, can we return sys.maxsize?Yes
  Can we assume we already have a stack class that can be used for this problem?Yes
  Can we assume this fits memory?Yes
TestCases:
  Push/Pop an empty stack
  Push/pop non empty stack
  Min on empty stack
  Min on non-empty stack
Algorithm
  We'll use a second stack to keep track of min values.
  Min:
    If the second stack is empty, return an error code (max int value)
    Else, return the top of the stack, without popping it
  Complexity : O(1) O(1)
  Push:
    Push the data
    If data is less than min then Push data to second stack
  Pop
    Pop the data
    If the data is equal to min Pop the top of the second stack
    return the data

"""

from stack import Stack
import sys
import unittest

class StackMin(Stack):
  def __init__(self, top=None):
    super(StackMin, self).__init__(top)
    self.stack_of_mins = Stack()
  def minimum(self):
    if self.stack_of_mins.top is None:
      return sys.maxsize
    else:
      return self.stack_of_mins.peek()
  
  def push(self, data):
    super(StackMin,self).push(data)
    if data < self.minimum():
      self.stack_of_mins.push(data)
  
  def pop(self):
    data = super(StackMin, self).pop()
    if data == self.minimum():
      self.stack_of_mins.pop()
    return data

class TestStackMin(unittest.TestCase):
  def test_stack_min(self):
    print('Test: Push on empty stack, non-empty stack')
    stack = StackMin()
    stack.push(5)
    self.assertEqual(stack.peek(), 5)
    self.assertEqual(stack.minimum(), 5)
    stack.push(1)
    self.assertEqual(stack.peek(), 1)
    self.assertEqual(stack.minimum(), 1)
    stack.push(3)
    self.assertEqual(stack.peek(), 3)
    self.assertEqual(stack.minimum(), 1)
    stack.push(0)
    self.assertEqual(stack.peek(), 0)
    self.assertEqual(stack.minimum(), 0)

    print('Test: Pop on non-empty stack')
    self.assertEqual(stack.pop(), 0)
    self.assertEqual(stack.minimum(), 1)
    self.assertEqual(stack.pop(), 3)
    self.assertEqual(stack.minimum(), 1)
    self.assertEqual(stack.pop(), 1)
    self.assertEqual(stack.minimum(), 5)
    self.assertEqual(stack.pop(), 5)
    self.assertEqual(stack.minimum(), sys.maxsize)

    print('Test: Pop empty stack')
    self.assertEqual(stack.pop(), None)

    print('Success: test_stack_min')
    
def main():
  test = TestStackMin()
  test.test_stack_min()


if __name__ == '__main__':
  main()