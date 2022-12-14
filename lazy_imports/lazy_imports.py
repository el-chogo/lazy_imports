import importlib

class LazyImportsError(Exception):
    pass

class ModuleAlreadyAdded(LazyImportsError):
    pass

class ModuleNotAdded(LazyImportsError):
    pass

class InvalidModule(LazyImportsError):
    pass

class ModuleNotLoaded:
    pass

class LazyImports:
    modules = {}
    aliases = {}
    cache = {}

    def add_module(self, module_name, alias=None):
        if alias is None:
            alias = module_name.split(".")[-1]

        if module_name in self.modules:
            raise ModuleAlreadyAdded

        self.modules[module_name] = ModuleNotLoaded()
        self.aliases[alias] = module_name

    def __getattr__(self, attr):
        if attr in self.cache:
            return self.cache[attr]

        if attr not in self.aliases:
            raise ModuleNotAdded

        module_name = self.aliases[attr]

        try:
            module_obj = importlib.import_module(module_name)
        except ModuleNotFoundError as e:
            raise InvalidModule from e

        self.cache[attr] = module_obj

        return module_obj

    def clear(self):
        self.modules = {}
        self.aliases = {}
        self.cache = {}

lazy_imports = LazyImports()
