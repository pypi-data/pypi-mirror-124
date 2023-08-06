#!/usr/bin/env python3
# --------------------( LICENSE                           )--------------------
# Copyright (c) 2014-2021 Beartype authors.
# See "LICENSE" for further details.

'''
Project-wide :pep:`484`-compliant PEP-noncompliant type hint test data.

:pep:`484`-compliant type hints *mostly* indistinguishable from
PEP-noncompliant type hints include:

* :func:`typing.NamedTuple`, a high-level factory function deferring to the
  lower-level :func:`collections.namedtuple` factory function creating and
  returning :class:`tuple` instances annotated by PEP-compliant type hints.
* :func:`typing.TypedDict`, a high-level factory function creating and
  returning :class:`dict` instances annotated by PEP-compliant type hints.
'''

# ....................{ IMPORTS                           }....................
from beartype_test.a00_unit.data.hint.util.data_hintmetacls import (
    HintNonpepMetadata,
    HintPithSatisfiedMetadata,
    HintPithUnsatisfiedMetadata,
)
from typing import (
    NamedTuple,
)

# ....................{ GLOBALS                           }....................
NamedTupleType = NamedTuple(
    'NamedTupleType', [('fumarole', str), ('enrolled', int)])
'''
PEP-compliant user-defined :func:`collections.namedtuple` instance typed with
PEP-compliant annotations.
'''

# ....................{ ADDERS                            }....................
def add_data(data_module: 'ModuleType') -> None:
    '''
    Add :pep:`484`**-compliant PEP-noncompliant type hint test data to various
    global containers declared by the passed module.

    Parameters
    ----------
    data_module : ModuleType
        Module to be added to.
    '''

    # ..................{ TUPLES                            }..................
    # Add PEP 484-specific PEP-noncompliant test type hints to this dictionary
    # global.
    data_module.HINTS_NONPEP_META.extend((
        # ................{ NAMEDTUPLE                        }................
        # "NamedTuple" instances transparently reduce to standard tuples and
        # *MUST* thus be handled as non-"typing" type hints.
        HintNonpepMetadata(
            hint=NamedTupleType,
            piths_satisfied_meta=(
                # Named tuple containing correctly typed items.
                HintPithSatisfiedMetadata(
                    NamedTupleType(fumarole='Leviathan', enrolled=37)),
            ),
            piths_unsatisfied_meta=(
                # String constant.
                HintPithUnsatisfiedMetadata('Of ͼarthen concordance that'),

                #FIXME: Uncomment after implementing "NamedTuple" support.
                # # Named tuple containing incorrectly typed items.
                # HintPithUnsatisfiedMetadata(
                #     pith=NamedTupleType(fumarole='Leviathan', enrolled=37),
                #     # Match that the exception message raised for this object...
                #     exception_str_match_regexes=(
                #         # Declares the name of this tuple's problematic item.
                #         r'\s[Ll]ist item 0\s',
                #     ),
                # ),
            ),
        ),

        # ................{ COLLECTIONS ~ typeddict           }................
        # "TypedDict" instances transparently reduce to dicts.
        #FIXME: Implement us up, but note when doing so that "TypedDict" was
        #first introduced with Python 3.8.
    ))
