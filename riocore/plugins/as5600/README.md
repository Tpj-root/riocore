# as5600


magnetic absolute encoder

## Basic-Example:
```
{
    "type": "as5600",
    "pins": {
        "sda": {
            "pin": "0"
        },
        "scl": {
            "pin": "1"
        }
    }
}
```

## Pins:
### sda:

 * direction: inout
 * pullup: False

### scl:

 * direction: output
 * pullup: False


## Options:
### name:
name of this plugin instance

 * type: str
 * default: None

### net:
target net in LinuxCNC

 * type: str
 * default: None


## Signals:
### position:

 * type: float
 * direction: input


## Interfaces:
### position:

 * size: 32 bit
 * direction: input


## Full-Example:
```
{
    "type": "as5600",
    "name": "",
    "net": "",
    "pins": {
        "sda": {
            "pin": "0",
            "modifiers": [
                {
                    "type": "invert"
                }
            ]
        },
        "scl": {
            "pin": "1",
            "modifiers": [
                {
                    "type": "invert"
                }
            ]
        }
    },
    "signals": {
        "position": {
            "net": "xxx.yyy.zzz",
            "function": "rio.xxx",
            "scale": 100.0,
            "offset": 0.0,
            "display": {
                "title": "position",
                "section": "inputs",
                "type": "meter"
            }
        }
    }
}
```

## Verilogs:
 * as5600.v