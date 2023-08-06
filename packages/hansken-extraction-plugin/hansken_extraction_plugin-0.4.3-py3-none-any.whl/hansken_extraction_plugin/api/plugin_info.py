"""This module contains all definitions to describe meta data of a plugin, a.k.a. PluginInfo."""
from enum import Enum
from typing import Any

from attr import dataclass


@dataclass
class Author:
    """
    The author of an Extraction Plugin.

    This information can be retrieved by an end-user from Hansken.
    """

    name: str
    email: str
    organisation: str


class MaturityLevel(Enum):
    """This class represents the maturity level of an extraction plugin."""

    PROOF_OF_CONCEPT = 0
    READY_FOR_TEST = 1
    PRODUCTION_READY = 2


@dataclass
class PluginId:
    """Identifier of a plugin, consisting of domain, category and name. Needs to be unique among all tools/plugins."""

    domain: str
    category: str
    name: str


class PluginInfo:
    """This information is used by Hansken to identify and run the plugin."""

    plugin: Any  # noqa
    version: str
    description: str
    author: Author
    maturity: MaturityLevel
    matcher: str
    webpage_url: str
    id: PluginId
    license: str
    deferred_iterations: int

    def __init__(self, plugin, version, description, author, maturity, matcher, webpage_url, id, license=None,
                 deferred_iterations=1):
        """
        Initialize a PluginInfo.

        :param plugin: the plugin that returns this plugininfo, pass self
        :param version: version of the plugin
        :param description: short description of the functionality of the plugin
        :param author: the author, this is an Author object
        :param maturity: maturitylevel, see enum
        :param matcher: this matcher selects the traces offered to the plugin
        :param webpage_url: plugin url
        :param id: PluginId consisting of domain, category of name. this combination should be unique for every plugin
        :param license: license of this plugin
        :param deferred_iterations: Optional, number of deferred iterations. Only for deferred plugins.
                                    Number should be between 1 and 20.
        """
        self.plugin = plugin
        self.version = version
        self.description = description
        self.author = author
        self.maturity = maturity
        self.matcher = matcher
        self.webpage_url = webpage_url
        self.id = id
        self.license = license
        self.deferred_iterations = deferred_iterations

        if not 1 <= self.deferred_iterations <= 20:
            raise ValueError(f'Invalid value for deferredIterations: {self.deferred_iterations}. '
                             f'Valid values are 1 =< 20.')
