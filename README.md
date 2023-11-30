Python Advanced

- `+-*/` implement: `__add__, __radd__, __neg__`
- `getattr`  `setattr`
- monkey patch:
  - The easiest mistake to make http://www.gregreda.com/2021/06/28/mocking-imported-module-function-python/ 
  view [minimal_patch_example](minimal_patch_example)
- with statement `__enter__` `__exit__`
- function parameter `inspect.signature(fn).parameters`
  - check version: `"gradient_checkpointing_kwargs" in list(inspect.signature(model.gradient_checkpointing_enable).parameters)`
- context manager
- yield
- `pyproject.toml` contains build system requirements and information, which are used by pip to build the package. that is, when `pip install -e .` , it use pyproject's environment to build package, so `The detected CUDA version (11.8) mismatches the version that was used to compile PyTorch (12.1). Please make sure to use the same CUDA versions.` means `pyproject.toml` has torch-cuda12.1
