---
name: "java"
description: "Java programming language including OOP, collections, multithreading, and Spring framework"
version: "1.0.0"
---

# Java Programming

## Basics

```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

## Key Topics

- OOP: Classes, Inheritance, Interfaces, Polymorphism
- Collections: List, Set, Map, Queue
- Generics, Exceptions, Streams (Java 8+)
- JDBC Database Access
- Spring Boot Framework
- Maven/Gradle Build Tools

## Collections

```java
List<String> list = new ArrayList<>();
list.add("item");
Map<String, Integer> map = new HashMap<>();
map.put("key", 42);

// Stream API (Java 8+)
List<Integer> result = list.stream()
    .filter(s -> s.length() > 3)
    .map(String::toUpperCase)
    .collect(Collectors.toList());
```

## Concurrency

```java
// Runnable
Thread t = new Thread(() -> {
    System.out.println("Running");
});
t.start();

// ExecutorService
ExecutorService es = Executors.newFixedThreadPool(4);
es.submit(() -> task());
es.shutdown();
```
