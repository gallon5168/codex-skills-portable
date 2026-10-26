---
name: "javascript"
description: "JavaScript programming for web, including ES6+ features, DOM, async programming"
version: "1.0.0"
---

# JavaScript Programming

## Basics

```javascript
const name = "John";
const numbers = [1, 2, 3];

// Arrow functions
const double = x => x * 2;

// Destructuring
const { first, last } = { first: "John", last: "Doe" };
const [a, b] = [1, 2];
```

## Key Topics

- ES6+ Features: let/const, arrow functions, destructuring
- DOM Manipulation
- Promises, Async/Await
- Modules (ES6+)
- Fetch API, Local Storage
- Event Handling, Event Delegation

## Async Programming

```javascript
// Promise
fetch('/api/data')
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));

// Async/Await
async function getData() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(error);
    }
}
```

## DOM

```javascript
// Select
const el = document.querySelector('#id');
const items = document.querySelectorAll('.class');

// Modify
el.textContent = 'New text';
el.classList.add('active');

// Events
el.addEventListener('click', (e) => {
    e.preventDefault();
    console.log('Clicked');
});
```
