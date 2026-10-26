---
name: "html"
description: "HTML5 markup language for web page structure and semantic elements"
version: "1.0.0"
---

# HTML Programming

## Basics

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Title</title>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>
```

## Key Topics

- Semantic Elements: header, nav, main, article, section, footer
- Forms & Input Validation
- Tables, Lists, Links
- Images, Audio, Video
- Accessibility (ARIA, alt text)
- SEO Best Practices

## Forms

```html
<form action="/submit" method="POST">
    <label for="email">Email:</label>
    <input type="email" id="email" name="email" required>
    <input type="submit" value="Submit">
</form>
```

## Responsive Images

```html
<img src="small.jpg" 
     srcset="small.jpg 480w, medium.jpg 800w, large.jpg 1200w"
     sizes="(max-width: 600px) 100vw, 50vw"
     alt="Description"
     loading="lazy">
```
