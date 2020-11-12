"""
Design a datastructure that follows the constraints of a LRU Cache
Implement the LRUCache class
  LRUCache(int capacity) Initialize the LRU cache with positive size capacity.
  int get(int key) Return the value of the key if the key exists, otherwise return -1
  void put(int key, int value) Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache. If the number of keys exceeds the capacity from this operation, evict the least recently used key.

Follow up
  Could you do get and put in O(1) time complexity?
  Example 1:
  Input
    ["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
    [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
  Output
    [null, null, null, 1, null, -1, null, -1, 3, 4]
  Explanation
    LRUCache lRUCache = new LRUCache(2);
    lRUCache.put(1, 1); // cache is {1=1}
    lRUCache.put(2, 2); // cache is {1=1, 2=2}
    lRUCache.get(1);    // return 1
    lRUCache.put(3, 3); // LRU key was 2, evicts key 2, cache is {1=1, 3=3}
    lRUCache.get(2);    // returns -1 (not found)
    lRUCache.put(4, 4); // LRU key was 1, evicts key 1, cache is {4=4, 3=3}
    lRUCache.get(1);    // return -1 (not found)
    lRUCache.get(3);    // return 3
    lRUCache.get(4);    // return 4
Constraints:
  1 <= capacity <= 3000
  0 <= key <= 3000
  0 <= value <= 10 pow 4
  At most 3 * 10 pow 4 calls will be made to get and put.
"""

class LRUCache(object):
  def __init__(self, msize):
    self.size = msize
    self.cache = {}
    self.next, self.before = {}, {}
    self.head, self.tail = "#", "$"
    self.connect(self.head, self.tail)
  
  def connect(self, a, b):
    self.next[a], self.before[b] = b, a
  
  def delete(self, key):
    self.connect(self.before[key], self.next[key])
    del self.before[key], self.next[key], self.cache[key]
  
  def append(self, k, v):
    self.cache[k] = v
    self.connect(self.before[self.tail], k)
    self.connect(k, self.tail)
    if len(self.cache) > self.size:
      self.delete(self.next[self.head])
  
  def get(self, key):
    if key not in self.cache: return -1
    val = self.cache[key]
    self.delete(key)
    self.append(key, val)
    return val