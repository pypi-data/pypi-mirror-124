'''
# replace this

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
hello = []
```
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
    jsii_type="compliantdynamodb.CompliantDynamoDb",
):
    '''
    :description:

    creates a DynamoDB table that is secured by an AWS backup plan und with point in time recovery
    enabled by default.
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        backup_vault_name: typing.Optional[builtins.str] = None,
        billing_mode: typing.Optional[aws_cdk.aws_dynamodb.BillingMode] = None,
        partition_key: typing.Optional[aws_cdk.aws_dynamodb.Attribute] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param backup_vault_name: 
        :param billing_mode: 
        :param partition_key: 
        :param table_name: 
        '''
        props = CompliantDynamoDbProps(
            backup_vault_name=backup_vault_name,
            billing_mode=billing_mode,
            partition_key=partition_key,
            table_name=table_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dynamodbTable")
    def dynamodb_table(self) -> aws_cdk.aws_dynamodb.Table:
        return typing.cast(aws_cdk.aws_dynamodb.Table, jsii.get(self, "dynamodbTable"))


@jsii.data_type(
    jsii_type="compliantdynamodb.CompliantDynamoDbProps",
    jsii_struct_bases=[],
    name_mapping={
        "backup_vault_name": "backupVaultName",
        "billing_mode": "billingMode",
        "partition_key": "partitionKey",
        "table_name": "tableName",
    },
)
class CompliantDynamoDbProps:
    def __init__(
        self,
        *,
        backup_vault_name: typing.Optional[builtins.str] = None,
        billing_mode: typing.Optional[aws_cdk.aws_dynamodb.BillingMode] = None,
        partition_key: typing.Optional[aws_cdk.aws_dynamodb.Attribute] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param backup_vault_name: 
        :param billing_mode: 
        :param partition_key: 
        :param table_name: 
        '''
        if isinstance(partition_key, dict):
            partition_key = aws_cdk.aws_dynamodb.Attribute(**partition_key)
        self._values: typing.Dict[str, typing.Any] = {}
        if backup_vault_name is not None:
            self._values["backup_vault_name"] = backup_vault_name
        if billing_mode is not None:
            self._values["billing_mode"] = billing_mode
        if partition_key is not None:
            self._values["partition_key"] = partition_key
        if table_name is not None:
            self._values["table_name"] = table_name

    @builtins.property
    def backup_vault_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("backup_vault_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def billing_mode(self) -> typing.Optional[aws_cdk.aws_dynamodb.BillingMode]:
        result = self._values.get("billing_mode")
        return typing.cast(typing.Optional[aws_cdk.aws_dynamodb.BillingMode], result)

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
