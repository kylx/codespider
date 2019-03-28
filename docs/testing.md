[< BACK](../README.md)

# Testing

The goal is to automate as much testing as possible. Framework used is [pytest](https://www.youtube.com/playlist?list=PLbpAWbHbi5rPC8O7WIPXA4V8JLRnTPVGR).

### Advantages
1. fast *- just run some commands*
2. code breaking changes are easy to detect
3. more confident mag edit/refactor since you know your tests will tell you if you did something wrong

## Commands

Reinstall requirements first:
```
pip install -r requirements.txt
```

|cmd|description|
| --- | --- |
| `pytest` | run tests |
| `pytest -r a` |... and with summary |
| `pytest -r a --tb=no` | ... and with no traceback(mas compact) |

## Making tests

TODO

## Current tests covered
Hopefully daghan ug tests na macover sa future pero for now:

1. URL names and paths for major pages

