## Making packages

### Adjust version number

emacs setup.py

git status
git setup.py
git commit -m "bump version"
git push origin master

### PyPi

For making source package, run

```
python3 setup.py sdist
```

For upload to PyPI:

```
twine upload dist/iocbio.kinetics-1.0.0.tar.gz
```

### Make release at Gitlab

Go to https://gitlab.com/iocbio/kinetics/tags and make a new release
with Changelog


