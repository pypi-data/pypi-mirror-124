# coding: utf-8

__all__ = ["Definition"]

from typing import Any, Optional, TYPE_CHECKING

from .stream import Stream
from ...tools import create_str_definition

if TYPE_CHECKING:
    from ...core.session import Session


class Definition(object):
    """
    Class is designed to request streaming chains and decode it dynamically

    Parameters
    ----------
    name : str
        Single instrument name
    closure : Any, optional
        Specifies the parameter that will be merged with the request
    service : str, optional
        Name service
    skip_summary_links : bool, optional
        Store skip summary links
    skip_empty : bool, optional
        Store skip empty
    override_summary_links : int, optional
        Store the override number of summary links

    Examples
    --------
    >>> from refinitiv.data.content.pricing import chain
    >>> definition_chain = chain.Definition("EUR")
    """

    def __init__(
        self,
        name: str,
        closure: Any = None,
        service: Optional[str] = None,
        # option for chain constituents
        skip_summary_links: Optional[bool] = True,
        skip_empty: Optional[bool] = True,
        override_summary_links: Optional[int] = None,
    ):
        self._name = name
        self._closure = closure
        self._service = service
        self._skip_summary_links = skip_summary_links
        self._skip_empty = skip_empty
        self._override_summary_links = override_summary_links

    def __repr__(self):
        return create_str_definition(
            self,
            middle_path="content",
            end_path="pricing.chain",
            content=f"{{name='{self._name}'}}",
        )

    def get_stream(
        self,
        session: "Session" = None,
    ) -> Stream:
        """
        Return a chain.Stream object for the defined data

        Parameters
        ----------
        session : Session, optional
            The Session defines the source where you want to retrieve your data

        Returns
        -------
        chain.Stream

        Examples
        -------
        Create a chain.Stream object

        >>> from refinitiv.data.content.pricing import chain
        >>> definition_chain = chain.Definition("EUR")
        >>> chain_stream = definition_chain.get_stream()

        Open the Stream connection

        >>> from refinitiv.data.content.pricing import chain
        >>> definition_chain = chain.Definition("EUR")
        >>> chain_stream = definition_chain.get_stream()
        >>> chain_stream.open()

        Closes the Stream connection

        >>> from refinitiv.data.content.pricing import chain
        >>> definition_chain = chain.Definition("EUR")
        >>> chain_stream = definition_chain.get_stream()
        >>> chain_stream.open()
        >>> chain_stream.close()

        Call constituents

        >>> from refinitiv.data.content.pricing import chain
        >>> definition_chain = chain.Definition("EUR")
        >>> chain_stream = definition_chain.get_stream()
        >>> chain_stream.open()
        >>> chain_stream.constituents

        Call property is_chain

        >>> from refinitiv.data.content.pricing import chain
        >>> definition_chain = chain.Definition("EUR")
        >>> chain_stream = definition_chain.get_stream()
        >>> chain_stream.open()
        >>> chain_stream.is_chain
        """
        stream = Stream(
            name=self._name,
            session=session,
            service=self._service,
            skip_summary_links=self._skip_summary_links,
            skip_empty=self._skip_empty,
            override_summary_links=self._override_summary_links,
        )
        return stream
