from bequestlib.globals import settings
from bequestlib.model.bequest_motives.optimizer_abc import AbstractUtilityOptimizer
import importlib


def get_utility_optimizer() -> AbstractUtilityOptimizer:
    module_name = f'bequestlib.model.bequest_motives.{settings.BEQUEST_MODULE}'
    optimizer_module = importlib.import_module(module_name)
    return optimizer_module.UtilityOptimizer()
