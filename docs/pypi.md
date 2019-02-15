# Upload package to pypi

## Generate archive 

```bash
pip install setuptools wheel
python setup.py sdist bdist_wheel
```

## Upload

```bash
pip install twine
twine upload dist/* 
```