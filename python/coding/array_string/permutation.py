"""
Problem: 
  Determine if a string is a permutation of another string.
Constraints
  Can we assume the string is ASCII?Yes
  Note: Unicode strings could require special handling depending on your language
  Is whitespace important?Yes
  Is this case sensitive? 'Nib', 'bin' is not a match?Yes
  Can we use additional data structures?Yes
  Can we assume this fits in memory?Yes
Test Cases:
  One or more None inputs -> False
  One or more empty strings -> False
  'Nib', 'bin' -> False
  'act', 'cat' -> True
  'a ct', 'ca t' -> True
  'dog', 'doggo' -> False
Algorithm: 
  Compare Sorted Strings
  Permutations contain the same strings but in different orders. This approach could be slow for large strings due to sorting.

  Sort both strings
  If both sorted strings are equal
    return True
  Else
    return False
  Complexity:

  Time: O(n log n) from the sort, in general
  Space: O(n)
"""

# Compare Sorted Strings
class Permutations(object):

  def is_permutation(self, str1, str2):
    if str1 is None or str2 is None:
      return False
    return sorted(str1) == sorted(str2)


from collections import defaultdict

# We'll keep a hash map (dict) to keep track of characters we encounter.

# Steps:

# Scan each character
# For each character in each string:
# If the character does not exist in a hash map, add the character to a hash map
# Else, increment the character's count
# If the hash maps for each string are equal
# Return True
# Else
# Return False
class PermutationsAlt(object):
  def is_permutation(self, str1, str2):
    if str1 is None or str2 is None:
      return False
    if len(str1) != len(str2):
      return False
    unique_counts1 = defaultdict(int)
    unique_counts2 = defaultdict(int)
    for char in str1:
      unique_counts1[char] += 1
    for char in str2:
      unique_counts2[char] += 1
    return unique_counts1 == unique_counts2

import unittest


class TestPermutation(unittest.TestCase):

  def test_permutation(self, func):
    self.assertEqual(func(None, 'foo'), False)
    self.assertEqual(func('', 'foo'), False)
    self.assertEqual(func('Nib', 'bin'), False)
    self.assertEqual(func('act', 'cat'), True)
    self.assertEqual(func('a ct', 'ca t'), True)
    self.assertEqual(func('dog', 'doggo'), False)
    print('Success: test_permutation')


def main():
  test = TestPermutation()
  permutations = Permutations()
  test.test_permutation(permutations.is_permutation)
  try:
    permutations_alt = PermutationsAlt()
    test.test_permutation(permutations_alt.is_permutation)
  except NameError:
    # Alternate solutions are only defined
    # in the solutions file
    pass


if __name__ == '__main__':
  main()
    