name: dependencies

.left-column[
### What is it
### How is it used
### How it works
### Present state
### Dependencies
]

.right-column[

Inspect `setup.py` declared dependencies.

```py
install_requires=[
    "pyop==2.0.5",       # implements OIDC
    "pysaml2==4.5.0",    # implements SAML2
*   "pycryptodomex",     # unused - should be removed
    "requests",          # client requests to remote resources
    "PyYAML",            # implements YAML
*   "gunicorn",          # unused - not a dependency
    "Werkzeug",          # implements the proxy serving
    "click",             # used by scripts
*   "pystache"           # plugin dependency
],
extras_require={
*   "ldap": ["ldap3"]    # plugin dependency
},
```

Not many dependencies; that's a good thing :)

..But!

- `pyop` will be deprecated and replaced by new libs
- `pysaml2` needs work / 70+ issues / 20+ pull requests

]

???

`requests` + `Werkzeug` do we really need our own low level handlers to network
requests? Should we using something battletested like django or flask?

---
