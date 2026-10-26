---
name: "cpp"
description: "C++ programming with modern C++ features, STL, templates, and OOP"
version: "1.0.0"
---

# C++ Programming

## Basics

```cpp
#include <iostream>
#include <vector>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
```

## Key Topics

- Modern C++ (C++11/14/17/20)
- STL Containers: vector, map, set
- Smart Pointers (unique_ptr, shared_ptr)
- Templates, Lambda Expressions
- OOP: Classes, Inheritance, Virtual Functions
- Concurrency: threads, mutex, async

## Modern Features

```cpp
// Smart pointers
auto ptr = std::make_unique<int>(42);
auto shared = std::make_shared<int>(100);

// Range-based for
std::vector<int> v = {1, 2, 3};
for (auto& item : v) { item *= 2; }

// Lambda
auto square = [](int x) { return x * x; };
std::cout << square(5) << std::endl;

// Auto deduction
auto x = 42;  // int
auto name = "John";  // const char*
```

## STL Containers

```cpp
std::vector<int> v = {5, 2, 8, 1, 9};
std::sort(v.begin(), v.end());

std::map<std::string, int> m;
m["key"] = 42;

auto it = std::find(v.begin(), v.end(), 5);
```
