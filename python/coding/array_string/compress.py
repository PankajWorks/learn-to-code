"""
Problem:
  Compress a string such that 'AAABCCDDDD' becomes 'A3BC2D4'. Only compress the string if it saves space.
Constraints:
  Can we assume the string is ASCII?Yes
    Note: Unicode strings could require special handling depending on your language
  Is this case sensitive? Yes
  Can we use additional data structures? Yes
  Can we assume this fits in memory? Yes
Test Cases:
  None -> None
  '' -> ''
  'AABBCC' -> 'AABBCC'
  'AAABCCDDDD' -> 'A3BC2D4'
Algorithm:
  For each char in string
    If char is the same as last_char, increment count
    Else:
      Append last_char and count to compressed_string
      last_char = char
      count = 1
  Append last_char and count to compressed_string
  If the compressed string size is < string size
    Return compressed string
  Else:
    Return string
Complexity: Time : O(n) Space : O(n)     
"""
class CompressString(object):
  def compress(self, string):
    if string is None or not string:
      return string
    result = ''
    prev_char = string[0]
    count = 0
    for char in string:
      if char == prev_char:
        count += 1
      else:
        result += self._calc_partial_result(prev_char, count)
        prev_char = char
        count = 1
    result += self._calc_partial_result(prev_char, count)
    return result if len(result) < len(string) else string
  
  def _calc_partial_result(self, prev_char, count):
    return prev_char + (str(count) if count > 1 else '')

# Test
import unittest
class TestCompress(unittest.TestCase):
  def test_compress(self, func):
    self.assertEqual(func(None), None)
    self.assertEqual(func(''), '')
    self.assertEqual(func('AABBCC'), 'AABBCC')
    self.assertEqual(func('AAABCCDDDDE'), 'A3BC2D4E')
    self.assertEqual(func('BAAACCDDDD'), 'BA3C2D4')
    self.assertEqual(func('AAABAACCDDDD'), 'A3BA2C2D4')
    print('Success: test_compress')


def main():
  test = TestCompress()
  compress_string = CompressString()
  test.test_compress(compress_string.compress)

if __name__ == '__main__':
    main()