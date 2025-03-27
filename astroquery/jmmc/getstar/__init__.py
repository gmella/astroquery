# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
JMMC GetStar Query Tool
-------------------
Query the JMMC GetStar service
https://www.jmmc.fr/getstar

:Author: Guillaume Mella (jmmc-tech-group@jmmc.fr)
"""
from astropy import config as _config


class Conf(_config.ConfigNamespace):
    """
    Configuration parameters for `astroquery.jmmc.getstar`.
    """
    server = _config.ConfigItem(
        ['https://astroquery.jmmc.fr/getstar',
        ],
        'GetStar server to use.')

    timeout = _config.ConfigItem(
        30,
        'Time limit for connecting to template_module server.')


conf = Conf()

from .core import GetStar

__all__ = ['GetStar',
           'Conf', 'conf',
           ]
