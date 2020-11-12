"""
Given an array, find the two indices that sum to a specific value.
Test Cases :
  None input -> TypeError
  [] -> ValueError
  [1, 3, 2, -7, 5], 7 -> [2, 4]

Algorithm:
BruteForce:
  For i in range(len(input)):
    For j in range(i+1, len(input)):
      if i + j == target return True
  return Falses

Optimised:
  Loop through each num in nums
    Calculate the cache_target = target - num
    put the cache_target in dictionary in not present.
    If present return because it will give answer.
Complexity:
  Time: O(n)
  Space: O(n)
"""

class Solution(object):
  def two_sum(self, nums, target):
    if nums is None or target is None:
      raise TypeError("nums or target cannot be None")
    if not nums:
      raise ValueError("nums cannot be empty")
    cache = {}
    for index, num in enumerate(nums):
      cache_taget = target - num
      if num in cache:
        return [cache[num], index]
      else:
        cache[cache_taget] = index
    return None

import unittest

class TestTwoSum(unittest.TestCase):
  def test_two_sum(self):
    solution = Solution()
    self.assertRaises(TypeError, solution.two_sum, None, None)
    self.assertRaises(ValueError, solution.two_sum, [], 0)
    target = 7
    nums = [1, 3, 2, -7, 5]
    expected = [2, 4]
    self.assertEqual(solution.two_sum(nums, target), expected)
    print('Success: test_two_sum')

def main():
  test = TestTwoSum()
  test.test_two_sum()


if __name__ == '__main__':
  main()  