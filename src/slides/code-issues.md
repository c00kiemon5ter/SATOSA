name: future

.left-column[
### What is it
### How is it used
### How it works
### Present state
### Dependencies
### Project issues
### Code issues
]

.right-column[

### Code-level improvements and architectural concerns

* Separate concerns: layering and subsystems

* Network layer & HTTP conformance

* Persistence & state

* Logging

* Error handling

* Microservices

* Plugins / Hooks / Events

* Dependencies

]

???

* Separate concerns, create layers and proper subsystems / modules

  Each module, each class, each function should be concerned by a single thing
  and nothing more. Making progress is based on the idea of abstracting
  concepts such that they have a single responsibility and those are
  orchestrated on a higher level.

  Separating concerns results to simpler code, easier to debug, easier to
  replace and easier to extend. Code is naturally layered to express more
  complex systems.

  Such layers are
  - data access or IO layer: networking, logging, persistence
  - business layer: the core domain
  - application or service layer
  - presentation layer

  Lots of refactoring.

* Network layer & HTTP conformance

  Separate the network layer - maybe wrap the core in a framework like `django`
  or `Flask`.

  Correctly handle erroneous requests. Proper logging, meaningful error
  reporting and appropriate status codes.

  Add proper support for frontend development.  Only send and receive data and
  offload the presentation to a frontend app or wrapper with templates.

  Define an API and message schema.

* Persistence

  Persistence is defined as state that outlives the process itself.

  Correctly configure and manage persistence (configuration and low level
  details)

  Unify the interface between in memory, file or database storage.

  Use adapters.

* Logging

  Logging and error handling has been troublesome and more and more people find
  it hard to understand what broke their setup.

  Logging will change a lot by adopting a structured format, enforcing a sane
  default behavior and utilizing different logger names and loglevels.

* Error handling

  Error handling will also change as part of the transformation of the logging
  process but also the refactoring that will take place.

  Proper and meaningful errors should be emitted by each module and errors
  should be chained (`rase ... from` pattern) to reveal what really has
  happened.

* Microservices

  Microservices are split from the main repository and a process needs to be
  decided as to how they will be integrated with SATOSA again. The approach
  that seems to satisfy and solve most problems is to separate each
  microservice to its own repository as its own package. Each microservice
  package has its own functionality and well defined purpose and dependencies.

* Plugins / Hooks

  I want to revisit the trade-offs of the choices made when defining the plugin
  interface. A flexible system should have multiple points where it can be
  configured.

  Hooks should be used at key-places where implementors can have access to
  affect the flow of execution.

  Events (or signals) can be used where asynchronous processing is needed.

  This will allow for greater customisability and things that currently cannot
  be done with microservices.

  Look into ideas from `py.test`:
  https://docs.pytest.org/en/latest/writing_plugins.html#writing-plugins

  or `eclipse`:
  https://www.eclipse.org/articles/Article-Plug-in-architecture/plugin_architecture.html

* Dependencies

  Last but not least, SATOSA depends on other components and their
  configurations. We are limited by those components, and maybe we should be
  looking into those too, to extend and improve.

* Other / Misc

  The list does not stop here. More are things are yet to be thought and
  implemented, like monitoring, health checks, self healing processes, scaling
  into multiple machines and communicating as a cluster, etc

---
