---
title: Intro to Web Security
subtitle: LUG X WiCyS Cybersec Week 
author: Michael Hanif Khan
date: 9/25/25
---

## 
\tableofcontents

# SQL Injections

## SQL Queries

`SELECT * FROM users WHERE username = 'username' AND password = 'password';`

Gets all entries from SQL database table "users" where the username is `username` and the password is `password`.

Therefore, a general format would look something like this:

`SELECT * FROM users WHERE username = '{username}' AND password = '{password}';`

Where username and password are variable per account.

## Injections

If we don't sanitize our inputs, single quotes input by a user can alter the structure of the actual query.

EXAMPLE:
username = `admin`
password = `' OR '1' = '1`

Becomes `SELECT * FROM users WHERE username = 'admin' AND password = '' OR '1' = '1';`
Which translates to, give me all accounts with the username admin and whose password is the empty string OR in the case `'1' = '1'`, which it always will.

This allows people to:

1. Sign into other people's accounts

2. Use accounts which don't actually exist, so they can't be moderated.

# XSS - Cross Site Scripting

## XSS

Place holder
