**animaljam**
---

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