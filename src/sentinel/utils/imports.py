from typing import Any, Tuple


def import_by_classpath(classpath: str) -> Tuple[str, Any]:
    """
    import by classpath
    """
    module_name, class_name = classpath.rsplit(".", 1)

    module = __import__(
        module_name,
        globals(),
        locals(),
        [
            class_name,
        ],
        0,
    )
    _class = getattr(module, class_name)

    return module_name, _class

