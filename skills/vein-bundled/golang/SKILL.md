---
name: "golang"
description: "Go programming language including goroutines, channels, and concurrency patterns"
version: "1.0.0"
---

# Go Programming

## Basics

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
```

## Key Topics

- Variables, Types, Slices, Maps
- Functions, Methods, Interfaces
- Goroutines, Channels, Select
- Error Handling (no exceptions)
- Packages, Testing
- Concurrency Patterns

## Concurrency

```go
// Goroutine
go func() {
    fmt.Println("Running in background")
}()

// Channel
ch := make(chan int, 10)
ch <- 42
value := <-ch

// Select
select {
case v := <-ch1:
    fmt.Println("From ch1:", v)
case v := <-ch2:
    fmt.Println("From ch2:", v)
default:
    fmt.Println("No message")
}

// WaitGroup
var wg sync.WaitGroup
wg.Add(2)
go func() { defer wg.Done(); work1() }()
go func() { defer wg.Done(); work2() }()
wg.Wait()
```

## Interfaces

```go
type Writer interface {
    Write([]byte) (int, error)
}

type File struct {
    name string
}

func (f *File) Write(p []byte) (int, error) {
    // Implementation
    return len(p), nil
}

// Polymorphism
func process(w Writer) {
    w.Write([]byte("data"))
}
```
