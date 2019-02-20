[![Build Status](https://travis-ci.com/ptrstn/runregistryclient.svg?branch=master)](https://travis-ci.com/ptrstn/runregistryclient)
[![codecov](https://codecov.io/gh/ptrstn/runregistryclient/branch/master/graph/badge.svg)](https://codecov.io/gh/ptrstn/runregistryclient)
[![](https://img.shields.io/pypi/v/runregistryclient.svg)](https://pypi.org/project/runregistryclient/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# CERN CMS Run Registry client

A Python client for the [new RunRegistry](https://cmsrunregistry.web.cern.ch/). 
A Python client for the [old RunRegistry](https://cmswbmoffshift.web.cern.ch/cmswbmoffshift/runregistry_offline/index.jsf) can be found [here](https://github.com/ptrstn/runregcrawlr/tree/master/runregcrawlr).

## Installation

```bash
pip install runregistryclient
```

## Usage

### Example 

If you want a single run, do this:

```python
import runreg

runreg.get(run_number=327600)
```

If you prefer a non-nested JSON output, use the ```flat=True``` parameter.

```python
import runreg

runreg.get(run_number=327600, flat=True)
```

```runreg``` assumes the *tracker* workspace by default. 
If you want to change it, you can do so by specifying the ```workspace``` attribute:

```python
import runreg

runreg.get(run_number=327600, workspace="global")
```

#### Multiple filters at once

If you want to use several filters at once, for example, to filter according to a sequence number range with certain criteria, you can do it this way:

```python
import runreg

runreg.get(run_number=[(327596, ">="), (327744, "lte")], name=("%Cosmics%", "like"))
```

Or if you prefer [Django like](https://docs.djangoproject.com/en/dev/topics/db/queries/#field-lookups) lookup fields:

```python
import runreg

runreg.get(run_number__gte=327596, run_number__lte=327744, name__like="%Cosmics%")
```


### Operators

Following operators are supported:

* ```=``` or ```eq``` (assumed per default)
* ```>=``` or ```gte```
* ```>``` or ```gt```
* ```<=``` or ```lte```
* ```<``` or ```lt```
* ```like```

The operators should be specified as the second element of a (value, operator) tuple such as ```(321123, "<=")```.

### Attributes

All available attributes can be found in the ```docs``` folder under ```attributes.md```.

## Development

Python version *3.5* or higher is required.

If you want to improve this software, you should follow these steps:

```bash
git clone https://github.com/ptrstn/runregistryclient
cd runregistryclient
python -m venv venv
. venv/bin/activate
pip install -e .
pip install -r testing-requirements.txt
```

### Running Tests

```
pytest --cov .
```

## FAQ

### How do you filter by subcomponent status?

If you want to filter for subcomponent states such as *Pixel* or *SiStrip*, you must use the attribute names specified in the RunRegistry API.
Unfortunately, they contain "-" and "." characters, so you need to use a little trick.

For example, to filter for the ```Track``` ```Status``` in the workspace ```Tracker``` then you need to do:

```python
import runreg

runreg.get(**{"tracker-track.status": "GOOD"})
```

You can still combine this with other attributes and options:

```python
import runreg

runreg.get(flat=True, run_number=[(327596, ">="), (327744, "lte")], **{"pix.status": "EXCLUDED", "strip.status":"GOOD"})
```

### Whats the difference between tracker-track and track?

```track``` is used for the *global* workspace, while ```tracker-track``` uses the *tracker* workspace. 
The same is true for ```tracker-pix``` / ```pix``` and ```tracker-strip``` / ```strip```.

## References

* https://cmsrunregistry.web.cern.ch/
