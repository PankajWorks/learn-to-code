> Package sync provides basic synchronization primitives such as mutual exclusion locks. Other than the Once and WaitGroup types, most are intended for use by low-level library routines. Higher-level synchronization is better done via channels and communication.

- **sync.Mutex** : allows a mutual exclusion on a shared resource (no simultaneous access)
```go
mutex := &sync.Mutex{}

mutex.Lock()
// Update shared variable (e.g. slice, pointer on a structure, etc.)
mutex.Unlock()

// sync.Mutex cannot be copied (just like all the other primitives of sync package). If a structure has a sync field, it must be passed by pointer.
```
- sync.RWMutex : reader/writer mutex. It provides the same methods that we have just seen with Lock() and Unlock() (as both structures implement sync.Locker interface). Yet, it also allows concurrent reads using RLock() and RUnlock() methods:

```go
mutex := &sync.RWMutex{}

mutex.Lock()
// Update shared variable
mutex.Unlock()

mutex.RLock()
// Read shared variable
mutex.RUnlock()

// A sync.RWMutex allows either at least one reader or exactly one writer whereas a sync.Mutex allows exactly one reader or writer.
```

- **sync.WaitGroup** : way for a goroutine to wait for the completion of a collection of goroutines. sync.WaitGroup holds an internal counter. If this counter is equal to 0, the Wait() method returns immediately. Otherwise, it is blocked until the counter is 0. To increment the counter we have to use Add(int). To decrement it we can either use Done() (that will decrement by 1) or the same Add(int) method with a negative value.
In the following example, we will spin up eight goroutines and wait for their completion:

```go
wg := &sync.WaitGroup{}

for i := 0; i < 8; i++ {
  wg.Add(1)
  go func() {
    // Do something
    wg.Done()
  }()
}

wg.Wait()
// Continue execution
```

- **sync.Map** : is a concurrent version of Go map where we can
  - Add elements with Store(interface{}, interface{})
  - Retrieve elements with Load(interface) interface{}
  - Remove elements with Delete(interface{})
  - Retrieve or add an element if it did not exist before with LoadOrStore(interface{}, interface{}) (interface, bool). The returned bool is true if the key was present in the map before.
  - Iterate on the elements with Range.

```go
m := &sync.Map{}

// Put elements
m.Store(1, "one")
m.Store(2, "two")

// Get element 1
value, contains := m.Load(1)
if contains {
  fmt.Printf("%s\n", value.(string))
}

// Returns the existing value if present, otherwise stores it
value, loaded := m.LoadOrStore(3, "three")
if !loaded {
  fmt.Printf("%s\n", value.(string))
}

// Delete element 3
m.Delete(3)

// Iterate over all the elements
m.Range(func(key, value interface{}) bool {
  fmt.Printf("%d: %s\n", key.(int), value.(string))
  return true
})

// Range method takes a func(key, value interface{}) bool function. 
// If we return false, the iteration is stopped. Interesting fact, the worst-case time-complexity remains O(n) even if we return false after a constant time
```
- When shall we use sync.Map instead of a sync.Mutex on top of a classic map?
  - When we have frequent reads and infrequent writes (in the same vein to sync.RWMutex)
  - When multiple goroutines read, write, and overwrite entries for disjoint sets of keys. What does it mean concretely? For example, if we have a sharding implementation with a set of 4 goroutines and each goroutine in charge of 25% of the keys (without collision). In this case, sync.Map is also the preferred choice.

- **sync.Pool** : is a concurrent pool, in charge to hold safely a set of objects.
  -  Get() interface{} to retrieve an element
  -  Put(interface{}) to add an element

```go
pool := &sync.Pool{}

pool.Put(NewConnection(1))
pool.Put(NewConnection(2))
pool.Put(NewConnection(3))

connection := pool.Get().(*Connection)
fmt.Printf("%d\n", connection.id)
connection = pool.Get().(*Connection)
fmt.Printf("%d\n", connection.id)
connection = pool.Get().(*Connection)
fmt.Printf("%d\n", connection.id)
```

```go
// With a creator method
pool := &sync.Pool{
  New: func() interface{} {
    return NewConnection()
  },
}

connection := pool.Get().(*Connection)

// The first one is when we have to reuse shared and long-live objects like a DB connection for example.
// The second one is to optimize memory allocation.
```

```go
//function that writes into a buffer and persists the result to a file. With sync.Pool, we can reuse the space allocated for the buffer by reusing the same object across the different function calls.
//The first step is to retrieve the buffer previously allocated (or to create one if it’s the first call but this is abstracted). Then, the deferred action is to put the buffer back in the pool.
func writeFile(pool *sync.Pool, filename string) error {
	// Gets a buffer object
	buf := pool.Get().(*bytes.Buffer)
	// Returns the buffer into the pool
	defer pool.Put(buf)

	// Reset buffer otherwise it will contain "foo" during the first call
	// Then "foofoo" etc.
	buf.Reset()

	buf.WriteString("foo")

	return ioutil.WriteFile(filename, buf.Bytes(), 0644)
}
```

- **sync.Once** :  guarantee that a function is executed only once.
```go
once := &sync.Once{}
for i := 0; i < 4; i++ {
	i := i
	go func() {
		once.Do(func() {
			fmt.Printf("first %d\n", i)
		})
	}()
}
// We have used the Do(func()) method to specify the part that must be called only once.
```

- **sync.Cond** : Less used : It is used to emit a signal (one-to-one) or broadcast a signal (one-to-many) to goroutine(s).
- Let’s consider a scenario where we have to indicate to one goroutine that the first element of a shared slice has been updated.
- Creating a sync.Cond requires a sync.Locker object (either a sync.Mutex or a sync.RWMutex)

```go
cond := sync.NewCond(&sync.RWMutex{})
func printFirstElement(s []int, cond *sync.Cond) {
	cond.L.Lock()
	cond.Wait()
	fmt.Printf("%d\n", s[0])
	cond.L.Unlock()
}

// We'll create a pool of printFirstElement by passing a shared slice and the sync.Cond
// previously created.
// Then, we call a get() function, store the result in s[0] and emit a signal:

s := make([]int, 1)
for i := 0; i < runtime.NumCPU(); i++ {
	go printFirstElement(s, cond)
}

i := get()
cond.L.Lock()
s[0] = i
cond.Signal()
cond.L.Unlock()

// This signal will unblock one of the goroutine created that will display s[0].
// Now we could argue that our code might break one of the most fundamental principles of Go:
// Do not communicate by sharing memory; instead, share memory by communicating.
// Indeed, in this example, it would have been better to use a channel to communicate the value returned by get().
// Yet, we also mentioned that sync.Cond can also be used to broadcast a signal.
//Let’s just modify the end of the previous example by calling Broadcast() instead of Signal():

i := get()
cond.L.Lock()
s[0] = i
cond.Broadcast()
cond.L.Unlock()
```