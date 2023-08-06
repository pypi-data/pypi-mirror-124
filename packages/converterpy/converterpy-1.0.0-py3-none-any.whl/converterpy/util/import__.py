import importlib
import sys

from converterpy.util.logger import LogManager


def import_class(base_path, module_name, class_name, **kwargs):
    LogManager.get_logger().debug("Reading module [%s] at [%s], class: [%s]" % (base_path, module_name, class_name))
    sys.path.append(base_path)

    module = importlib.import_module(module_name)

    return getattr(module, class_name)
