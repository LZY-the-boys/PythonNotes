
class _patch(object):

    def __init__(
        self,
        getter,
        attribute,
        new,
    ):
        self.getter = getter
        self.attribute = attribute
        self.new = new
        self.has_local = False
        self.additional_patchers = []

    def __enter__(self):
        """Perform the patch."""
        self.target = self.getter()
        original = self.target.__dict__[self.attribute]
        self.temp_original = original
        setattr(self.target, self.attribute, self.new)
        return self.new

    def __exit__(self, *exc_info):
        """Undo the patch."""
        setattr(self.target, self.attribute, self.temp_original)

def _importer(target):
    components = target.split('.')
    import_path = components.pop(0)
    thing = __import__(import_path)

    for comp in components:
        import_path += ".%s" % comp
        try:
            thing= getattr(thing, comp)
        except AttributeError:
            __import__(import_path)
            thing= getattr(thing, comp)

    return thing

def patch(target, new):
    target, attribute = target.rsplit('.', 1)
    getter = lambda: _importer(target)
    return _patch(
        getter,
        attribute,
        new,
    )