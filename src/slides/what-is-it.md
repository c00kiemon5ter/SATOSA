name: what-is-it

.left-column[
### What is it
]

.right-column[
SATOSA stands for «SAML to SAML».

<div class="mermaid">
graph LR
	node#1[SAML]
	node#2[SAML]

	node#1 ---|to| node#2
</div>

A configurable proxy for translating between different authentication protocols
such as `SAML2`, `OpenID Connect` and `OAuth2`.

Part of the [IdentityPython][idpy] organisation.
]

---
name: what-is-it-2
count: false

.left-column[
### What is it
]

.right-column[
SATOSA stands for «SAML to SAML»

<div class="mermaid">
graph LR
	node#1[Protocol x]
	node#2[Protocol y]

	node#1 ---|translate to| node#2
</div>


A configurable proxy for translating between different authentication protocols
such as `SAML2`, `OpenID Connect` and `OAuth2`.

Part of the [IdentityPython][idpy] organisation.

### At its core it is a **_protocol translator_**.
]
---
