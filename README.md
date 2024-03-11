Python Advanced

- `getattr`  `setattr`
- 不能重写 delattr 函数，这是一个 Python 的内建函数，用户不能修改。在调用 delattr(obj, "attr") 时，Python 会转而调用 obj.__delattr__("attr") 方法，所以你可以通过重写 __delattr__ 方法来改变 delattr 的行为。
- monkey patch:
  - The easiest mistake to make http://www.gregreda.com/2021/06/28/mocking-imported-module-function-python/ 
  view [minimal_patch_example](minimal_patch_example)
- with statement `__enter__` `__exit__`
- function parameter `inspect.signature(fn).parameters`
  - check version: `"gradient_checkpointing_kwargs" in list(inspect.signature(model.gradient_checkpointing_enable).parameters)`
- context manager
- yield
- `pyproject.toml` contains build system requirements and information, which are used by pip to build the package. that is, when `pip install -e .` , it use pyproject's environment to build package, so `The detected CUDA version (11.8) mismatches the version that was used to compile PyTorch (12.1). Please make sure to use the same CUDA versions.` means `pyproject.toml` has torch-cuda12.1
- Python 函数里边只要存在对全局变量的赋值，不管是否动态执行到，都会自动把该变量名自动创建local的，和原来的全局完全无关 所以需要提前声明 `global` 或者 `nonlocal`
