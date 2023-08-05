import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

import cdktf
import constructs


class AppstreamFleet(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.AppStream.AppstreamFleet",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html aws_appstream_fleet}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        compute_capacity: "AppstreamFleetComputeCapacity",
        instance_type: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        display_name: typing.Optional[builtins.str] = None,
        domain_join_info: typing.Optional["AppstreamFleetDomainJoinInfo"] = None,
        enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        fleet_type: typing.Optional[builtins.str] = None,
        iam_role_arn: typing.Optional[builtins.str] = None,
        idle_disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        image_arn: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        max_user_duration_in_seconds: typing.Optional[jsii.Number] = None,
        stream_view: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags_all: typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        vpc_config: typing.Optional["AppstreamFleetVpcConfig"] = None,
        count: typing.Optional[typing.Union[jsii.Number, cdktf.IResolvable]] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html aws_appstream_fleet} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param compute_capacity: compute_capacity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#compute_capacity AppstreamFleet#compute_capacity}
        :param instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#instance_type AppstreamFleet#instance_type}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#name AppstreamFleet#name}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#description AppstreamFleet#description}.
        :param disconnect_timeout_in_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#disconnect_timeout_in_seconds AppstreamFleet#disconnect_timeout_in_seconds}.
        :param display_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#display_name AppstreamFleet#display_name}.
        :param domain_join_info: domain_join_info block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#domain_join_info AppstreamFleet#domain_join_info}
        :param enable_default_internet_access: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#enable_default_internet_access AppstreamFleet#enable_default_internet_access}.
        :param fleet_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#fleet_type AppstreamFleet#fleet_type}.
        :param iam_role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#iam_role_arn AppstreamFleet#iam_role_arn}.
        :param idle_disconnect_timeout_in_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#idle_disconnect_timeout_in_seconds AppstreamFleet#idle_disconnect_timeout_in_seconds}.
        :param image_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#image_arn AppstreamFleet#image_arn}.
        :param image_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#image_name AppstreamFleet#image_name}.
        :param max_user_duration_in_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#max_user_duration_in_seconds AppstreamFleet#max_user_duration_in_seconds}.
        :param stream_view: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#stream_view AppstreamFleet#stream_view}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#tags AppstreamFleet#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#tags_all AppstreamFleet#tags_all}.
        :param vpc_config: vpc_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#vpc_config AppstreamFleet#vpc_config}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = AppstreamFleetConfig(
            compute_capacity=compute_capacity,
            instance_type=instance_type,
            name=name,
            description=description,
            disconnect_timeout_in_seconds=disconnect_timeout_in_seconds,
            display_name=display_name,
            domain_join_info=domain_join_info,
            enable_default_internet_access=enable_default_internet_access,
            fleet_type=fleet_type,
            iam_role_arn=iam_role_arn,
            idle_disconnect_timeout_in_seconds=idle_disconnect_timeout_in_seconds,
            image_arn=image_arn,
            image_name=image_name,
            max_user_duration_in_seconds=max_user_duration_in_seconds,
            stream_view=stream_view,
            tags=tags,
            tags_all=tags_all,
            vpc_config=vpc_config,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="putComputeCapacity")
    def put_compute_capacity(self, *, desired_instances: jsii.Number) -> None:
        '''
        :param desired_instances: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#desired_instances AppstreamFleet#desired_instances}.
        '''
        value = AppstreamFleetComputeCapacity(desired_instances=desired_instances)

        return typing.cast(None, jsii.invoke(self, "putComputeCapacity", [value]))

    @jsii.member(jsii_name="putDomainJoinInfo")
    def put_domain_join_info(
        self,
        *,
        directory_name: typing.Optional[builtins.str] = None,
        organizational_unit_distinguished_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param directory_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#directory_name AppstreamFleet#directory_name}.
        :param organizational_unit_distinguished_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#organizational_unit_distinguished_name AppstreamFleet#organizational_unit_distinguished_name}.
        '''
        value = AppstreamFleetDomainJoinInfo(
            directory_name=directory_name,
            organizational_unit_distinguished_name=organizational_unit_distinguished_name,
        )

        return typing.cast(None, jsii.invoke(self, "putDomainJoinInfo", [value]))

    @jsii.member(jsii_name="putVpcConfig")
    def put_vpc_config(
        self,
        *,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param security_group_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#security_group_ids AppstreamFleet#security_group_ids}.
        :param subnet_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#subnet_ids AppstreamFleet#subnet_ids}.
        '''
        value = AppstreamFleetVpcConfig(
            security_group_ids=security_group_ids, subnet_ids=subnet_ids
        )

        return typing.cast(None, jsii.invoke(self, "putVpcConfig", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisconnectTimeoutInSeconds")
    def reset_disconnect_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisconnectTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetDomainJoinInfo")
    def reset_domain_join_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainJoinInfo", []))

    @jsii.member(jsii_name="resetEnableDefaultInternetAccess")
    def reset_enable_default_internet_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableDefaultInternetAccess", []))

    @jsii.member(jsii_name="resetFleetType")
    def reset_fleet_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFleetType", []))

    @jsii.member(jsii_name="resetIamRoleArn")
    def reset_iam_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIamRoleArn", []))

    @jsii.member(jsii_name="resetIdleDisconnectTimeoutInSeconds")
    def reset_idle_disconnect_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdleDisconnectTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetImageArn")
    def reset_image_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageArn", []))

    @jsii.member(jsii_name="resetImageName")
    def reset_image_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageName", []))

    @jsii.member(jsii_name="resetMaxUserDurationInSeconds")
    def reset_max_user_duration_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxUserDurationInSeconds", []))

    @jsii.member(jsii_name="resetStreamView")
    def reset_stream_view(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStreamView", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetVpcConfig")
    def reset_vpc_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcConfig", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="computeCapacity")
    def compute_capacity(self) -> "AppstreamFleetComputeCapacityOutputReference":
        return typing.cast("AppstreamFleetComputeCapacityOutputReference", jsii.get(self, "computeCapacity"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="createdTime")
    def created_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdTime"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="domainJoinInfo")
    def domain_join_info(self) -> "AppstreamFleetDomainJoinInfoOutputReference":
        return typing.cast("AppstreamFleetDomainJoinInfoOutputReference", jsii.get(self, "domainJoinInfo"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(self) -> "AppstreamFleetVpcConfigOutputReference":
        return typing.cast("AppstreamFleetVpcConfigOutputReference", jsii.get(self, "vpcConfig"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="computeCapacityInput")
    def compute_capacity_input(
        self,
    ) -> typing.Optional["AppstreamFleetComputeCapacity"]:
        return typing.cast(typing.Optional["AppstreamFleetComputeCapacity"], jsii.get(self, "computeCapacityInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="disconnectTimeoutInSecondsInput")
    def disconnect_timeout_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "disconnectTimeoutInSecondsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="domainJoinInfoInput")
    def domain_join_info_input(self) -> typing.Optional["AppstreamFleetDomainJoinInfo"]:
        return typing.cast(typing.Optional["AppstreamFleetDomainJoinInfo"], jsii.get(self, "domainJoinInfoInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enableDefaultInternetAccessInput")
    def enable_default_internet_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "enableDefaultInternetAccessInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fleetTypeInput")
    def fleet_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fleetTypeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="iamRoleArnInput")
    def iam_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamRoleArnInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idleDisconnectTimeoutInSecondsInput")
    def idle_disconnect_timeout_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "idleDisconnectTimeoutInSecondsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="imageArnInput")
    def image_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageArnInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="imageNameInput")
    def image_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageNameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="maxUserDurationInSecondsInput")
    def max_user_duration_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUserDurationInSecondsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="streamViewInput")
    def stream_view_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streamViewInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "tagsAllInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tagsInput")
    def tags_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "tagsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpcConfigInput")
    def vpc_config_input(self) -> typing.Optional["AppstreamFleetVpcConfig"]:
        return typing.cast(typing.Optional["AppstreamFleetVpcConfig"], jsii.get(self, "vpcConfigInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        jsii.set(self, "instanceType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="disconnectTimeoutInSeconds")
    def disconnect_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "disconnectTimeoutInSeconds"))

    @disconnect_timeout_in_seconds.setter
    def disconnect_timeout_in_seconds(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        jsii.set(self, "disconnectTimeoutInSeconds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "displayName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enableDefaultInternetAccess")
    def enable_default_internet_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "enableDefaultInternetAccess"))

    @enable_default_internet_access.setter
    def enable_default_internet_access(
        self,
        value: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]],
    ) -> None:
        jsii.set(self, "enableDefaultInternetAccess", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fleetType")
    def fleet_type(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fleetType"))

    @fleet_type.setter
    def fleet_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "fleetType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="iamRoleArn")
    def iam_role_arn(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamRoleArn"))

    @iam_role_arn.setter
    def iam_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "iamRoleArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idleDisconnectTimeoutInSeconds")
    def idle_disconnect_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "idleDisconnectTimeoutInSeconds"))

    @idle_disconnect_timeout_in_seconds.setter
    def idle_disconnect_timeout_in_seconds(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        jsii.set(self, "idleDisconnectTimeoutInSeconds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="imageArn")
    def image_arn(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageArn"))

    @image_arn.setter
    def image_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "imageArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "imageName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="maxUserDurationInSeconds")
    def max_user_duration_in_seconds(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUserDurationInSeconds"))

    @max_user_duration_in_seconds.setter
    def max_user_duration_in_seconds(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "maxUserDurationInSeconds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="streamView")
    def stream_view(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streamView"))

    @stream_view.setter
    def stream_view(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "streamView", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        jsii.set(self, "tags", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tagsAll")
    def tags_all(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        jsii.set(self, "tagsAll", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.AppStream.AppstreamFleetComputeCapacity",
    jsii_struct_bases=[],
    name_mapping={"desired_instances": "desiredInstances"},
)
class AppstreamFleetComputeCapacity:
    def __init__(self, *, desired_instances: jsii.Number) -> None:
        '''
        :param desired_instances: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#desired_instances AppstreamFleet#desired_instances}.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "desired_instances": desired_instances,
        }

    @builtins.property
    def desired_instances(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#desired_instances AppstreamFleet#desired_instances}.'''
        result = self._values.get("desired_instances")
        assert result is not None, "Required property 'desired_instances' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppstreamFleetComputeCapacity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppstreamFleetComputeCapacityOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.AppStream.AppstreamFleetComputeCapacityOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.ITerraformResource,
        terraform_attribute: builtins.str,
        is_single_item: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param is_single_item: True if this is a block, false if it's a list.
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, is_single_item])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="desiredInstancesInput")
    def desired_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "desiredInstancesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="desiredInstances")
    def desired_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "desiredInstances"))

    @desired_instances.setter
    def desired_instances(self, value: jsii.Number) -> None:
        jsii.set(self, "desiredInstances", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.AppStream.AppstreamFleetConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "compute_capacity": "computeCapacity",
        "instance_type": "instanceType",
        "name": "name",
        "description": "description",
        "disconnect_timeout_in_seconds": "disconnectTimeoutInSeconds",
        "display_name": "displayName",
        "domain_join_info": "domainJoinInfo",
        "enable_default_internet_access": "enableDefaultInternetAccess",
        "fleet_type": "fleetType",
        "iam_role_arn": "iamRoleArn",
        "idle_disconnect_timeout_in_seconds": "idleDisconnectTimeoutInSeconds",
        "image_arn": "imageArn",
        "image_name": "imageName",
        "max_user_duration_in_seconds": "maxUserDurationInSeconds",
        "stream_view": "streamView",
        "tags": "tags",
        "tags_all": "tagsAll",
        "vpc_config": "vpcConfig",
    },
)
class AppstreamFleetConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[typing.Union[jsii.Number, cdktf.IResolvable]] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        compute_capacity: AppstreamFleetComputeCapacity,
        instance_type: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        display_name: typing.Optional[builtins.str] = None,
        domain_join_info: typing.Optional["AppstreamFleetDomainJoinInfo"] = None,
        enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        fleet_type: typing.Optional[builtins.str] = None,
        iam_role_arn: typing.Optional[builtins.str] = None,
        idle_disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        image_arn: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        max_user_duration_in_seconds: typing.Optional[jsii.Number] = None,
        stream_view: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags_all: typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        vpc_config: typing.Optional["AppstreamFleetVpcConfig"] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param compute_capacity: compute_capacity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#compute_capacity AppstreamFleet#compute_capacity}
        :param instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#instance_type AppstreamFleet#instance_type}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#name AppstreamFleet#name}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#description AppstreamFleet#description}.
        :param disconnect_timeout_in_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#disconnect_timeout_in_seconds AppstreamFleet#disconnect_timeout_in_seconds}.
        :param display_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#display_name AppstreamFleet#display_name}.
        :param domain_join_info: domain_join_info block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#domain_join_info AppstreamFleet#domain_join_info}
        :param enable_default_internet_access: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#enable_default_internet_access AppstreamFleet#enable_default_internet_access}.
        :param fleet_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#fleet_type AppstreamFleet#fleet_type}.
        :param iam_role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#iam_role_arn AppstreamFleet#iam_role_arn}.
        :param idle_disconnect_timeout_in_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#idle_disconnect_timeout_in_seconds AppstreamFleet#idle_disconnect_timeout_in_seconds}.
        :param image_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#image_arn AppstreamFleet#image_arn}.
        :param image_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#image_name AppstreamFleet#image_name}.
        :param max_user_duration_in_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#max_user_duration_in_seconds AppstreamFleet#max_user_duration_in_seconds}.
        :param stream_view: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#stream_view AppstreamFleet#stream_view}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#tags AppstreamFleet#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#tags_all AppstreamFleet#tags_all}.
        :param vpc_config: vpc_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#vpc_config AppstreamFleet#vpc_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(compute_capacity, dict):
            compute_capacity = AppstreamFleetComputeCapacity(**compute_capacity)
        if isinstance(domain_join_info, dict):
            domain_join_info = AppstreamFleetDomainJoinInfo(**domain_join_info)
        if isinstance(vpc_config, dict):
            vpc_config = AppstreamFleetVpcConfig(**vpc_config)
        self._values: typing.Dict[str, typing.Any] = {
            "compute_capacity": compute_capacity,
            "instance_type": instance_type,
            "name": name,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if description is not None:
            self._values["description"] = description
        if disconnect_timeout_in_seconds is not None:
            self._values["disconnect_timeout_in_seconds"] = disconnect_timeout_in_seconds
        if display_name is not None:
            self._values["display_name"] = display_name
        if domain_join_info is not None:
            self._values["domain_join_info"] = domain_join_info
        if enable_default_internet_access is not None:
            self._values["enable_default_internet_access"] = enable_default_internet_access
        if fleet_type is not None:
            self._values["fleet_type"] = fleet_type
        if iam_role_arn is not None:
            self._values["iam_role_arn"] = iam_role_arn
        if idle_disconnect_timeout_in_seconds is not None:
            self._values["idle_disconnect_timeout_in_seconds"] = idle_disconnect_timeout_in_seconds
        if image_arn is not None:
            self._values["image_arn"] = image_arn
        if image_name is not None:
            self._values["image_name"] = image_name
        if max_user_duration_in_seconds is not None:
            self._values["max_user_duration_in_seconds"] = max_user_duration_in_seconds
        if stream_view is not None:
            self._values["stream_view"] = stream_view
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def count(self) -> typing.Optional[typing.Union[jsii.Number, cdktf.IResolvable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, cdktf.IResolvable]], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def compute_capacity(self) -> AppstreamFleetComputeCapacity:
        '''compute_capacity block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#compute_capacity AppstreamFleet#compute_capacity}
        '''
        result = self._values.get("compute_capacity")
        assert result is not None, "Required property 'compute_capacity' is missing"
        return typing.cast(AppstreamFleetComputeCapacity, result)

    @builtins.property
    def instance_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#instance_type AppstreamFleet#instance_type}.'''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#name AppstreamFleet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#description AppstreamFleet#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disconnect_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#disconnect_timeout_in_seconds AppstreamFleet#disconnect_timeout_in_seconds}.'''
        result = self._values.get("disconnect_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#display_name AppstreamFleet#display_name}.'''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_join_info(self) -> typing.Optional["AppstreamFleetDomainJoinInfo"]:
        '''domain_join_info block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#domain_join_info AppstreamFleet#domain_join_info}
        '''
        result = self._values.get("domain_join_info")
        return typing.cast(typing.Optional["AppstreamFleetDomainJoinInfo"], result)

    @builtins.property
    def enable_default_internet_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#enable_default_internet_access AppstreamFleet#enable_default_internet_access}.'''
        result = self._values.get("enable_default_internet_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def fleet_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#fleet_type AppstreamFleet#fleet_type}.'''
        result = self._values.get("fleet_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#iam_role_arn AppstreamFleet#iam_role_arn}.'''
        result = self._values.get("iam_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idle_disconnect_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#idle_disconnect_timeout_in_seconds AppstreamFleet#idle_disconnect_timeout_in_seconds}.'''
        result = self._values.get("idle_disconnect_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def image_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#image_arn AppstreamFleet#image_arn}.'''
        result = self._values.get("image_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#image_name AppstreamFleet#image_name}.'''
        result = self._values.get("image_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_user_duration_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#max_user_duration_in_seconds AppstreamFleet#max_user_duration_in_seconds}.'''
        result = self._values.get("max_user_duration_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def stream_view(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#stream_view AppstreamFleet#stream_view}.'''
        result = self._values.get("stream_view")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#tags AppstreamFleet#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def tags_all(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#tags_all AppstreamFleet#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def vpc_config(self) -> typing.Optional["AppstreamFleetVpcConfig"]:
        '''vpc_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#vpc_config AppstreamFleet#vpc_config}
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional["AppstreamFleetVpcConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppstreamFleetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.AppStream.AppstreamFleetDomainJoinInfo",
    jsii_struct_bases=[],
    name_mapping={
        "directory_name": "directoryName",
        "organizational_unit_distinguished_name": "organizationalUnitDistinguishedName",
    },
)
class AppstreamFleetDomainJoinInfo:
    def __init__(
        self,
        *,
        directory_name: typing.Optional[builtins.str] = None,
        organizational_unit_distinguished_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param directory_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#directory_name AppstreamFleet#directory_name}.
        :param organizational_unit_distinguished_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#organizational_unit_distinguished_name AppstreamFleet#organizational_unit_distinguished_name}.
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if directory_name is not None:
            self._values["directory_name"] = directory_name
        if organizational_unit_distinguished_name is not None:
            self._values["organizational_unit_distinguished_name"] = organizational_unit_distinguished_name

    @builtins.property
    def directory_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#directory_name AppstreamFleet#directory_name}.'''
        result = self._values.get("directory_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organizational_unit_distinguished_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#organizational_unit_distinguished_name AppstreamFleet#organizational_unit_distinguished_name}.'''
        result = self._values.get("organizational_unit_distinguished_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppstreamFleetDomainJoinInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppstreamFleetDomainJoinInfoOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.AppStream.AppstreamFleetDomainJoinInfoOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.ITerraformResource,
        terraform_attribute: builtins.str,
        is_single_item: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param is_single_item: True if this is a block, false if it's a list.
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, is_single_item])

    @jsii.member(jsii_name="resetDirectoryName")
    def reset_directory_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirectoryName", []))

    @jsii.member(jsii_name="resetOrganizationalUnitDistinguishedName")
    def reset_organizational_unit_distinguished_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganizationalUnitDistinguishedName", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="directoryNameInput")
    def directory_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directoryNameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationalUnitDistinguishedNameInput")
    def organizational_unit_distinguished_name_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationalUnitDistinguishedNameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="directoryName")
    def directory_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directoryName"))

    @directory_name.setter
    def directory_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "directoryName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationalUnitDistinguishedName")
    def organizational_unit_distinguished_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationalUnitDistinguishedName"))

    @organizational_unit_distinguished_name.setter
    def organizational_unit_distinguished_name(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "organizationalUnitDistinguishedName", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.AppStream.AppstreamFleetVpcConfig",
    jsii_struct_bases=[],
    name_mapping={"security_group_ids": "securityGroupIds", "subnet_ids": "subnetIds"},
)
class AppstreamFleetVpcConfig:
    def __init__(
        self,
        *,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param security_group_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#security_group_ids AppstreamFleet#security_group_ids}.
        :param subnet_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#subnet_ids AppstreamFleet#subnet_ids}.
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#security_group_ids AppstreamFleet#security_group_ids}.'''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_fleet.html#subnet_ids AppstreamFleet#subnet_ids}.'''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppstreamFleetVpcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppstreamFleetVpcConfigOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.AppStream.AppstreamFleetVpcConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.ITerraformResource,
        terraform_attribute: builtins.str,
        is_single_item: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param is_single_item: True if this is a block, false if it's a list.
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, is_single_item])

    @jsii.member(jsii_name="resetSecurityGroupIds")
    def reset_security_group_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroupIds", []))

    @jsii.member(jsii_name="resetSubnetIds")
    def reset_subnet_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetIds", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="subnetIdsInput")
    def subnet_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIdsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "securityGroupIds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "subnetIds", value)


class AppstreamImageBuilder(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.AppStream.AppstreamImageBuilder",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html aws_appstream_image_builder}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        instance_type: builtins.str,
        name: builtins.str,
        access_endpoint: typing.Optional[typing.Sequence["AppstreamImageBuilderAccessEndpoint"]] = None,
        appstream_agent_version: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        domain_join_info: typing.Optional["AppstreamImageBuilderDomainJoinInfo"] = None,
        enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        iam_role_arn: typing.Optional[builtins.str] = None,
        image_arn: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags_all: typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        vpc_config: typing.Optional["AppstreamImageBuilderVpcConfig"] = None,
        count: typing.Optional[typing.Union[jsii.Number, cdktf.IResolvable]] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html aws_appstream_image_builder} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#instance_type AppstreamImageBuilder#instance_type}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#name AppstreamImageBuilder#name}.
        :param access_endpoint: access_endpoint block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#access_endpoint AppstreamImageBuilder#access_endpoint}
        :param appstream_agent_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#appstream_agent_version AppstreamImageBuilder#appstream_agent_version}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#description AppstreamImageBuilder#description}.
        :param display_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#display_name AppstreamImageBuilder#display_name}.
        :param domain_join_info: domain_join_info block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#domain_join_info AppstreamImageBuilder#domain_join_info}
        :param enable_default_internet_access: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#enable_default_internet_access AppstreamImageBuilder#enable_default_internet_access}.
        :param iam_role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#iam_role_arn AppstreamImageBuilder#iam_role_arn}.
        :param image_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#image_arn AppstreamImageBuilder#image_arn}.
        :param image_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#image_name AppstreamImageBuilder#image_name}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#tags AppstreamImageBuilder#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#tags_all AppstreamImageBuilder#tags_all}.
        :param vpc_config: vpc_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#vpc_config AppstreamImageBuilder#vpc_config}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = AppstreamImageBuilderConfig(
            instance_type=instance_type,
            name=name,
            access_endpoint=access_endpoint,
            appstream_agent_version=appstream_agent_version,
            description=description,
            display_name=display_name,
            domain_join_info=domain_join_info,
            enable_default_internet_access=enable_default_internet_access,
            iam_role_arn=iam_role_arn,
            image_arn=image_arn,
            image_name=image_name,
            tags=tags,
            tags_all=tags_all,
            vpc_config=vpc_config,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="putDomainJoinInfo")
    def put_domain_join_info(
        self,
        *,
        directory_name: typing.Optional[builtins.str] = None,
        organizational_unit_distinguished_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param directory_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#directory_name AppstreamImageBuilder#directory_name}.
        :param organizational_unit_distinguished_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#organizational_unit_distinguished_name AppstreamImageBuilder#organizational_unit_distinguished_name}.
        '''
        value = AppstreamImageBuilderDomainJoinInfo(
            directory_name=directory_name,
            organizational_unit_distinguished_name=organizational_unit_distinguished_name,
        )

        return typing.cast(None, jsii.invoke(self, "putDomainJoinInfo", [value]))

    @jsii.member(jsii_name="putVpcConfig")
    def put_vpc_config(
        self,
        *,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param security_group_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#security_group_ids AppstreamImageBuilder#security_group_ids}.
        :param subnet_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#subnet_ids AppstreamImageBuilder#subnet_ids}.
        '''
        value = AppstreamImageBuilderVpcConfig(
            security_group_ids=security_group_ids, subnet_ids=subnet_ids
        )

        return typing.cast(None, jsii.invoke(self, "putVpcConfig", [value]))

    @jsii.member(jsii_name="resetAccessEndpoint")
    def reset_access_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessEndpoint", []))

    @jsii.member(jsii_name="resetAppstreamAgentVersion")
    def reset_appstream_agent_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppstreamAgentVersion", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetDomainJoinInfo")
    def reset_domain_join_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainJoinInfo", []))

    @jsii.member(jsii_name="resetEnableDefaultInternetAccess")
    def reset_enable_default_internet_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableDefaultInternetAccess", []))

    @jsii.member(jsii_name="resetIamRoleArn")
    def reset_iam_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIamRoleArn", []))

    @jsii.member(jsii_name="resetImageArn")
    def reset_image_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageArn", []))

    @jsii.member(jsii_name="resetImageName")
    def reset_image_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageName", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetVpcConfig")
    def reset_vpc_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcConfig", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="createdTime")
    def created_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdTime"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="domainJoinInfo")
    def domain_join_info(self) -> "AppstreamImageBuilderDomainJoinInfoOutputReference":
        return typing.cast("AppstreamImageBuilderDomainJoinInfoOutputReference", jsii.get(self, "domainJoinInfo"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(self) -> "AppstreamImageBuilderVpcConfigOutputReference":
        return typing.cast("AppstreamImageBuilderVpcConfigOutputReference", jsii.get(self, "vpcConfig"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accessEndpointInput")
    def access_endpoint_input(
        self,
    ) -> typing.Optional[typing.List["AppstreamImageBuilderAccessEndpoint"]]:
        return typing.cast(typing.Optional[typing.List["AppstreamImageBuilderAccessEndpoint"]], jsii.get(self, "accessEndpointInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="appstreamAgentVersionInput")
    def appstream_agent_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appstreamAgentVersionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="domainJoinInfoInput")
    def domain_join_info_input(
        self,
    ) -> typing.Optional["AppstreamImageBuilderDomainJoinInfo"]:
        return typing.cast(typing.Optional["AppstreamImageBuilderDomainJoinInfo"], jsii.get(self, "domainJoinInfoInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enableDefaultInternetAccessInput")
    def enable_default_internet_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "enableDefaultInternetAccessInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="iamRoleArnInput")
    def iam_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamRoleArnInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="imageArnInput")
    def image_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageArnInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="imageNameInput")
    def image_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageNameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "tagsAllInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tagsInput")
    def tags_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "tagsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpcConfigInput")
    def vpc_config_input(self) -> typing.Optional["AppstreamImageBuilderVpcConfig"]:
        return typing.cast(typing.Optional["AppstreamImageBuilderVpcConfig"], jsii.get(self, "vpcConfigInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        jsii.set(self, "instanceType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accessEndpoint")
    def access_endpoint(
        self,
    ) -> typing.Optional[typing.List["AppstreamImageBuilderAccessEndpoint"]]:
        return typing.cast(typing.Optional[typing.List["AppstreamImageBuilderAccessEndpoint"]], jsii.get(self, "accessEndpoint"))

    @access_endpoint.setter
    def access_endpoint(
        self,
        value: typing.Optional[typing.List["AppstreamImageBuilderAccessEndpoint"]],
    ) -> None:
        jsii.set(self, "accessEndpoint", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="appstreamAgentVersion")
    def appstream_agent_version(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appstreamAgentVersion"))

    @appstream_agent_version.setter
    def appstream_agent_version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "appstreamAgentVersion", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "displayName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enableDefaultInternetAccess")
    def enable_default_internet_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "enableDefaultInternetAccess"))

    @enable_default_internet_access.setter
    def enable_default_internet_access(
        self,
        value: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]],
    ) -> None:
        jsii.set(self, "enableDefaultInternetAccess", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="iamRoleArn")
    def iam_role_arn(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamRoleArn"))

    @iam_role_arn.setter
    def iam_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "iamRoleArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="imageArn")
    def image_arn(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageArn"))

    @image_arn.setter
    def image_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "imageArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "imageName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        jsii.set(self, "tags", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tagsAll")
    def tags_all(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        jsii.set(self, "tagsAll", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.AppStream.AppstreamImageBuilderAccessEndpoint",
    jsii_struct_bases=[],
    name_mapping={"endpoint_type": "endpointType", "vpce_id": "vpceId"},
)
class AppstreamImageBuilderAccessEndpoint:
    def __init__(
        self,
        *,
        endpoint_type: builtins.str,
        vpce_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param endpoint_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#endpoint_type AppstreamImageBuilder#endpoint_type}.
        :param vpce_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#vpce_id AppstreamImageBuilder#vpce_id}.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "endpoint_type": endpoint_type,
        }
        if vpce_id is not None:
            self._values["vpce_id"] = vpce_id

    @builtins.property
    def endpoint_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#endpoint_type AppstreamImageBuilder#endpoint_type}.'''
        result = self._values.get("endpoint_type")
        assert result is not None, "Required property 'endpoint_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpce_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#vpce_id AppstreamImageBuilder#vpce_id}.'''
        result = self._values.get("vpce_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppstreamImageBuilderAccessEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.AppStream.AppstreamImageBuilderConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "instance_type": "instanceType",
        "name": "name",
        "access_endpoint": "accessEndpoint",
        "appstream_agent_version": "appstreamAgentVersion",
        "description": "description",
        "display_name": "displayName",
        "domain_join_info": "domainJoinInfo",
        "enable_default_internet_access": "enableDefaultInternetAccess",
        "iam_role_arn": "iamRoleArn",
        "image_arn": "imageArn",
        "image_name": "imageName",
        "tags": "tags",
        "tags_all": "tagsAll",
        "vpc_config": "vpcConfig",
    },
)
class AppstreamImageBuilderConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[typing.Union[jsii.Number, cdktf.IResolvable]] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        instance_type: builtins.str,
        name: builtins.str,
        access_endpoint: typing.Optional[typing.Sequence[AppstreamImageBuilderAccessEndpoint]] = None,
        appstream_agent_version: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        domain_join_info: typing.Optional["AppstreamImageBuilderDomainJoinInfo"] = None,
        enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        iam_role_arn: typing.Optional[builtins.str] = None,
        image_arn: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags_all: typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        vpc_config: typing.Optional["AppstreamImageBuilderVpcConfig"] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#instance_type AppstreamImageBuilder#instance_type}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#name AppstreamImageBuilder#name}.
        :param access_endpoint: access_endpoint block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#access_endpoint AppstreamImageBuilder#access_endpoint}
        :param appstream_agent_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#appstream_agent_version AppstreamImageBuilder#appstream_agent_version}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#description AppstreamImageBuilder#description}.
        :param display_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#display_name AppstreamImageBuilder#display_name}.
        :param domain_join_info: domain_join_info block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#domain_join_info AppstreamImageBuilder#domain_join_info}
        :param enable_default_internet_access: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#enable_default_internet_access AppstreamImageBuilder#enable_default_internet_access}.
        :param iam_role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#iam_role_arn AppstreamImageBuilder#iam_role_arn}.
        :param image_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#image_arn AppstreamImageBuilder#image_arn}.
        :param image_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#image_name AppstreamImageBuilder#image_name}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#tags AppstreamImageBuilder#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#tags_all AppstreamImageBuilder#tags_all}.
        :param vpc_config: vpc_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#vpc_config AppstreamImageBuilder#vpc_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(domain_join_info, dict):
            domain_join_info = AppstreamImageBuilderDomainJoinInfo(**domain_join_info)
        if isinstance(vpc_config, dict):
            vpc_config = AppstreamImageBuilderVpcConfig(**vpc_config)
        self._values: typing.Dict[str, typing.Any] = {
            "instance_type": instance_type,
            "name": name,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if access_endpoint is not None:
            self._values["access_endpoint"] = access_endpoint
        if appstream_agent_version is not None:
            self._values["appstream_agent_version"] = appstream_agent_version
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if domain_join_info is not None:
            self._values["domain_join_info"] = domain_join_info
        if enable_default_internet_access is not None:
            self._values["enable_default_internet_access"] = enable_default_internet_access
        if iam_role_arn is not None:
            self._values["iam_role_arn"] = iam_role_arn
        if image_arn is not None:
            self._values["image_arn"] = image_arn
        if image_name is not None:
            self._values["image_name"] = image_name
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def count(self) -> typing.Optional[typing.Union[jsii.Number, cdktf.IResolvable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, cdktf.IResolvable]], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def instance_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#instance_type AppstreamImageBuilder#instance_type}.'''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#name AppstreamImageBuilder#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_endpoint(
        self,
    ) -> typing.Optional[typing.List[AppstreamImageBuilderAccessEndpoint]]:
        '''access_endpoint block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#access_endpoint AppstreamImageBuilder#access_endpoint}
        '''
        result = self._values.get("access_endpoint")
        return typing.cast(typing.Optional[typing.List[AppstreamImageBuilderAccessEndpoint]], result)

    @builtins.property
    def appstream_agent_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#appstream_agent_version AppstreamImageBuilder#appstream_agent_version}.'''
        result = self._values.get("appstream_agent_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#description AppstreamImageBuilder#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#display_name AppstreamImageBuilder#display_name}.'''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_join_info(
        self,
    ) -> typing.Optional["AppstreamImageBuilderDomainJoinInfo"]:
        '''domain_join_info block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#domain_join_info AppstreamImageBuilder#domain_join_info}
        '''
        result = self._values.get("domain_join_info")
        return typing.cast(typing.Optional["AppstreamImageBuilderDomainJoinInfo"], result)

    @builtins.property
    def enable_default_internet_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#enable_default_internet_access AppstreamImageBuilder#enable_default_internet_access}.'''
        result = self._values.get("enable_default_internet_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def iam_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#iam_role_arn AppstreamImageBuilder#iam_role_arn}.'''
        result = self._values.get("iam_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#image_arn AppstreamImageBuilder#image_arn}.'''
        result = self._values.get("image_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#image_name AppstreamImageBuilder#image_name}.'''
        result = self._values.get("image_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#tags AppstreamImageBuilder#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def tags_all(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#tags_all AppstreamImageBuilder#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def vpc_config(self) -> typing.Optional["AppstreamImageBuilderVpcConfig"]:
        '''vpc_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#vpc_config AppstreamImageBuilder#vpc_config}
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional["AppstreamImageBuilderVpcConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppstreamImageBuilderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.AppStream.AppstreamImageBuilderDomainJoinInfo",
    jsii_struct_bases=[],
    name_mapping={
        "directory_name": "directoryName",
        "organizational_unit_distinguished_name": "organizationalUnitDistinguishedName",
    },
)
class AppstreamImageBuilderDomainJoinInfo:
    def __init__(
        self,
        *,
        directory_name: typing.Optional[builtins.str] = None,
        organizational_unit_distinguished_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param directory_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#directory_name AppstreamImageBuilder#directory_name}.
        :param organizational_unit_distinguished_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#organizational_unit_distinguished_name AppstreamImageBuilder#organizational_unit_distinguished_name}.
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if directory_name is not None:
            self._values["directory_name"] = directory_name
        if organizational_unit_distinguished_name is not None:
            self._values["organizational_unit_distinguished_name"] = organizational_unit_distinguished_name

    @builtins.property
    def directory_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#directory_name AppstreamImageBuilder#directory_name}.'''
        result = self._values.get("directory_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organizational_unit_distinguished_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#organizational_unit_distinguished_name AppstreamImageBuilder#organizational_unit_distinguished_name}.'''
        result = self._values.get("organizational_unit_distinguished_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppstreamImageBuilderDomainJoinInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppstreamImageBuilderDomainJoinInfoOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.AppStream.AppstreamImageBuilderDomainJoinInfoOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.ITerraformResource,
        terraform_attribute: builtins.str,
        is_single_item: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param is_single_item: True if this is a block, false if it's a list.
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, is_single_item])

    @jsii.member(jsii_name="resetDirectoryName")
    def reset_directory_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirectoryName", []))

    @jsii.member(jsii_name="resetOrganizationalUnitDistinguishedName")
    def reset_organizational_unit_distinguished_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganizationalUnitDistinguishedName", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="directoryNameInput")
    def directory_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directoryNameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationalUnitDistinguishedNameInput")
    def organizational_unit_distinguished_name_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationalUnitDistinguishedNameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="directoryName")
    def directory_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directoryName"))

    @directory_name.setter
    def directory_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "directoryName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationalUnitDistinguishedName")
    def organizational_unit_distinguished_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationalUnitDistinguishedName"))

    @organizational_unit_distinguished_name.setter
    def organizational_unit_distinguished_name(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "organizationalUnitDistinguishedName", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.AppStream.AppstreamImageBuilderVpcConfig",
    jsii_struct_bases=[],
    name_mapping={"security_group_ids": "securityGroupIds", "subnet_ids": "subnetIds"},
)
class AppstreamImageBuilderVpcConfig:
    def __init__(
        self,
        *,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param security_group_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#security_group_ids AppstreamImageBuilder#security_group_ids}.
        :param subnet_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#subnet_ids AppstreamImageBuilder#subnet_ids}.
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#security_group_ids AppstreamImageBuilder#security_group_ids}.'''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_image_builder.html#subnet_ids AppstreamImageBuilder#subnet_ids}.'''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppstreamImageBuilderVpcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppstreamImageBuilderVpcConfigOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.AppStream.AppstreamImageBuilderVpcConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.ITerraformResource,
        terraform_attribute: builtins.str,
        is_single_item: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param is_single_item: True if this is a block, false if it's a list.
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, is_single_item])

    @jsii.member(jsii_name="resetSecurityGroupIds")
    def reset_security_group_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroupIds", []))

    @jsii.member(jsii_name="resetSubnetIds")
    def reset_subnet_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetIds", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="subnetIdsInput")
    def subnet_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIdsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "securityGroupIds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "subnetIds", value)


class AppstreamStack(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.AppStream.AppstreamStack",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html aws_appstream_stack}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        access_endpoints: typing.Optional[typing.Sequence["AppstreamStackAccessEndpoints"]] = None,
        application_settings: typing.Optional["AppstreamStackApplicationSettings"] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        embed_host_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        feedback_url: typing.Optional[builtins.str] = None,
        redirect_url: typing.Optional[builtins.str] = None,
        storage_connectors: typing.Optional[typing.Sequence["AppstreamStackStorageConnectors"]] = None,
        tags: typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags_all: typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        user_settings: typing.Optional[typing.Sequence["AppstreamStackUserSettings"]] = None,
        count: typing.Optional[typing.Union[jsii.Number, cdktf.IResolvable]] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html aws_appstream_stack} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#name AppstreamStack#name}.
        :param access_endpoints: access_endpoints block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#access_endpoints AppstreamStack#access_endpoints}
        :param application_settings: application_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#application_settings AppstreamStack#application_settings}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#description AppstreamStack#description}.
        :param display_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#display_name AppstreamStack#display_name}.
        :param embed_host_domains: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#embed_host_domains AppstreamStack#embed_host_domains}.
        :param feedback_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#feedback_url AppstreamStack#feedback_url}.
        :param redirect_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#redirect_url AppstreamStack#redirect_url}.
        :param storage_connectors: storage_connectors block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#storage_connectors AppstreamStack#storage_connectors}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#tags AppstreamStack#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#tags_all AppstreamStack#tags_all}.
        :param user_settings: user_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#user_settings AppstreamStack#user_settings}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = AppstreamStackConfig(
            name=name,
            access_endpoints=access_endpoints,
            application_settings=application_settings,
            description=description,
            display_name=display_name,
            embed_host_domains=embed_host_domains,
            feedback_url=feedback_url,
            redirect_url=redirect_url,
            storage_connectors=storage_connectors,
            tags=tags,
            tags_all=tags_all,
            user_settings=user_settings,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="putApplicationSettings")
    def put_application_settings(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        settings_group: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#enabled AppstreamStack#enabled}.
        :param settings_group: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#settings_group AppstreamStack#settings_group}.
        '''
        value = AppstreamStackApplicationSettings(
            enabled=enabled, settings_group=settings_group
        )

        return typing.cast(None, jsii.invoke(self, "putApplicationSettings", [value]))

    @jsii.member(jsii_name="resetAccessEndpoints")
    def reset_access_endpoints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessEndpoints", []))

    @jsii.member(jsii_name="resetApplicationSettings")
    def reset_application_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationSettings", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetEmbedHostDomains")
    def reset_embed_host_domains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmbedHostDomains", []))

    @jsii.member(jsii_name="resetFeedbackUrl")
    def reset_feedback_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFeedbackUrl", []))

    @jsii.member(jsii_name="resetRedirectUrl")
    def reset_redirect_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUrl", []))

    @jsii.member(jsii_name="resetStorageConnectors")
    def reset_storage_connectors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageConnectors", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetUserSettings")
    def reset_user_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserSettings", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationSettings")
    def application_settings(
        self,
    ) -> "AppstreamStackApplicationSettingsOutputReference":
        return typing.cast("AppstreamStackApplicationSettingsOutputReference", jsii.get(self, "applicationSettings"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="createdTime")
    def created_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdTime"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accessEndpointsInput")
    def access_endpoints_input(
        self,
    ) -> typing.Optional[typing.List["AppstreamStackAccessEndpoints"]]:
        return typing.cast(typing.Optional[typing.List["AppstreamStackAccessEndpoints"]], jsii.get(self, "accessEndpointsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationSettingsInput")
    def application_settings_input(
        self,
    ) -> typing.Optional["AppstreamStackApplicationSettings"]:
        return typing.cast(typing.Optional["AppstreamStackApplicationSettings"], jsii.get(self, "applicationSettingsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="embedHostDomainsInput")
    def embed_host_domains_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "embedHostDomainsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="feedbackUrlInput")
    def feedback_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "feedbackUrlInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="redirectUrlInput")
    def redirect_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectUrlInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="storageConnectorsInput")
    def storage_connectors_input(
        self,
    ) -> typing.Optional[typing.List["AppstreamStackStorageConnectors"]]:
        return typing.cast(typing.Optional[typing.List["AppstreamStackStorageConnectors"]], jsii.get(self, "storageConnectorsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "tagsAllInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tagsInput")
    def tags_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "tagsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="userSettingsInput")
    def user_settings_input(
        self,
    ) -> typing.Optional[typing.List["AppstreamStackUserSettings"]]:
        return typing.cast(typing.Optional[typing.List["AppstreamStackUserSettings"]], jsii.get(self, "userSettingsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accessEndpoints")
    def access_endpoints(
        self,
    ) -> typing.Optional[typing.List["AppstreamStackAccessEndpoints"]]:
        return typing.cast(typing.Optional[typing.List["AppstreamStackAccessEndpoints"]], jsii.get(self, "accessEndpoints"))

    @access_endpoints.setter
    def access_endpoints(
        self,
        value: typing.Optional[typing.List["AppstreamStackAccessEndpoints"]],
    ) -> None:
        jsii.set(self, "accessEndpoints", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "displayName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="embedHostDomains")
    def embed_host_domains(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "embedHostDomains"))

    @embed_host_domains.setter
    def embed_host_domains(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "embedHostDomains", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="feedbackUrl")
    def feedback_url(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "feedbackUrl"))

    @feedback_url.setter
    def feedback_url(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "feedbackUrl", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="redirectUrl")
    def redirect_url(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectUrl"))

    @redirect_url.setter
    def redirect_url(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "redirectUrl", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="storageConnectors")
    def storage_connectors(
        self,
    ) -> typing.Optional[typing.List["AppstreamStackStorageConnectors"]]:
        return typing.cast(typing.Optional[typing.List["AppstreamStackStorageConnectors"]], jsii.get(self, "storageConnectors"))

    @storage_connectors.setter
    def storage_connectors(
        self,
        value: typing.Optional[typing.List["AppstreamStackStorageConnectors"]],
    ) -> None:
        jsii.set(self, "storageConnectors", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        jsii.set(self, "tags", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tagsAll")
    def tags_all(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        jsii.set(self, "tagsAll", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="userSettings")
    def user_settings(
        self,
    ) -> typing.Optional[typing.List["AppstreamStackUserSettings"]]:
        return typing.cast(typing.Optional[typing.List["AppstreamStackUserSettings"]], jsii.get(self, "userSettings"))

    @user_settings.setter
    def user_settings(
        self,
        value: typing.Optional[typing.List["AppstreamStackUserSettings"]],
    ) -> None:
        jsii.set(self, "userSettings", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.AppStream.AppstreamStackAccessEndpoints",
    jsii_struct_bases=[],
    name_mapping={"endpoint_type": "endpointType", "vpce_id": "vpceId"},
)
class AppstreamStackAccessEndpoints:
    def __init__(
        self,
        *,
        endpoint_type: builtins.str,
        vpce_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param endpoint_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#endpoint_type AppstreamStack#endpoint_type}.
        :param vpce_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#vpce_id AppstreamStack#vpce_id}.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "endpoint_type": endpoint_type,
        }
        if vpce_id is not None:
            self._values["vpce_id"] = vpce_id

    @builtins.property
    def endpoint_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#endpoint_type AppstreamStack#endpoint_type}.'''
        result = self._values.get("endpoint_type")
        assert result is not None, "Required property 'endpoint_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpce_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#vpce_id AppstreamStack#vpce_id}.'''
        result = self._values.get("vpce_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppstreamStackAccessEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.AppStream.AppstreamStackApplicationSettings",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "settings_group": "settingsGroup"},
)
class AppstreamStackApplicationSettings:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        settings_group: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#enabled AppstreamStack#enabled}.
        :param settings_group: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#settings_group AppstreamStack#settings_group}.
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if settings_group is not None:
            self._values["settings_group"] = settings_group

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#enabled AppstreamStack#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def settings_group(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#settings_group AppstreamStack#settings_group}.'''
        result = self._values.get("settings_group")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppstreamStackApplicationSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppstreamStackApplicationSettingsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.AppStream.AppstreamStackApplicationSettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.ITerraformResource,
        terraform_attribute: builtins.str,
        is_single_item: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param is_single_item: True if this is a block, false if it's a list.
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, is_single_item])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetSettingsGroup")
    def reset_settings_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSettingsGroup", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="settingsGroupInput")
    def settings_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "settingsGroupInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]],
    ) -> None:
        jsii.set(self, "enabled", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="settingsGroup")
    def settings_group(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "settingsGroup"))

    @settings_group.setter
    def settings_group(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "settingsGroup", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.AppStream.AppstreamStackConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
        "access_endpoints": "accessEndpoints",
        "application_settings": "applicationSettings",
        "description": "description",
        "display_name": "displayName",
        "embed_host_domains": "embedHostDomains",
        "feedback_url": "feedbackUrl",
        "redirect_url": "redirectUrl",
        "storage_connectors": "storageConnectors",
        "tags": "tags",
        "tags_all": "tagsAll",
        "user_settings": "userSettings",
    },
)
class AppstreamStackConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[typing.Union[jsii.Number, cdktf.IResolvable]] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: builtins.str,
        access_endpoints: typing.Optional[typing.Sequence[AppstreamStackAccessEndpoints]] = None,
        application_settings: typing.Optional[AppstreamStackApplicationSettings] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        embed_host_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        feedback_url: typing.Optional[builtins.str] = None,
        redirect_url: typing.Optional[builtins.str] = None,
        storage_connectors: typing.Optional[typing.Sequence["AppstreamStackStorageConnectors"]] = None,
        tags: typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags_all: typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        user_settings: typing.Optional[typing.Sequence["AppstreamStackUserSettings"]] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#name AppstreamStack#name}.
        :param access_endpoints: access_endpoints block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#access_endpoints AppstreamStack#access_endpoints}
        :param application_settings: application_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#application_settings AppstreamStack#application_settings}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#description AppstreamStack#description}.
        :param display_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#display_name AppstreamStack#display_name}.
        :param embed_host_domains: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#embed_host_domains AppstreamStack#embed_host_domains}.
        :param feedback_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#feedback_url AppstreamStack#feedback_url}.
        :param redirect_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#redirect_url AppstreamStack#redirect_url}.
        :param storage_connectors: storage_connectors block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#storage_connectors AppstreamStack#storage_connectors}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#tags AppstreamStack#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#tags_all AppstreamStack#tags_all}.
        :param user_settings: user_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#user_settings AppstreamStack#user_settings}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(application_settings, dict):
            application_settings = AppstreamStackApplicationSettings(**application_settings)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if access_endpoints is not None:
            self._values["access_endpoints"] = access_endpoints
        if application_settings is not None:
            self._values["application_settings"] = application_settings
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if embed_host_domains is not None:
            self._values["embed_host_domains"] = embed_host_domains
        if feedback_url is not None:
            self._values["feedback_url"] = feedback_url
        if redirect_url is not None:
            self._values["redirect_url"] = redirect_url
        if storage_connectors is not None:
            self._values["storage_connectors"] = storage_connectors
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if user_settings is not None:
            self._values["user_settings"] = user_settings

    @builtins.property
    def count(self) -> typing.Optional[typing.Union[jsii.Number, cdktf.IResolvable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, cdktf.IResolvable]], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#name AppstreamStack#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_endpoints(
        self,
    ) -> typing.Optional[typing.List[AppstreamStackAccessEndpoints]]:
        '''access_endpoints block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#access_endpoints AppstreamStack#access_endpoints}
        '''
        result = self._values.get("access_endpoints")
        return typing.cast(typing.Optional[typing.List[AppstreamStackAccessEndpoints]], result)

    @builtins.property
    def application_settings(
        self,
    ) -> typing.Optional[AppstreamStackApplicationSettings]:
        '''application_settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#application_settings AppstreamStack#application_settings}
        '''
        result = self._values.get("application_settings")
        return typing.cast(typing.Optional[AppstreamStackApplicationSettings], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#description AppstreamStack#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#display_name AppstreamStack#display_name}.'''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def embed_host_domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#embed_host_domains AppstreamStack#embed_host_domains}.'''
        result = self._values.get("embed_host_domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def feedback_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#feedback_url AppstreamStack#feedback_url}.'''
        result = self._values.get("feedback_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#redirect_url AppstreamStack#redirect_url}.'''
        result = self._values.get("redirect_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_connectors(
        self,
    ) -> typing.Optional[typing.List["AppstreamStackStorageConnectors"]]:
        '''storage_connectors block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#storage_connectors AppstreamStack#storage_connectors}
        '''
        result = self._values.get("storage_connectors")
        return typing.cast(typing.Optional[typing.List["AppstreamStackStorageConnectors"]], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#tags AppstreamStack#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def tags_all(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#tags_all AppstreamStack#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def user_settings(
        self,
    ) -> typing.Optional[typing.List["AppstreamStackUserSettings"]]:
        '''user_settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#user_settings AppstreamStack#user_settings}
        '''
        result = self._values.get("user_settings")
        return typing.cast(typing.Optional[typing.List["AppstreamStackUserSettings"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppstreamStackConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.AppStream.AppstreamStackStorageConnectors",
    jsii_struct_bases=[],
    name_mapping={
        "connector_type": "connectorType",
        "domains": "domains",
        "resource_identifier": "resourceIdentifier",
    },
)
class AppstreamStackStorageConnectors:
    def __init__(
        self,
        *,
        connector_type: builtins.str,
        domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connector_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#connector_type AppstreamStack#connector_type}.
        :param domains: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#domains AppstreamStack#domains}.
        :param resource_identifier: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#resource_identifier AppstreamStack#resource_identifier}.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "connector_type": connector_type,
        }
        if domains is not None:
            self._values["domains"] = domains
        if resource_identifier is not None:
            self._values["resource_identifier"] = resource_identifier

    @builtins.property
    def connector_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#connector_type AppstreamStack#connector_type}.'''
        result = self._values.get("connector_type")
        assert result is not None, "Required property 'connector_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#domains AppstreamStack#domains}.'''
        result = self._values.get("domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource_identifier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#resource_identifier AppstreamStack#resource_identifier}.'''
        result = self._values.get("resource_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppstreamStackStorageConnectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.AppStream.AppstreamStackUserSettings",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "permission": "permission"},
)
class AppstreamStackUserSettings:
    def __init__(self, *, action: builtins.str, permission: builtins.str) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#action AppstreamStack#action}.
        :param permission: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#permission AppstreamStack#permission}.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action": action,
            "permission": permission,
        }

    @builtins.property
    def action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#action AppstreamStack#action}.'''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def permission(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appstream_stack.html#permission AppstreamStack#permission}.'''
        result = self._values.get("permission")
        assert result is not None, "Required property 'permission' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppstreamStackUserSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AppstreamFleet",
    "AppstreamFleetComputeCapacity",
    "AppstreamFleetComputeCapacityOutputReference",
    "AppstreamFleetConfig",
    "AppstreamFleetDomainJoinInfo",
    "AppstreamFleetDomainJoinInfoOutputReference",
    "AppstreamFleetVpcConfig",
    "AppstreamFleetVpcConfigOutputReference",
    "AppstreamImageBuilder",
    "AppstreamImageBuilderAccessEndpoint",
    "AppstreamImageBuilderConfig",
    "AppstreamImageBuilderDomainJoinInfo",
    "AppstreamImageBuilderDomainJoinInfoOutputReference",
    "AppstreamImageBuilderVpcConfig",
    "AppstreamImageBuilderVpcConfigOutputReference",
    "AppstreamStack",
    "AppstreamStackAccessEndpoints",
    "AppstreamStackApplicationSettings",
    "AppstreamStackApplicationSettingsOutputReference",
    "AppstreamStackConfig",
    "AppstreamStackStorageConnectors",
    "AppstreamStackUserSettings",
]

publication.publish()
