"""
Problem :
  Sort a stack. You can use another stack as a buffer.
Constraints:
  When sorted, should the largest element be at the top or bottom? Top
  Can you have duplicate values like 5, 5? Yes
  Can we assume we already have a stack class that can be used for this problem? Yes
  Can we assume this fits memory? Yes
TestCases:
  Empty stack -> None
  One element stack
  Two or more element stack (general case)
  Already sorted stack
Algorithm:
  Our buffer will hold elements in reverse sorted order, smallest at the top
  Store the current top element in a temp variable
  While stack is not empty
    While buffer is not empty or buffer top is > than temp
      Move buffer top to stack
    Move temp to top of buffer
  return buffer
  
  Complexity : Time : O(n^2) Space : O(n)

"""

from stack import Stack
from random import randint
import unittest

class MyStack(Stack):
  def sort(self):
    buff = MyStack()
    while not self.is_empty():
      temp = self.pop()
      while not buff.is_empty() and temp < buff.peek():
        self.push(buff.pop())
      buff.push(temp)
    return buff


class TestSortStack(unittest.TestCase):
  def get_sorted_stack(self, stack, numbers):
    for x in numbers:
      stack.push(x)
    sorted_stack = stack.sort()
    return sorted_stack

  def test_sort_stack(self, stack):
    print('Test: Empty stack')
    sorted_stack = self.get_sorted_stack(stack, [])
    self.assertEqual(sorted_stack.pop(), None)

    print('Test: One element stack')
    sorted_stack = self.get_sorted_stack(stack, [1])
    self.assertEqual(sorted_stack.pop(), 1)

    print('Test: Two or more element stack (general case)')
    num_items = 10
    numbers = [randint(0, 10) for x in range(num_items)]
    sorted_stack = self.get_sorted_stack(stack, numbers)
    sorted_numbers = []
    for _ in range(num_items):
        sorted_numbers.append(sorted_stack.pop())
    self.assertEqual(sorted_numbers, sorted(numbers, reverse=True))

    print('Success: test_sort_stack')


def main():
  test = TestSortStack()
  test.test_sort_stack(MyStack())


if __name__ == '__main__':
  main()
        