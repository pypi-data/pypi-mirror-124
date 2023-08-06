'''
# cdk-renovo-instance-service
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

import aws_cdk.aws_ec2
import aws_cdk.core


@jsii.interface(
    jsii_type="@renovosolutions/cdk-library-renovo-instance-service.IInstanceServiceProps"
)
class IInstanceServiceProps(typing_extensions.Protocol):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ami")
    def ami(self) -> aws_cdk.aws_ec2.IMachineImage:
        '''The Amazon Machine Image (AMI) to launch the target instance with.'''
        ...

    @ami.setter
    def ami(self, value: aws_cdk.aws_ec2.IMachineImage) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enableCloudwatchLogs")
    def enable_cloudwatch_logs(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to enable logging to Cloudwatch Logs.

        :default: true
        '''
        ...

    @enable_cloudwatch_logs.setter
    def enable_cloudwatch_logs(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _IInstanceServicePropsProxy:
    __jsii_type__: typing.ClassVar[str] = "@renovosolutions/cdk-library-renovo-instance-service.IInstanceServiceProps"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ami")
    def ami(self) -> aws_cdk.aws_ec2.IMachineImage:
        '''The Amazon Machine Image (AMI) to launch the target instance with.'''
        return typing.cast(aws_cdk.aws_ec2.IMachineImage, jsii.get(self, "ami"))

    @ami.setter
    def ami(self, value: aws_cdk.aws_ec2.IMachineImage) -> None:
        jsii.set(self, "ami", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enableCloudwatchLogs")
    def enable_cloudwatch_logs(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to enable logging to Cloudwatch Logs.

        :default: true
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enableCloudwatchLogs"))

    @enable_cloudwatch_logs.setter
    def enable_cloudwatch_logs(self, value: typing.Optional[builtins.bool]) -> None:
        jsii.set(self, "enableCloudwatchLogs", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IInstanceServiceProps).__jsii_proxy_class__ = lambda : _IInstanceServicePropsProxy


class InstanceService(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-renovo-instance-service.InstanceService",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        props: IInstanceServiceProps,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        jsii.create(self.__class__, self, [scope, id, props])


__all__ = [
    "IInstanceServiceProps",
    "InstanceService",
]

publication.publish()
