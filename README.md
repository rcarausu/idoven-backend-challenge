# ECG (electrocardiograms) service

This repository contains the code of a microservice that allows users to register or store ECGs for processing, 
and then query various insights about them, such as the number of zero crossings of the signal.

## Description

The project is built using Python + FastAPI stack, following _**Hexagonal**_
(also known as _**Ports and Adapters**_) architectural style and a simplistic approach of the CQRS pattern.

In the following image ([source](https://betterprogramming.pub/a-quick-and-practical-example-of-hexagonal-architecture-in-java-8d57c419250d)), we can see a diagram representing the different parts that may for a
system following this architecture design:

![hexagonal_architecture](resources/hexagonal_architecture.png)

The directory structure is as follows:
- [src](src) &rarr; main package with all the source code.
  - [ecg](src/ecg) &rarr; package with all the code related to the ECG feature.
    - [adapter](src/ecg/adapter) &rarr; implementations of the interfaces (ports) that communicate with the application core.
        There are two types of adapters:
      - *in_adapters* &rarr; they are implementations of external systems that communicate *inwards* with the 
      application, such as HTTP, etc.
      - *out_adapters* &rarr; they are implementations of external system that communicate *outwards* with the
      application, such as databases, etc.
    - [application](src/ecg/application) &rarr; [ports](src/ecg/application/port) (interfaces) that adapters implement for 
    communication with the application core. There are two types as well, *in_ports* and *out_ports*, following the
    same logic as with adapters.
    Here we can also find the [service](src/ecg/application/service) package, which add another layer for further 
    segregation of dependencies between domain entities and adapter implementations.
    - [domain](src/ecg/domain) &rarr; main domain model and business logic of the application.

## Running

* Install Python 3.11. You can use [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation) 
to install the required Python version.
```shell
pyenv install 3.11.7
```

* Set it up as the global version.
```shell
pyenv global 3.11.7
```

* Create the virtual environment with the [pyenv virtualenv plugin](https://github.com/pyenv/pyenv-virtualenv).
```shell
pyenv virtualenv 3.11.7 idoven-venv-3.11.7
```

* Activate it
```shell
pyenv activate idoven-venv-3.11.7
```

* Install the dependencies
```shell
pip install -r requirements.txt
```

* Launch the app using the built-in uvicorn server
```shell
uvicorn src.main:app --reload
```

* When done, you can clean the virtual environment using the following commands
```shell
pyenv deactivate

pyenv uninstall idoven-venv-3.11.7
```

## Testing

After installing dependencies, just run pytest to execute the tests.
```shell
pytest -v --cov tests
```
