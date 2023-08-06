# coding: utf8

__all__ = ["Definition"]

from typing import Optional

from ..data_grid._fundamental_class import Fundamental
from ...core.session import Session
from ...tools import create_str_definition
from ...tools._raise_exception import raise_exception_on_error


class Definition:
    """
    This class describe the universe (list of instruments), the fields (a.k.a. data items) and
    parameters that will be requested to the data platform

    Parameters:
    ----------
    universe : list
        The list of RICs
    fields : list
        List of fundamental field names
    parameters : dict, optional
        Global parameters for fields
    use_field_names_in_headers : bool, optional
        If value is True we add field names in headers.
    closure : str, optional
        Specifies the parameter that will be merged with the request
    extended_params : dict, optional
        Other parameters can be provided if necessary

    Examples
    --------
    >>> from refinitiv.data.content import fundamental_and_reference
    >>> definition = fundamental_and_reference.Definition(["IBM"], ["TR.Volume"])
    """

    def __init__(
        self,
        universe: list,
        fields: list,
        parameters: Optional[dict] = None,
        use_field_names_in_headers: Optional[bool] = False,
        closure: Optional[str] = None,
        extended_params: Optional[dict] = None,
    ):
        self.universe = universe
        self.fields = fields
        self.parameters = parameters
        self.use_field_names_in_headers = use_field_names_in_headers
        self.closure = closure
        self.extended_params = extended_params

    def __repr__(self):
        return create_str_definition(
            self,
            middle_path="content",
            content=f"{{name='{self.universe}'}}",
        )

    @raise_exception_on_error
    def get_data(self, session: Session = None, on_response=None):
        """
        Returns a response from the API to the library

        Parameters
        ----------
        session : Session, optional
            The Session defines the source where you want to retrieve your data
        on_response : Callable, optional
            Callable object to process retrieved data

        Returns
        -------
        Response

        Examples
        --------
        >>> from refinitiv.data.content import fundamental_and_reference
        >>> definition = fundamental_and_reference.Definition(["IBM"], ["TR.Volume"])
        >>> definition.get_data()
        """
        fundamental_class = Fundamental(session=session, on_response=on_response)
        response = fundamental_class._get_data(
            universe=self.universe,
            fields=self.fields,
            parameters=self.parameters,
            use_field_names_in_headers=self.use_field_names_in_headers,
            closure=self.closure,
            extended_params=self.extended_params,
        )

        return response

    @raise_exception_on_error
    async def get_data_async(self, session: Session = None, on_response=None):
        """
        Returns a response asynchronously from the API to the library

        Parameters
        ----------
        session : Session, optional
            The Session defines the source where you want to retrieve your data
        on_response : Callable, optional
            Callable object to process retrieved data

        Returns
        -------
        Response

        Examples
        --------
        >>> from refinitiv.data.content import fundamental_and_reference
        >>> definition = fundamental_and_reference.Definition(["IBM"], ["TR.Volume"])
        >>> await definition.get_data_async()
        """
        fundamental_class = Fundamental(session=session, on_response=on_response)
        response = await fundamental_class._get_data_async(
            universe=self.universe,
            fields=self.fields,
            parameters=self.parameters,
            use_field_names_in_headers=self.use_field_names_in_headers,
            closure=self.closure,
            extended_params=self.extended_params,
        )
        return response
