"""
Modified version of mkdocs.config.config_options.ConfigItems,
see https://github.com/mkdocs/mkdocs/blob/master/mkdocs/config/config_options.py
for the original implementation.
"""
__all__ = ("ConfigItems",)

from collections import Sequence

from mkdocs.config.base import ValidationError
from mkdocs.config.config_options import BaseConfigOption, SubConfig

class ConfigItems(BaseConfigOption):
    """
    Config Items Option

    Validates a list of mappings that all must match the same set of
    options.
    """
    def __init__(self, *config_options, **kwargs):
        BaseConfigOption.__init__(self)
        self.item_config_options = config_options
        self.required = kwargs.get('required', False)
    @property
    def item_config(self):
        return SubConfig(*self.item_config_options)

    def __repr__(self):
        return '{}: {}'.format(self.__class__.__name__, self.item_config)

    def run_validation(self, value):
        if value is None:
            if self.required:
                raise ValidationError("Required configuration not provided.")
            else:
                return ()

        if not isinstance(value, Sequence):
            raise ValidationError('Expected a sequence of mappings, but a %s '
                                  'was given.' % type(value))
        result = []
        for item in value:
            if len(item) != 1:
                raise ValidationError("Expected a sequence of mappings with one item each, got {0}".format(len(item)))
            result.append(dict((k, self.item_config.validate(v)) for k,v in item.items()))
        return result
