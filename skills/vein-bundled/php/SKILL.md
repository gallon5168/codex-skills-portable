---
name: "php"
description: "PHP programming language basics, syntax, and security best practices"
version: "1.0.0"
---

# PHP Programming

## Basics

```php
<?php
$name = "John";
$age = 25;
echo "Hello, $name!";
?>
```

## Key Topics

- Variables, Arrays, Strings
- OOP Classes & Objects
- PDO Database Access
- Composer Dependencies
- Security: SQLi, XSS, CSRF Protection
- Laravel/Symfony Frameworks

## Reference

```php
// Arrays
$fruits = ["apple", "banana"];
$fruits[] = "orange";

// Superglobals
$_GET, $_POST, $_SESSION, $_COOKIE

// PDO Prepared Statements
$stmt = $pdo->prepare("SELECT * FROM users WHERE email = ?");
$stmt->execute([$email]);
```

## Security

```php
// Input sanitization
$clean = htmlspecialchars($input, ENT_QUOTES, 'UTF-8');

// Password hashing
$hash = password_hash($pass, PASSWORD_DEFAULT);

// CSRF token
$_SESSION['token'] = bin2hex(random_bytes(32));
```
