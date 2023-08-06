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
import aws_cdk.aws_events
import aws_cdk.aws_kinesis
import aws_cdk.aws_kms
import aws_cdk.core


class CompliantDynamoDb(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="compliantdynamodb.CompliantDynamoDb",
):
    '''Creates a DynamoDB table that is secured by an AWS backup plan und with point in time recovery enabled by default.'''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        props: typing.Optional["ICompliantDynamoDbProps"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dynamodbTable")
    def dynamodb_table(self) -> aws_cdk.aws_dynamodb.Table:
        return typing.cast(aws_cdk.aws_dynamodb.Table, jsii.get(self, "dynamodbTable"))


@jsii.interface(jsii_type="compliantdynamodb.ICompliantDynamoDbProps")
class ICompliantDynamoDbProps(typing_extensions.Protocol):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupPlanStartTime")
    def backup_plan_start_time(self) -> typing.Optional[aws_cdk.aws_events.Schedule]:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupVaultName")
    def backup_vault_name(self) -> typing.Optional[builtins.str]:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="contributorInsightsEnabled")
    def contributor_insights_enabled(self) -> typing.Optional[builtins.bool]:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.Key]:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="kinesisStream")
    def kinesis_stream(self) -> typing.Optional[aws_cdk.aws_kinesis.Stream]:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="partitionKey")
    def partition_key(self) -> typing.Optional[aws_cdk.aws_dynamodb.Attribute]:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="replicationRegions")
    def replication_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="replicationTimeout")
    def replication_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sortKey")
    def sort_key(self) -> typing.Optional[aws_cdk.aws_dynamodb.Attribute]:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> typing.Optional[builtins.str]:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="timeToLiveAttribute")
    def time_to_live_attribute(self) -> typing.Optional[builtins.str]:
        ...


class _ICompliantDynamoDbPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "compliantdynamodb.ICompliantDynamoDbProps"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupPlanStartTime")
    def backup_plan_start_time(self) -> typing.Optional[aws_cdk.aws_events.Schedule]:
        return typing.cast(typing.Optional[aws_cdk.aws_events.Schedule], jsii.get(self, "backupPlanStartTime"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupVaultName")
    def backup_vault_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupVaultName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="contributorInsightsEnabled")
    def contributor_insights_enabled(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "contributorInsightsEnabled"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.Key]:
        return typing.cast(typing.Optional[aws_cdk.aws_kms.Key], jsii.get(self, "encryptionKey"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="kinesisStream")
    def kinesis_stream(self) -> typing.Optional[aws_cdk.aws_kinesis.Stream]:
        return typing.cast(typing.Optional[aws_cdk.aws_kinesis.Stream], jsii.get(self, "kinesisStream"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="partitionKey")
    def partition_key(self) -> typing.Optional[aws_cdk.aws_dynamodb.Attribute]:
        return typing.cast(typing.Optional[aws_cdk.aws_dynamodb.Attribute], jsii.get(self, "partitionKey"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="replicationRegions")
    def replication_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "replicationRegions"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="replicationTimeout")
    def replication_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        return typing.cast(typing.Optional[aws_cdk.core.Duration], jsii.get(self, "replicationTimeout"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sortKey")
    def sort_key(self) -> typing.Optional[aws_cdk.aws_dynamodb.Attribute]:
        return typing.cast(typing.Optional[aws_cdk.aws_dynamodb.Attribute], jsii.get(self, "sortKey"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="timeToLiveAttribute")
    def time_to_live_attribute(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeToLiveAttribute"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICompliantDynamoDbProps).__jsii_proxy_class__ = lambda : _ICompliantDynamoDbPropsProxy


__all__ = [
    "CompliantDynamoDb",
    "ICompliantDynamoDbProps",
]

publication.publish()
