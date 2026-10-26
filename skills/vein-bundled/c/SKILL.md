---
name: "c"
description: "C programming language for system programming, memory management, and low-level operations"
version: "1.0.0"
---

# C Programming

## Basics

```c
#include <stdio.h>

int main() {
    printf("Hello, World!\n");
    return 0;
}
```

## Key Topics

- Pointers, Arrays, Strings
- Memory Management (malloc/free)
- Structures, Unions
- File I/O Operations
- Preprocessor Directives
- Makefiles

## Pointers

```c
int num = 42;
int* ptr = &num;  // Address of num

printf("%d\n", *ptr);  // Dereference: 42

// Dynamic allocation
int* arr = malloc(100 * sizeof(int));
if (arr == NULL) { /* handle error */ }
free(arr);
```

## File I/O

```c
FILE* fp = fopen("file.txt", "r");
if (fp == NULL) { perror("Error"); exit(1); }

fprintf(fp, "Hello\n");
fscanf(fp, "%d", &num);

fclose(fp);
```
