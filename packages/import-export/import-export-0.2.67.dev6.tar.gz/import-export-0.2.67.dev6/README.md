# import export
## A Python package methods decorator

Once upon a time, not very long time ago, about last Friday...

Let me show here! tldr

### 1. install
```bash
pip install import-export
```

### 2. use 
```python
"""mypack.py"""
import export

def fee():
    print 'twee'
	
@export
def moo():
    print 'moow'
```
```python
> from mypack import *
> print(fee())
NameError: name 'fee' is not defined
> print(moo())
moow
```

### How it work
* Eeh... just add decorated resource name to the dictionary `module.__all__[]`


## License
* It's opensource and free software, see the [LICENSE](LICENSE) for more details.


## Credits
* This project is inspired by [export joke](https://pypi.org/project/export/) :: http://github.com/zsiciarz/export
* Written in [CudaText](https://cudatext.github.io/) :: https://github.com/Alexey-T/CudaText/
* Lot a thnx SO topic writers https://stackoverflow.com/q/44834


## TODO
* [ ] `export(None)` - export nothing outside pkg
* [ ] may be implement `private()` `public()` etc decorator to classes
* [ ] your ideas? 
