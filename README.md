# <p align="center">Election Tracker 🇺🇸</p>

<p align="center">
    <a href="#overview">Overview</a>
    &nbsp; • &nbsp;
    <a href="#technologies">Technologies</a>
    &nbsp; • &nbsp;
    <a href="#usage">Usage</a>
    &nbsp; • &nbsp;
    <a href="#license">License</a>
</p>

<p align="center">
<img src="https://img.shields.io/github/languages/count/luisarojas/elections-tracker.svg?style=flat" alt="languages-badge"/>
<img src="https://img.shields.io/github/license/luisarojas/elections-tracker.svg?style=flat" alt="license-badge"/>
<img src="https://img.shields.io/github/repo-size/luisarojas/elections-tracker" alt="repo-size-badge">
<img src="https://img.shields.io/github/last-commit/luisarojas/elections-tracker" alt="last-commit-badge">
<img src="https://img.shields.io/github/issues-raw/luisarojas/elections-tracker" alt="open-issues-badge">
</p>



## Overview

To avoid a heart-attack induced by refreshing the election results (way) too often, I decided to, instead, create a web scraper that could check for updates for me.

The script uses [ABC News](https://abcnews.go.com/Elections) as its source and checks it every 15 minutes. If any changes are identified, an e-mail will be sent to all recipients specified in the `env.py` file (not included).

<p style="color: grey;">Disclaimer: Please note that I wrote this program in a bit of a rush, since the election is close to its conclusion. I'm aware there is plenty of room for refactoring and general improvement!</p>


## Technologies

* `python==3.8.6`
* `beautifulsoup4==4.9.3`
* `lxml==4.6.1`
* `requests==2.24.0`


## Usage

### Inputs

No command-line inputs are required; only your `env.py` is needed.

### What should your `env.py` look like?

```python
ENV = {
    'recipient': {
        'emails': ['recipient1@mail.com', 'recipient2@mailcom']
    },
    'sender': {
        'email': 'sender@email.com',
        'password': 'senderpassword'
    }
}
```
<p style="color: grey;">Note: If using Gmail, you should enable the setting to allow access from "less secure apps".</p>


### Execution

```
$ pipenv run python run.py
```

## License

This project was released under the [MIT License](http://www.opensource.org/licenses/MIT).

Copyright &copy; 2020 Luisa Rojas

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
