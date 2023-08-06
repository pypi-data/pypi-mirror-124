#  Pygwin

Pygwin (pygame window system) provides a set of classes to program
very basic window interfaces with pygame.

pygwin is hosted on gitlab:
https://gitlab.com/qouify/pygwin/


## License

Pygwin is published under the term of
[GPLv3](https://www.gnu.org/licenses/gpl-3.0.txt).


## Installation

Install latest pygwin release with pip:

```
pip3 install pygwin
```

or to get the development version:
```
git clone https://gitlab.com/qouify/pygwin/
cd pygwin
python setup.py install --user
```


## Testing

To see the some of the features provided by the module:

```python
from pygwin.test import test
test.go()
```
