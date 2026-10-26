---
name: "css"
description: "CSS3 styling language including Flexbox, Grid, animations, and responsive design"
version: "1.0.0"
---

# CSS Programming

## Basics

```css
.selector {
    property: value;
    /* Comment */
}
```

## Layout Systems

```css
/* Flexbox */
.container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
}

/* Grid */
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
}
```

## Key Topics

- Box Model, Selectors, Specificity
- Flexbox, Grid Layout
- Animations, Transitions, Transforms
- Media Queries, Responsive Design
- CSS Variables (Custom Properties)
- CSS Frameworks (Bootstrap, Tailwind)

## Animations

```css
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.element {
    animation: fadeIn 0.5s ease-in-out;
    transition: all 0.3s ease;
}
```

## Variables

```css
:root {
    --primary-color: #3498db;
    --font-size: 16px;
}

.element {
    color: var(--primary-color);
    font-size: var(--font-size);
}
```
