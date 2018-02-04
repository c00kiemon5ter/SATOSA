name: how-it-works

.left-column[
### What is it
### How is it used
### How it works
]

.right-column.center[

<div class="mermaid">
graph TD
	sp(Service Provider)
	idp(Identity Provider)
	frontend[Frontend: Protocol x IdP]
	backend[Backend: Protocol y SP]
	state[Internal state]

	subgraph SATOSA
		frontend ---|translate from incoming protocol| state
		state ---|translate to outgoing protocol| backend
	end

	sp ---|Protocol x| frontend
	backend ---|Protocol y| idp
</div>

]

???

* a frontend plugin mimics protocol x IdP

* a backend plugin mimics protocol y SP/client

* SATOSA has been configured with an attribute map that is used to translate
  attributes from one protocol to another

* internally SATOSA stores

  * `SESSION_ID`: This is a session identifier given by the SATOSA proxy
  * `SATOSA_REQUESTER`: The identifier of the requester who called the proxy
  * `IDHASHER.hash_type`: Which identifier type the requester is asking for
    (ie, persistent, transient, etc)
  * `ROUTER`: Which frontend module that should answer the requester

* other plugins/microservices are utilized to achieve more functionality
  * consent service
  * account linking
  * logging
  * routing
  * etc

---
