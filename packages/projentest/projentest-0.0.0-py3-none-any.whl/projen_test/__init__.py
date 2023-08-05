'''
# replace this
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

import aws_cdk.aws_dynamodb
import aws_cdk.core


class CompliantDynamoDb(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="compliantDynamodb.CompliantDynamoDb",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        partition_key: typing.Optional[aws_cdk.aws_dynamodb.Attribute] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param partition_key: 
        :param table_name: 
        '''
        props = CompliantDynamoDbProps(
            partition_key=partition_key, table_name=table_name
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="compliantDynamodb.CompliantDynamoDbProps",
    jsii_struct_bases=[],
    name_mapping={"partition_key": "partitionKey", "table_name": "tableName"},
)
class CompliantDynamoDbProps:
    def __init__(
        self,
        *,
        partition_key: typing.Optional[aws_cdk.aws_dynamodb.Attribute] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param partition_key: 
        :param table_name: 
        '''
        if isinstance(partition_key, dict):
            partition_key = aws_cdk.aws_dynamodb.Attribute(**partition_key)
        self._values: typing.Dict[str, typing.Any] = {}
        if partition_key is not None:
            self._values["partition_key"] = partition_key
        if table_name is not None:
            self._values["table_name"] = table_name

    @builtins.property
    def partition_key(self) -> typing.Optional[aws_cdk.aws_dynamodb.Attribute]:
        result = self._values.get("partition_key")
        return typing.cast(typing.Optional[aws_cdk.aws_dynamodb.Attribute], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CompliantDynamoDbProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CompliantDynamoDb",
    "CompliantDynamoDbProps",
]

publication.publish()
