# Intro to Web Security Notes w/ References

## For the love of God, sanitize your inputs.

### SQL Injections

Really bad SQL table design & no sanitization of inputs lets people just do whatever they want with your database.

Archetypical unsanitized SQL request:

`SELECT user FROM users WHERE Username = '?' AND Password = '?'`

Where `?` is replaced by user input.

If I wanted to get root access, I'd try typical root account usernames, such as "admin" or "root" and input `' OR '1' = '1'` as the password field, because 1 is always equal to 1. Therefore, if an admin account existed, I could get it. It goes without saying I could also then sign into anyone's account.

### XSS | Cross Site Scripting

3 Types:

1. Reflected XSS

Payload delivered via URL or request. Immediately reflected in HTTP request.
Used by malicious actors to use your legitimate site to do bad things to users. Bad, but mainly because it lets people abuse your servers & name to do bad things.

2. Stored XSS

The big one. Payload gets saved onto your servers/database/CMS and served back to users persistently. Congrats, someone weaseled their way into your backend! This is probably the worst

3. DOM-Based XSS

Client-side. Browser does malicious things due to "DOM manip". Think of that one gif that would crash discord a while back.

Source: [Palo Alto Networks](https://www.paloaltonetworks.com/cyberpedia/xss-cross-site-scripting)

