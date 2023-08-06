'''
# replace this

# Python

* run `python3 -m venv .env` an than pj
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *


@jsii.data_type(
    jsii_type="prowler-sdk-poc.Chek73Props",
    jsii_struct_bases=[],
    name_mapping={"white_listed_bucket_names": "whiteListedBucketNames"},
)
class Chek73Props:
    def __init__(
        self,
        *,
        white_listed_bucket_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param white_listed_bucket_names: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if white_listed_bucket_names is not None:
            self._values["white_listed_bucket_names"] = white_listed_bucket_names

    @builtins.property
    def white_listed_bucket_names(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("white_listed_bucket_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Chek73Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Chek73Props",
]

publication.publish()
