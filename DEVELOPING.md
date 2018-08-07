# Developing actionqueues

`actionqueues` is currently developed for Python 2.7, but works with 3.x.

## Getting started

Use `pipenv` to install the development environment:

```sh
pipenv install -d
```

## Testing

Run:

```sh
make test
```

It runs:

- pylint.
- pytest with coverage.

## Uploading a release

The project uses [`twine`](https://github.com/pypa/twine) to upload releases.
This will be installed when running `pipenv install -d`, above.

1. Update setup.py version number
2. Upload the binary:

        rm -rf dist
        python setup.py sdist bdist_wheel
        twine upload dist/*
        rm -rf dist

ref: https://github.com/pypa/twine#using-twine
