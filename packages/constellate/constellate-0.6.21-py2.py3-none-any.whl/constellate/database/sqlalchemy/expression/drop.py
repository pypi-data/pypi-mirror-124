import sys
from typing import List, Union, Iterable

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import ClauseElement
from sqlalchemy.sql.base import Executable


class Drop(Executable, ClauseElement):
    def __init__(
        self,
        table: Union[object, List[object]] = None,
        if_exists: bool = False,
        cascade: bool = False,
    ):
        self.table = table
        self._option_if_exists = if_exists
        self._option_cascade = cascade


def _visit_drop_generic(element, compiler, max_table=0, db_type: str = None, **kw):
    if db_type == "sqlite":
        if element._option_cascade:
            raise ValueError("cascade not sqlite supported")

    pre_options = " ".join(
        filter(lambda x: x is not None, ["IF EXISTS" if element._option_if_exists else None])
    )
    post_options = " ".join(
        filter(lambda x: x is not None, ["CASCADE" if element._option_cascade else None])
    )

    tables = element.table if isinstance(element.table, Iterable) else [element.table]
    tables = [t for t in tables]
    if len(tables) > max_table:
        raise ValueError(f"Database supports no more than {max_table} dropped tables per statement")

    tables = ", ".join([compiler.process(t.__table__, asfrom=True, **kw) for t in tables])
    return "DROP TABLE %s %s %s" % (pre_options, tables, post_options)


@compiles(Drop)
def visit_drop(element, compiler, **kw):
    raise NotImplementedError()


@compiles(Drop, "postgresql")
def visit_drop(element, compiler, **kw):
    return _visit_drop_generic(element, compiler, max_table=sys.maxsize, db_type="postgresql", **kw)


@compiles(Drop, "sqlite")
def visit_drop(element, compiler, **kw):
    return _visit_drop_generic(element, compiler, max_table=1, db_type="sqlite", **kw)
