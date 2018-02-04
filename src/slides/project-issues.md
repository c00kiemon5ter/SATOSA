name: project-issues

.left-column[
### What is it
### How is it used
### How it works
### Present state
### Dependencies
### Project issues
]

.right-column[

### Project-level improvements

* Documentation

* Tests

* Coding practices

* Release management

]

???

Things I would like to see improve are:

## Documentation

- improve the existing documentation
- bring it up to date
- simplify some things and add more examples
- look into ways to automate the generation
- sync with platforms like readthedocs
- document the code / not only the flow-configurations

## Tests

- go over all the tests
- make sure they test "the right thing"
- write tests for all pending fixes and new features
- try to do end-to-end tests

## Coding practices

As part of the idpy.org a set of coding practices will be decided upon for all
projects to follow. This will include things from formatting and naming
conventions to usage of dangerous functions such as `subprocess.call()` or the
usage of `pickle` or git-commit templates and examples.

## Releases

Complains have been all over lately regarding SATOSA releases. I would like
this to change to a model where releases are smaller and more-often. Releases
should contain a changelog which should map to the commits included in the
release.

Breaking changes should be expressed clearly and be accompanied by a migration
document or script.

---
