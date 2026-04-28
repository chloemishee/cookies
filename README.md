# Cookies Demo

## Project Summary
This project shows how missing HttpOnly protection allows JavaScript to read and steal a session cookie. The secure version uses HttpOnly and SameSite=Strict to protect the session cookie.

## Threat Model
In this project, an attacker is able to run JavaScript in the victim’s browser (like in a typical XSS attack). The goal is to steal the session_id cookie and use it to impersonate the user.

## Security Mechanism
Primary mechanism: HttpOnly cookie flag  
Supporting mechanism: SameSite=Strict

## How to Run
cd cookie-demo
python3 app.py
Open http://127.0.0.1:5000

## Vulnerable Demo
1. Log in using Vulnerable Mode.
2. Click the steal cookie button.
3. Go to /attacker.
4. The session_id appears because JavaScript could read document.cookie.

## Secure Demo
1. Log in using Secure Mode.
2. Click the steal cookie button.
3. Go to /attacker.
4. The session_id does not appear because HttpOnly blocks JavaScript access.

## Failure Case
If HttpOnly is removed, JavaScript can access document.cookie and send the session_id to the attacker. This breaks session confidentiality and allows possible session hijacking.
