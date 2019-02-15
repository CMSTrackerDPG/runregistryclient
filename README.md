[![Build Status](https://travis-ci.com/ptrstn/runregistryclient.svg?branch=master)](https://travis-ci.com/ptrstn/runregistryclient)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# CERN CMS Run Registry client

A python client to the new [Run Registry](https://cmsrunregistry.web.cern.ch/).
An python client to the [old Run Registry]() can be found [here](https://github.com/ptrstn/runregcrawlr/tree/master/runregcrawlr).


## Installation

```bash
pip install git+https://github.com/ptrstn/runregistryclient
```

## Usage

### Example 

If you want to get a single run do:

```python
import runreg

runreg.get(run_number=327600)
```

If you prefer a non nested json output then use the ```flat=True``` parameter

```python
import runreg

runreg.get(run_number=327600, flat=True)
```

```runreg``` assumes per default the *tracker* workspace. If you want to change it, you can do so by specifying the ```workspace``` attribute:

```python
import runreg

runreg.get(run_number=327600, workspace="global")
```

#### Multiple filters at once

If you want to use multiple filters at once, for example, to filter by a run number range with a specific criteria, then you can do so like this:

```python
import runreg

runreg.get(run_number=[(327596, ">="), (327744, "lte")], name=("%Cosmics%", "like"))
```

### Operators

Following operators are supported:

* ```=``` or ```eq``` (assumed per default)
* ```>=``` or ```gte```
* ```>=``` or ```gte```
* ```>``` or ```gt```
* ```<=``` or ```lte```
* ```<``` or ```lt```
* ```like```

The operators should be specified as the second element of a (value, operator) tuple such as ```(321123, "<=")```

### Attributes

All available attributes can be found in the ```docs``` folder under ```attributes.md```

## Development

Python version *3.5* or higher is required.

If you want to improve this software you should follow these steps:

```bash
git clone https://github.com/ptrstn/runregistryclient
cd runregistryclient
python -m venv venv
. venv/bin/activate
pip install -e .
pip install -r testing-requirements
```

### Running Tests

```
pytest
```

## FAQ

### How do you filter by subcomponent status?

When you want to filter by subcomponent status like *Pixel*, or *SiStrip* you have to follow to use the attribute names es specified in the RunRegistry API.
Unfortunately they contain "-" and "." therefore you have to use a little trick.

For example to filter by ```track``` ```status``` in the ```tracker``` workspace you have to do:

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

```track``` is used for the *global* workspace while ```tracker-track``` uses the *tracker* workspace. 
Same applies for ```tracker-pix```/```pix```, ```tracker-strip```/```strip```.

## References

* https://cmsrunregistry.web.cern.ch/
