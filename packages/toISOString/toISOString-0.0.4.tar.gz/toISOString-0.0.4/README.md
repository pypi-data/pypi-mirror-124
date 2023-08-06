# toISOString
this package convert Python Date to Javascript's `Date.prototype.toISOString`

## install

```
pip install toISOString
```

## usage

```
from datetime import datetime
from toISOString import toISOString

now = datetime.now()
print(toISOString(now))
```
