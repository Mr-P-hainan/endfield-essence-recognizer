import importlib.metadata

try:
    __version__ = importlib.metadata.version("endfield-essence-recognizer")
except importlib.metadata.PackageNotFoundError:
    __version__ = None
