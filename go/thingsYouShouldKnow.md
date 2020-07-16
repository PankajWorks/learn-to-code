## Anonymous structs
> Grouped globals
```go
var config struct {
    APIKey      string
    OAuthConfig oauth.Config
}

config.APIKey = "BADC0C0A"
```
> Template data
```go
data := struct {
    Title string
    Users []*User
}{
    title,
    users,
}
err := tmpl.Execute(w, data)
```
> (Cheaper and safer than using map[string]interface{}.)

> Test tables
```go
var indexRuneTests = []struct {
    s    string
    rune rune
    out  int
}{
    {"a A x", 'A', 2},
    {"some_text=some_value", '=', 9},
    {"☺a", 'a', 3},
    {"a☻☺b", '☺', 4},
}
```
> Embedded lock
```go
var hits struct {
    sync.Mutex
    n int
}

hits.Lock()
hits.n++
hits.Unlock()
```

## Nested structs
> Decoding deeply nested JSON data

```go
{"data": {"children": [
  {"data": {
    "title": "The Go homepage",
    "url": "http://golang.org/"
  }},
  ...
]}}
```

```go
type Item struct {
    Title string
    URL   string
}

type Response struct {
    Data struct {
        Children []struct {
            Data Item
        }
    }
}
```

## Command-line godoc
```bash
% godoc sync Mutex
PACKAGE

package sync
    import "sync"

TYPES

type Mutex struct {
    // contains filtered or unexported fields
}
    A Mutex is a mutual exclusion lock. Mutexes can be created as part of
    other structures; the zero value for a Mutex is an unlocked mutex.

func (m *Mutex) Lock()
    Lock locks m. If the lock is already in use, the calling goroutine
    blocks until the mutex is available.

func (m *Mutex) Unlock()
    Unlock unlocks m. It is a run-time error if m is not locked on entry to
    Unlock.

    A locked Mutex is not associated with a particular goroutine. It is
    allowed for one goroutine to lock a Mutex and then arrange for another
    goroutine to unlock it.
```

## go get supports custom domains
> See `go help importpath` for the details.

## Mock out the file system
> Got a package that works with the file system, but don't want your tests to actually use the disk?

```go
var fs fileSystem = osFS{}

type fileSystem interface {
    Open(name string) (file, error)
    Stat(name string) (os.FileInfo, error)
}

type file interface {
    io.Closer
    io.Reader
    io.ReaderAt
    io.Seeker
    Stat() (os.FileInfo, error)
}

// osFS implements fileSystem using the local disk.
type osFS struct{}

func (osFS) Open(name string) (file, error)        { return os.Open(name) }
func (osFS) Stat(name string) (os.FileInfo, error) { return os.Stat(name) }
```

##  Method expressions
```go
type T struct {}
func (T) Foo(s string) { println(s) }

var fn func(T, string) = T.Foo
```
> Real example from os/exec:
```go
func (c *Cmd) stdin() (f *os.File, err error)
func (c *Cmd) stdout() (f *os.File, err error)
func (c *Cmd) stderr() (f *os.File, err error)

```
```go
type F func(*Cmd) (*os.File, error)
for _, setupFd := range []F{(*Cmd).stdin, (*Cmd).stdout, (*Cmd).stderr} {
    fd, err := setupFd(c)
    if err != nil {
        c.closeDescriptors(c.closeAfterStart)
        c.closeDescriptors(c.closeAfterWait)
        return err
    }
    c.childFiles = append(c.childFiles, fd)
}
```
## Send and receive on the same channel
```go
package main

import "fmt"

var battle = make(chan string)

func warrior(name string, done chan struct{}) {
    select {
    case opponent := <-battle:
        fmt.Printf("%s beat %s\n", name, opponent)
    case battle <- name:
        // I lost :-(
    }
    done <- struct{}{}
}

func main() {
    done := make(chan struct{})
    langs := []string{"Go", "C", "C++", "Java", "Perl", "Python"}
    for _, l := range langs { go warrior(l, done) }
    for _ = range langs { <-done }
}
```
> Using close to broadcast
```go
func waiter(i int, block, done chan struct{}) {
    time.Sleep(time.Duration(rand.Intn(3000)) * time.Millisecond)
    fmt.Println(i, "waiting...")
    <-block
    fmt.Println(i, "done!")
    done <- struct{}{}
}

func main() {
    block, done := make(chan struct{}), make(chan struct{})
    for i := 0; i < 4; i++ {
        go waiter(i, block, done)
    }
    time.Sleep(5 * time.Second)
    close(block)
    for i := 0; i < 4; i++ {
        <-done
    }
}
```

```go
func worker(i int, ch chan Work, quit chan struct{}) {
    var quitting bool
    for {
        select {
        case w := <-ch:
            if quitting {
                w.Refuse(); fmt.Println("worker", i, "refused", w)
                break
            }
            w.Do(); fmt.Println("worker", i, "processed", w)
        case <-quit:
            fmt.Println("worker", i, "quitting")
            quitting = true
        }
    }
}

func main() {
    ch, quit := make(chan Work), make(chan struct{})
    go makeWork(ch)
    for i := 0; i < 4; i++ { go worker(i, ch, quit) }
    time.Sleep(5 * time.Second)
    close(quit)
    time.Sleep(2 * time.Second)
}
```

## Nil channel in select
```go
func worker(i int, ch chan Work, quit chan struct{}) {
    for {
        select {
        case w := <-ch:
            if quit == nil {
                w.Refuse(); fmt.Println("worker", i, "refused", w)
                break
            }
            w.Do(); fmt.Println("worker", i, "processed", w)
        case <-quit:
            fmt.Println("worker", i, "quitting")
            quit = nil
        }
    }
}

func main() {
    ch, quit := make(chan Work), make(chan struct{})
    go makeWork(ch)
    for i := 0; i < 4; i++ { go worker(i, ch, quit) }
    time.Sleep(5 * time.Second)
    close(quit)
    time.Sleep(2 * time.Second)
}
```
