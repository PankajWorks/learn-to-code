"""
Problem:
  Sort an array of strings so all anagrams are next to each other.
Constraints:
  Are there any other sorting requirements other than the grouping of anagrams? No
  Can we assume the inputs are valid? No
  Can we assume this fits memory? Yes
TestCase:
  None -> Exception
  [] -> []
  General case
  Input: ['ram', 'act', 'arm', 'bat', 'cat', 'tab']
  Result: ['arm', 'ram', 'act', 'cat', 'bat', 'tab']

Algorithm:
  Sort the chars for each item:
  Use a map of sorted chars to each item to group anagrams:
  
  Complexity:
    Time: O(k * n), due to the modified bucket sort
    Space: O(n)
"""

from collections import OrderedDict
import unittest

class Anagram(object):
  def group_anagrams(self, items):
    if items is None:
      raise TypeError('items cannot be None')
    if not items:
      return items
    anagram_map = OrderedDict()
    for item in items:
      # Use a tuple, which is hashable and serves as the key in anagram_map
      sorted_chars = tuple(sorted(item))
      if sorted_chars in anagram_map:
        anagram_map[sorted_chars].append(item)
      else:
        anagram_map[sorted_chars] = [item]
    result = []
    for value in anagram_map.values():
      result.extend(value)
    return result

class TestAnagrams(unittest.TestCase):
  def test_group_anagrams(self):
    anagram = Anagram()
    self.assertRaises(TypeError, anagram.group_anagrams, None)
    data = ['ram', 'act', 'arm', 'bat', 'cat', 'tab']
    expected = ['ram', 'arm', 'act', 'cat', 'bat', 'tab']
    self.assertEqual(anagram.group_anagrams(data), expected)

    print('Success: test_group_anagrams')


def main():
  test = TestAnagrams()
  test.test_group_anagrams()


if __name__ == '__main__':
  main()