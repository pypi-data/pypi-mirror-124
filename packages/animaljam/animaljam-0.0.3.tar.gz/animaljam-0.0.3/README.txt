**animaljam**
===

**animaljam** a python module to easily create bots on Animal Jam Classic.

Example:
---

```py
import animaljam

if animaljam.login('username', 'password') == 'Failed to login.':
    print('Error logging in!')
else:
    animaljam.joinDen('randomusername')
    while True:
        animaljam.jag('randomusername', 'LOL')
```

Features:
---

- Buddy
- Buddy Remove
- JAG
- Join Den
- Join Room
- Change colour
- Move
- Teleport
- Manual packet sending