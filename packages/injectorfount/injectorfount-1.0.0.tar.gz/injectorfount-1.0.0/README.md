# injector fount

An injector provider for injector package, adding a layer/wrapper to prepare and initialize then build the injector instance.

Basically a builder that builds a configuration first, then initialize when all is complete, used to add configurators on many levels of the application and then initializes when all configurators are added successfully.

So we end up with a multi-step builder, then we build our injector after all steps are complete, checkout [serviceregistry](https://github.com/0mars/serviceregistry) package on how to integrate this into a multi-step service locator, to provide a true dependency injection container with a service registry to python.

## usage
```python
from injectorfount import InjectorFount
from injector import singleton, provider, Module

# the configurator
class UseCasesConfigurator(Module):
    @singleton
    @provider
    def add_new(self) -> SearchBooksUseCase:
        return SearchBooksUseCase(
            self.__injector__.get(BookRepository)
        )


# the fount
fount = InjectorFount()

# here, we prepare the found with configurators to configure the actualy injector
fount.add_configurator(UseCasesConfigurator)


# get the injector
injector = fount.get_injector()

# have the injector get the service required
search_books_usecase = injector.get(SearchBooksUseCase)

```

## setup

```
pipenv install -e git+https://gitlab.com/bookla-foundation/injector-fount.git#egg=injectorfount
```
