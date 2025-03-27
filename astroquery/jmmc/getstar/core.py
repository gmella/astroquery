# Licensed under a 3-clause BSD style license - see LICENSE.rst

import astropy.io.votable as votable
from io import BytesIO, StringIO


from astropy.table import Table
from urllib.parse import quote as urlencode


# local imports - use relative imports
from ...query import BaseQuery
# has common functions required by most modules
from ...utils import commons
# prepend_docstr is a way to copy docstrings between methods
from ...utils import prepend_docstr_nosections
# async_to_sync generates the relevant query tools from _async methods
from ...utils import async_to_sync
# import configurable items declared in __init__.py
from . import conf

import numpy as np


# export all the public classes and methods
__all__ = ['GetStar', 'GetStarClass']

# declare global variables and constants if any

@async_to_sync
class GetStarClass(BaseQuery):
    object_name_sep = ','
    maxBatchSize = 100

    # TODO limit size of names or split accross chunk

    def query_object_async(self, object_names, *, get_query_payload=False,
                           cache=True):
        """
        This method query the object name (TODO object_names).

        Parameters
        ----------
        object_names : [list of str]
            name of the identifier(s) to query.
        get_query_payload : bool, optional
            This should default to False. When set to `True` the method
            should return the HTTP request parameters as a dict.
        verbose : bool, optional
           This should default to `False`, when set to `True` it displays
           VOTable warnings.

        Returns
        -------
        response : `requests.Response`
            The HTTP response with raw votable as content.

        Examples
        --------
        While this section is optional you may put in some examples that
        show how to use the method. The examples are written similar to
        standard doctests in python.

        """
        request_payload = self._args_to_payload(object_names=object_names)

        if get_query_payload:
            return request_payload

        response = self._request('GET', conf.server, params=request_payload,
                                 timeout=conf.timeout, cache=cache)

        return response

    def _args_to_payload(self, *args, **kwargs):
        request_payload = dict()
        object_names = kwargs.get("object_names")

        if not isinstance(object_names,(list, tuple, np.ndarray)):
            raise ValueError("object_names must be a list of target names")

        if len(object_names)>self.maxBatchSize:
            raise ValueError(f"object_names must not be larger than {self.maxBatchSize}")

        request_payload["star"] = self.object_name_sep.join(object_names)

        return request_payload

    def _parse_result(self, response, *, verbose=False):
        if not verbose:
            commons.suppress_vo_warnings()
        # try to parse the result into an astropy.Table, else
        # return the raw result with an informative error message.
        try:
            return commons.parse_votable(response.content).get_first_table().to_table(use_names_over_ids=True)
        except ValueError:
            # catch common errors here, but never use bare excepts
            # return raw result/ handle in some way
            pass

        return response


# the default tool for users to interact with is an instance of the Class
GetStar = GetStarClass()

# TODO
# - think about providing the query_region method.
# - tests should be written : see ./tests for examples on this
# - write the docs in astroquery/docs/module_name using Sphinx.