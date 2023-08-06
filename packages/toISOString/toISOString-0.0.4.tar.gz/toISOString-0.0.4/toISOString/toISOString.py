import pytz

# toISOString is just the same as Javascript's Date.prototype.toISOString
def toISOString(d):
    return f'{d.astimezone(pytz.utc).isoformat(timespec="milliseconds").replace("+00:00","")}Z'
