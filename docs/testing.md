[< BACK](../README.md)

# Testing

The goal is to automate as much testing as possible.

### Advantages
1. fast *- just run some commands*
2. code breaking changes are easy to detect
3. more confident mag edit/refactor since you know your tests will tell you if you did something wrong

## Commands

Reinstall requirements first:
```
pip install -r requirements.txt
```

|||
| --- | --- |
| `pytest` | run tests |
| `pytest -r a` |... and with summary |
| `pytest -r a --tb=no` | ... and with no traceback(mas compact) |

## Making tests

TODO

## Current tests covered

1. URL names and paths for major pages

