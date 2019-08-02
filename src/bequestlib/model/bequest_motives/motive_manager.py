from bequestlib.globals import BEQUEST_MODULE
from bequestlib.model.bequest_motives.optimizer_abc import AbstractUtilityOptimizer
import importlib


def get_utility_optimizer() -> AbstractUtilityOptimizer:
    optimizer_module = importlib.import_module(f'bequestlib.model.bequest_motives.{BEQUEST_MODULE}')
    return optimizer_module.UtilityOptimizer()
