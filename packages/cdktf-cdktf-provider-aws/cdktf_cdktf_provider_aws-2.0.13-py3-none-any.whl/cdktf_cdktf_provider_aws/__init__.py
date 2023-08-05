'''
# Terraform CDK aws Provider ~> 3.0

This repo builds and publishes the Terraform aws Provider bindings for [cdktf](https://cdk.tf).

Current build targets are:

* npm
* Pypi
* Nuget
* Maven

## Docs

Find auto-generated docs for this provider here: [./API.md](./API.md)

## Versioning

This project is explicitly not tracking the Terraform aws Provider version 1:1. In fact, it always tracks `latest` of `~> 3.0` with every release. If there scenarios where you explicitly have to pin your provider version, you can do so by generating the [provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [Terraform CDK](https://cdk.tf)
* [Terraform aws Provider](https://github.com/terraform-providers/terraform-provider-aws)
* [Terraform Engine](https://terraform.io)

If there are breaking changes (backward incompatible) in any of the above, the major version of this project will be bumped. While the Terraform Engine and the Terraform aws Provider are relatively stable, the Terraform CDK is in an early stage. Therefore, it's likely that there will be breaking changes.

## Features / Issues / Bugs

Please report bugs and issues to the [terraform cdk](https://cdk.tf) project:

* [Create bug report](https://cdk.tf/bug)
* [Create feature request](https://cdk.tf/feature)

## Contributing

## projen

This is mostly based on [projen](https://github.com/eladb/projen), which takes care of generating the entire repository.

## cdktf-provider-project based on projen

There's a custom [project builder](https://github.com/terraform-cdk-providers/cdktf-provider-project) which encapsulate the common settings for all `cdktf` providers.

## provider version

The provider version can be adjusted in [./.projenrc.js](./.projenrc.js).
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

import cdktf
import constructs


class AwsProvider(
    cdktf.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.AwsProvider",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws aws}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        region: builtins.str,
        access_key: typing.Optional[builtins.str] = None,
        alias: typing.Optional[builtins.str] = None,
        allowed_account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        assume_role: typing.Optional["AwsProviderAssumeRole"] = None,
        default_tags: typing.Optional["AwsProviderDefaultTags"] = None,
        endpoints: typing.Optional[typing.Sequence["AwsProviderEndpoints"]] = None,
        forbidden_account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        http_proxy: typing.Optional[builtins.str] = None,
        ignore_tags: typing.Optional["AwsProviderIgnoreTags"] = None,
        insecure: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        profile: typing.Optional[builtins.str] = None,
        s3_force_path_style: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        secret_key: typing.Optional[builtins.str] = None,
        shared_credentials_file: typing.Optional[builtins.str] = None,
        skip_credentials_validation: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        skip_get_ec2_platforms: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        skip_metadata_api_check: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        skip_region_validation: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        skip_requesting_account_id: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws aws} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param region: The region where AWS operations will take place. Examples are us-east-1, us-west-2, etc. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#region AwsProvider#region}
        :param access_key: The access key for API operations. You can retrieve this from the 'Security & Credentials' section of the AWS console. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#access_key AwsProvider#access_key}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#alias AwsProvider#alias}
        :param allowed_account_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#allowed_account_ids AwsProvider#allowed_account_ids}.
        :param assume_role: assume_role block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#assume_role AwsProvider#assume_role}
        :param default_tags: default_tags block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#default_tags AwsProvider#default_tags}
        :param endpoints: endpoints block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#endpoints AwsProvider#endpoints}
        :param forbidden_account_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#forbidden_account_ids AwsProvider#forbidden_account_ids}.
        :param http_proxy: The address of an HTTP proxy to use when accessing the AWS API. Can also be configured using the ``HTTP_PROXY`` or ``HTTPS_PROXY`` environment variables. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#http_proxy AwsProvider#http_proxy}
        :param ignore_tags: ignore_tags block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#ignore_tags AwsProvider#ignore_tags}
        :param insecure: Explicitly allow the provider to perform "insecure" SSL requests. If omitted, default value is ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#insecure AwsProvider#insecure}
        :param max_retries: The maximum number of times an AWS API request is being executed. If the API request still fails, an error is thrown. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#max_retries AwsProvider#max_retries}
        :param profile: The profile for API operations. If not set, the default profile created with ``aws configure`` will be used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#profile AwsProvider#profile}
        :param s3_force_path_style: Set this to true to force the request to use path-style addressing, i.e., http://s3.amazonaws.com/BUCKET/KEY. By default, the S3 client will use virtual hosted bucket addressing when possible (http://BUCKET.s3.amazonaws.com/KEY). Specific to the Amazon S3 service. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#s3_force_path_style AwsProvider#s3_force_path_style}
        :param secret_key: The secret key for API operations. You can retrieve this from the 'Security & Credentials' section of the AWS console. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#secret_key AwsProvider#secret_key}
        :param shared_credentials_file: The path to the shared credentials file. If not set this defaults to ~/.aws/credentials. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#shared_credentials_file AwsProvider#shared_credentials_file}
        :param skip_credentials_validation: Skip the credentials validation via STS API. Used for AWS API implementations that do not have STS available/implemented. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#skip_credentials_validation AwsProvider#skip_credentials_validation}
        :param skip_get_ec2_platforms: Skip getting the supported EC2 platforms. Used by users that don't have ec2:DescribeAccountAttributes permissions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#skip_get_ec2_platforms AwsProvider#skip_get_ec2_platforms}
        :param skip_metadata_api_check: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#skip_metadata_api_check AwsProvider#skip_metadata_api_check}.
        :param skip_region_validation: Skip static validation of region name. Used by users of alternative AWS-like APIs or users w/ access to regions that are not public (yet). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#skip_region_validation AwsProvider#skip_region_validation}
        :param skip_requesting_account_id: Skip requesting the account ID. Used for AWS API implementations that do not have IAM/STS API and/or metadata API. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#skip_requesting_account_id AwsProvider#skip_requesting_account_id}
        :param token: session token. A session token is only required if you are using temporary security credentials. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#token AwsProvider#token}
        '''
        config = AwsProviderConfig(
            region=region,
            access_key=access_key,
            alias=alias,
            allowed_account_ids=allowed_account_ids,
            assume_role=assume_role,
            default_tags=default_tags,
            endpoints=endpoints,
            forbidden_account_ids=forbidden_account_ids,
            http_proxy=http_proxy,
            ignore_tags=ignore_tags,
            insecure=insecure,
            max_retries=max_retries,
            profile=profile,
            s3_force_path_style=s3_force_path_style,
            secret_key=secret_key,
            shared_credentials_file=shared_credentials_file,
            skip_credentials_validation=skip_credentials_validation,
            skip_get_ec2_platforms=skip_get_ec2_platforms,
            skip_metadata_api_check=skip_metadata_api_check,
            skip_region_validation=skip_region_validation,
            skip_requesting_account_id=skip_requesting_account_id,
            token=token,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetAccessKey")
    def reset_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessKey", []))

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetAllowedAccountIds")
    def reset_allowed_account_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedAccountIds", []))

    @jsii.member(jsii_name="resetAssumeRole")
    def reset_assume_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssumeRole", []))

    @jsii.member(jsii_name="resetDefaultTags")
    def reset_default_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTags", []))

    @jsii.member(jsii_name="resetEndpoints")
    def reset_endpoints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpoints", []))

    @jsii.member(jsii_name="resetForbiddenAccountIds")
    def reset_forbidden_account_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForbiddenAccountIds", []))

    @jsii.member(jsii_name="resetHttpProxy")
    def reset_http_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpProxy", []))

    @jsii.member(jsii_name="resetIgnoreTags")
    def reset_ignore_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreTags", []))

    @jsii.member(jsii_name="resetInsecure")
    def reset_insecure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsecure", []))

    @jsii.member(jsii_name="resetMaxRetries")
    def reset_max_retries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRetries", []))

    @jsii.member(jsii_name="resetProfile")
    def reset_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProfile", []))

    @jsii.member(jsii_name="resetS3ForcePathStyle")
    def reset_s3_force_path_style(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3ForcePathStyle", []))

    @jsii.member(jsii_name="resetSecretKey")
    def reset_secret_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretKey", []))

    @jsii.member(jsii_name="resetSharedCredentialsFile")
    def reset_shared_credentials_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedCredentialsFile", []))

    @jsii.member(jsii_name="resetSkipCredentialsValidation")
    def reset_skip_credentials_validation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipCredentialsValidation", []))

    @jsii.member(jsii_name="resetSkipGetEc2Platforms")
    def reset_skip_get_ec2_platforms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipGetEc2Platforms", []))

    @jsii.member(jsii_name="resetSkipMetadataApiCheck")
    def reset_skip_metadata_api_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipMetadataApiCheck", []))

    @jsii.member(jsii_name="resetSkipRegionValidation")
    def reset_skip_region_validation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipRegionValidation", []))

    @jsii.member(jsii_name="resetSkipRequestingAccountId")
    def reset_skip_requesting_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipRequestingAccountId", []))

    @jsii.member(jsii_name="resetToken")
    def reset_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetToken", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accessKeyInput")
    def access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKeyInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="allowedAccountIdsInput")
    def allowed_account_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedAccountIdsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="assumeRoleInput")
    def assume_role_input(self) -> typing.Optional["AwsProviderAssumeRole"]:
        return typing.cast(typing.Optional["AwsProviderAssumeRole"], jsii.get(self, "assumeRoleInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultTagsInput")
    def default_tags_input(self) -> typing.Optional["AwsProviderDefaultTags"]:
        return typing.cast(typing.Optional["AwsProviderDefaultTags"], jsii.get(self, "defaultTagsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endpointsInput")
    def endpoints_input(self) -> typing.Optional[typing.List["AwsProviderEndpoints"]]:
        return typing.cast(typing.Optional[typing.List["AwsProviderEndpoints"]], jsii.get(self, "endpointsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="forbiddenAccountIdsInput")
    def forbidden_account_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "forbiddenAccountIdsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="httpProxyInput")
    def http_proxy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpProxyInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ignoreTagsInput")
    def ignore_tags_input(self) -> typing.Optional["AwsProviderIgnoreTags"]:
        return typing.cast(typing.Optional["AwsProviderIgnoreTags"], jsii.get(self, "ignoreTagsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="insecureInput")
    def insecure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "insecureInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="maxRetriesInput")
    def max_retries_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetriesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="profileInput")
    def profile_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "profileInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="s3ForcePathStyleInput")
    def s3_force_path_style_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "s3ForcePathStyleInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="secretKeyInput")
    def secret_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretKeyInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sharedCredentialsFileInput")
    def shared_credentials_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sharedCredentialsFileInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="skipCredentialsValidationInput")
    def skip_credentials_validation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "skipCredentialsValidationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="skipGetEc2PlatformsInput")
    def skip_get_ec2_platforms_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "skipGetEc2PlatformsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="skipMetadataApiCheckInput")
    def skip_metadata_api_check_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "skipMetadataApiCheckInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="skipRegionValidationInput")
    def skip_region_validation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "skipRegionValidationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="skipRequestingAccountIdInput")
    def skip_requesting_account_id_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "skipRequestingAccountIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tokenInput")
    def token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accessKey")
    def access_key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKey"))

    @access_key.setter
    def access_key(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "accessKey", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "alias", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="allowedAccountIds")
    def allowed_account_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedAccountIds"))

    @allowed_account_ids.setter
    def allowed_account_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "allowedAccountIds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="assumeRole")
    def assume_role(self) -> typing.Optional["AwsProviderAssumeRole"]:
        return typing.cast(typing.Optional["AwsProviderAssumeRole"], jsii.get(self, "assumeRole"))

    @assume_role.setter
    def assume_role(self, value: typing.Optional["AwsProviderAssumeRole"]) -> None:
        jsii.set(self, "assumeRole", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultTags")
    def default_tags(self) -> typing.Optional["AwsProviderDefaultTags"]:
        return typing.cast(typing.Optional["AwsProviderDefaultTags"], jsii.get(self, "defaultTags"))

    @default_tags.setter
    def default_tags(self, value: typing.Optional["AwsProviderDefaultTags"]) -> None:
        jsii.set(self, "defaultTags", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endpoints")
    def endpoints(self) -> typing.Optional[typing.List["AwsProviderEndpoints"]]:
        return typing.cast(typing.Optional[typing.List["AwsProviderEndpoints"]], jsii.get(self, "endpoints"))

    @endpoints.setter
    def endpoints(
        self,
        value: typing.Optional[typing.List["AwsProviderEndpoints"]],
    ) -> None:
        jsii.set(self, "endpoints", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="forbiddenAccountIds")
    def forbidden_account_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "forbiddenAccountIds"))

    @forbidden_account_ids.setter
    def forbidden_account_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "forbiddenAccountIds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="httpProxy")
    def http_proxy(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpProxy"))

    @http_proxy.setter
    def http_proxy(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "httpProxy", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ignoreTags")
    def ignore_tags(self) -> typing.Optional["AwsProviderIgnoreTags"]:
        return typing.cast(typing.Optional["AwsProviderIgnoreTags"], jsii.get(self, "ignoreTags"))

    @ignore_tags.setter
    def ignore_tags(self, value: typing.Optional["AwsProviderIgnoreTags"]) -> None:
        jsii.set(self, "ignoreTags", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="insecure")
    def insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "insecure"))

    @insecure.setter
    def insecure(
        self,
        value: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]],
    ) -> None:
        jsii.set(self, "insecure", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="maxRetries")
    def max_retries(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetries"))

    @max_retries.setter
    def max_retries(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "maxRetries", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="profile")
    def profile(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "profile"))

    @profile.setter
    def profile(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "profile", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))

    @region.setter
    def region(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "region", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="s3ForcePathStyle")
    def s3_force_path_style(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "s3ForcePathStyle"))

    @s3_force_path_style.setter
    def s3_force_path_style(
        self,
        value: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]],
    ) -> None:
        jsii.set(self, "s3ForcePathStyle", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="secretKey")
    def secret_key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretKey"))

    @secret_key.setter
    def secret_key(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "secretKey", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sharedCredentialsFile")
    def shared_credentials_file(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sharedCredentialsFile"))

    @shared_credentials_file.setter
    def shared_credentials_file(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "sharedCredentialsFile", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="skipCredentialsValidation")
    def skip_credentials_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "skipCredentialsValidation"))

    @skip_credentials_validation.setter
    def skip_credentials_validation(
        self,
        value: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]],
    ) -> None:
        jsii.set(self, "skipCredentialsValidation", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="skipGetEc2Platforms")
    def skip_get_ec2_platforms(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "skipGetEc2Platforms"))

    @skip_get_ec2_platforms.setter
    def skip_get_ec2_platforms(
        self,
        value: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]],
    ) -> None:
        jsii.set(self, "skipGetEc2Platforms", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="skipMetadataApiCheck")
    def skip_metadata_api_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "skipMetadataApiCheck"))

    @skip_metadata_api_check.setter
    def skip_metadata_api_check(
        self,
        value: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]],
    ) -> None:
        jsii.set(self, "skipMetadataApiCheck", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="skipRegionValidation")
    def skip_region_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "skipRegionValidation"))

    @skip_region_validation.setter
    def skip_region_validation(
        self,
        value: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]],
    ) -> None:
        jsii.set(self, "skipRegionValidation", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="skipRequestingAccountId")
    def skip_requesting_account_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "skipRequestingAccountId"))

    @skip_requesting_account_id.setter
    def skip_requesting_account_id(
        self,
        value: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]],
    ) -> None:
        jsii.set(self, "skipRequestingAccountId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="token")
    def token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "token"))

    @token.setter
    def token(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "token", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.AwsProviderAssumeRole",
    jsii_struct_bases=[],
    name_mapping={
        "duration_seconds": "durationSeconds",
        "external_id": "externalId",
        "policy": "policy",
        "policy_arns": "policyArns",
        "role_arn": "roleArn",
        "session_name": "sessionName",
        "tags": "tags",
        "transitive_tag_keys": "transitiveTagKeys",
    },
)
class AwsProviderAssumeRole:
    def __init__(
        self,
        *,
        duration_seconds: typing.Optional[jsii.Number] = None,
        external_id: typing.Optional[builtins.str] = None,
        policy: typing.Optional[builtins.str] = None,
        policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        session_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        transitive_tag_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param duration_seconds: Seconds to restrict the assume role session duration. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#duration_seconds AwsProvider#duration_seconds}
        :param external_id: Unique identifier that might be required for assuming a role in another account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#external_id AwsProvider#external_id}
        :param policy: IAM Policy JSON describing further restricting permissions for the IAM Role being assumed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#policy AwsProvider#policy}
        :param policy_arns: Amazon Resource Names (ARNs) of IAM Policies describing further restricting permissions for the IAM Role being assumed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#policy_arns AwsProvider#policy_arns}
        :param role_arn: Amazon Resource Name of an IAM Role to assume prior to making API calls. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#role_arn AwsProvider#role_arn}
        :param session_name: Identifier for the assumed role session. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#session_name AwsProvider#session_name}
        :param tags: Assume role session tags. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#tags AwsProvider#tags}
        :param transitive_tag_keys: Assume role session tag keys to pass to any subsequent sessions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#transitive_tag_keys AwsProvider#transitive_tag_keys}
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if duration_seconds is not None:
            self._values["duration_seconds"] = duration_seconds
        if external_id is not None:
            self._values["external_id"] = external_id
        if policy is not None:
            self._values["policy"] = policy
        if policy_arns is not None:
            self._values["policy_arns"] = policy_arns
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if session_name is not None:
            self._values["session_name"] = session_name
        if tags is not None:
            self._values["tags"] = tags
        if transitive_tag_keys is not None:
            self._values["transitive_tag_keys"] = transitive_tag_keys

    @builtins.property
    def duration_seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds to restrict the assume role session duration.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#duration_seconds AwsProvider#duration_seconds}
        '''
        result = self._values.get("duration_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def external_id(self) -> typing.Optional[builtins.str]:
        '''Unique identifier that might be required for assuming a role in another account.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#external_id AwsProvider#external_id}
        '''
        result = self._values.get("external_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''IAM Policy JSON describing further restricting permissions for the IAM Role being assumed.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#policy AwsProvider#policy}
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Amazon Resource Names (ARNs) of IAM Policies describing further restricting permissions for the IAM Role being assumed.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#policy_arns AwsProvider#policy_arns}
        '''
        result = self._values.get("policy_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''Amazon Resource Name of an IAM Role to assume prior to making API calls.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#role_arn AwsProvider#role_arn}
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_name(self) -> typing.Optional[builtins.str]:
        '''Identifier for the assumed role session.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#session_name AwsProvider#session_name}
        '''
        result = self._values.get("session_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        '''Assume role session tags.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#tags AwsProvider#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def transitive_tag_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Assume role session tag keys to pass to any subsequent sessions.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#transitive_tag_keys AwsProvider#transitive_tag_keys}
        '''
        result = self._values.get("transitive_tag_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsProviderAssumeRole(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AwsProviderAssumeRoleOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.AwsProviderAssumeRoleOutputReference",
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

    @jsii.member(jsii_name="resetDurationSeconds")
    def reset_duration_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDurationSeconds", []))

    @jsii.member(jsii_name="resetExternalId")
    def reset_external_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalId", []))

    @jsii.member(jsii_name="resetPolicy")
    def reset_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicy", []))

    @jsii.member(jsii_name="resetPolicyArns")
    def reset_policy_arns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyArns", []))

    @jsii.member(jsii_name="resetRoleArn")
    def reset_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoleArn", []))

    @jsii.member(jsii_name="resetSessionName")
    def reset_session_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionName", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTransitiveTagKeys")
    def reset_transitive_tag_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransitiveTagKeys", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="durationSecondsInput")
    def duration_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "durationSecondsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="externalIdInput")
    def external_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policyArnsInput")
    def policy_arns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "policyArnsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policyInput")
    def policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sessionNameInput")
    def session_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionNameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tagsInput")
    def tags_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "tagsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="transitiveTagKeysInput")
    def transitive_tag_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "transitiveTagKeysInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="durationSeconds")
    def duration_seconds(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "durationSeconds"))

    @duration_seconds.setter
    def duration_seconds(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "durationSeconds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="externalId")
    def external_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalId"))

    @external_id.setter
    def external_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "externalId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "policy", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policyArns")
    def policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "policyArns"))

    @policy_arns.setter
    def policy_arns(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "policyArns", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "roleArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sessionName")
    def session_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionName"))

    @session_name.setter
    def session_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "sessionName", value)

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
    @jsii.member(jsii_name="transitiveTagKeys")
    def transitive_tag_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "transitiveTagKeys"))

    @transitive_tag_keys.setter
    def transitive_tag_keys(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "transitiveTagKeys", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.AwsProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "region": "region",
        "access_key": "accessKey",
        "alias": "alias",
        "allowed_account_ids": "allowedAccountIds",
        "assume_role": "assumeRole",
        "default_tags": "defaultTags",
        "endpoints": "endpoints",
        "forbidden_account_ids": "forbiddenAccountIds",
        "http_proxy": "httpProxy",
        "ignore_tags": "ignoreTags",
        "insecure": "insecure",
        "max_retries": "maxRetries",
        "profile": "profile",
        "s3_force_path_style": "s3ForcePathStyle",
        "secret_key": "secretKey",
        "shared_credentials_file": "sharedCredentialsFile",
        "skip_credentials_validation": "skipCredentialsValidation",
        "skip_get_ec2_platforms": "skipGetEc2Platforms",
        "skip_metadata_api_check": "skipMetadataApiCheck",
        "skip_region_validation": "skipRegionValidation",
        "skip_requesting_account_id": "skipRequestingAccountId",
        "token": "token",
    },
)
class AwsProviderConfig:
    def __init__(
        self,
        *,
        region: builtins.str,
        access_key: typing.Optional[builtins.str] = None,
        alias: typing.Optional[builtins.str] = None,
        allowed_account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        assume_role: typing.Optional[AwsProviderAssumeRole] = None,
        default_tags: typing.Optional["AwsProviderDefaultTags"] = None,
        endpoints: typing.Optional[typing.Sequence["AwsProviderEndpoints"]] = None,
        forbidden_account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        http_proxy: typing.Optional[builtins.str] = None,
        ignore_tags: typing.Optional["AwsProviderIgnoreTags"] = None,
        insecure: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        profile: typing.Optional[builtins.str] = None,
        s3_force_path_style: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        secret_key: typing.Optional[builtins.str] = None,
        shared_credentials_file: typing.Optional[builtins.str] = None,
        skip_credentials_validation: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        skip_get_ec2_platforms: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        skip_metadata_api_check: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        skip_region_validation: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        skip_requesting_account_id: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param region: The region where AWS operations will take place. Examples are us-east-1, us-west-2, etc. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#region AwsProvider#region}
        :param access_key: The access key for API operations. You can retrieve this from the 'Security & Credentials' section of the AWS console. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#access_key AwsProvider#access_key}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#alias AwsProvider#alias}
        :param allowed_account_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#allowed_account_ids AwsProvider#allowed_account_ids}.
        :param assume_role: assume_role block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#assume_role AwsProvider#assume_role}
        :param default_tags: default_tags block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#default_tags AwsProvider#default_tags}
        :param endpoints: endpoints block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#endpoints AwsProvider#endpoints}
        :param forbidden_account_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#forbidden_account_ids AwsProvider#forbidden_account_ids}.
        :param http_proxy: The address of an HTTP proxy to use when accessing the AWS API. Can also be configured using the ``HTTP_PROXY`` or ``HTTPS_PROXY`` environment variables. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#http_proxy AwsProvider#http_proxy}
        :param ignore_tags: ignore_tags block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#ignore_tags AwsProvider#ignore_tags}
        :param insecure: Explicitly allow the provider to perform "insecure" SSL requests. If omitted, default value is ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#insecure AwsProvider#insecure}
        :param max_retries: The maximum number of times an AWS API request is being executed. If the API request still fails, an error is thrown. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#max_retries AwsProvider#max_retries}
        :param profile: The profile for API operations. If not set, the default profile created with ``aws configure`` will be used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#profile AwsProvider#profile}
        :param s3_force_path_style: Set this to true to force the request to use path-style addressing, i.e., http://s3.amazonaws.com/BUCKET/KEY. By default, the S3 client will use virtual hosted bucket addressing when possible (http://BUCKET.s3.amazonaws.com/KEY). Specific to the Amazon S3 service. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#s3_force_path_style AwsProvider#s3_force_path_style}
        :param secret_key: The secret key for API operations. You can retrieve this from the 'Security & Credentials' section of the AWS console. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#secret_key AwsProvider#secret_key}
        :param shared_credentials_file: The path to the shared credentials file. If not set this defaults to ~/.aws/credentials. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#shared_credentials_file AwsProvider#shared_credentials_file}
        :param skip_credentials_validation: Skip the credentials validation via STS API. Used for AWS API implementations that do not have STS available/implemented. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#skip_credentials_validation AwsProvider#skip_credentials_validation}
        :param skip_get_ec2_platforms: Skip getting the supported EC2 platforms. Used by users that don't have ec2:DescribeAccountAttributes permissions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#skip_get_ec2_platforms AwsProvider#skip_get_ec2_platforms}
        :param skip_metadata_api_check: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#skip_metadata_api_check AwsProvider#skip_metadata_api_check}.
        :param skip_region_validation: Skip static validation of region name. Used by users of alternative AWS-like APIs or users w/ access to regions that are not public (yet). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#skip_region_validation AwsProvider#skip_region_validation}
        :param skip_requesting_account_id: Skip requesting the account ID. Used for AWS API implementations that do not have IAM/STS API and/or metadata API. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#skip_requesting_account_id AwsProvider#skip_requesting_account_id}
        :param token: session token. A session token is only required if you are using temporary security credentials. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#token AwsProvider#token}
        '''
        if isinstance(assume_role, dict):
            assume_role = AwsProviderAssumeRole(**assume_role)
        if isinstance(default_tags, dict):
            default_tags = AwsProviderDefaultTags(**default_tags)
        if isinstance(ignore_tags, dict):
            ignore_tags = AwsProviderIgnoreTags(**ignore_tags)
        self._values: typing.Dict[str, typing.Any] = {
            "region": region,
        }
        if access_key is not None:
            self._values["access_key"] = access_key
        if alias is not None:
            self._values["alias"] = alias
        if allowed_account_ids is not None:
            self._values["allowed_account_ids"] = allowed_account_ids
        if assume_role is not None:
            self._values["assume_role"] = assume_role
        if default_tags is not None:
            self._values["default_tags"] = default_tags
        if endpoints is not None:
            self._values["endpoints"] = endpoints
        if forbidden_account_ids is not None:
            self._values["forbidden_account_ids"] = forbidden_account_ids
        if http_proxy is not None:
            self._values["http_proxy"] = http_proxy
        if ignore_tags is not None:
            self._values["ignore_tags"] = ignore_tags
        if insecure is not None:
            self._values["insecure"] = insecure
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if profile is not None:
            self._values["profile"] = profile
        if s3_force_path_style is not None:
            self._values["s3_force_path_style"] = s3_force_path_style
        if secret_key is not None:
            self._values["secret_key"] = secret_key
        if shared_credentials_file is not None:
            self._values["shared_credentials_file"] = shared_credentials_file
        if skip_credentials_validation is not None:
            self._values["skip_credentials_validation"] = skip_credentials_validation
        if skip_get_ec2_platforms is not None:
            self._values["skip_get_ec2_platforms"] = skip_get_ec2_platforms
        if skip_metadata_api_check is not None:
            self._values["skip_metadata_api_check"] = skip_metadata_api_check
        if skip_region_validation is not None:
            self._values["skip_region_validation"] = skip_region_validation
        if skip_requesting_account_id is not None:
            self._values["skip_requesting_account_id"] = skip_requesting_account_id
        if token is not None:
            self._values["token"] = token

    @builtins.property
    def region(self) -> builtins.str:
        '''The region where AWS operations will take place. Examples are us-east-1, us-west-2, etc.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#region AwsProvider#region}
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_key(self) -> typing.Optional[builtins.str]:
        '''The access key for API operations. You can retrieve this from the 'Security & Credentials' section of the AWS console.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#access_key AwsProvider#access_key}
        '''
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#alias AwsProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allowed_account_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#allowed_account_ids AwsProvider#allowed_account_ids}.'''
        result = self._values.get("allowed_account_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def assume_role(self) -> typing.Optional[AwsProviderAssumeRole]:
        '''assume_role block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#assume_role AwsProvider#assume_role}
        '''
        result = self._values.get("assume_role")
        return typing.cast(typing.Optional[AwsProviderAssumeRole], result)

    @builtins.property
    def default_tags(self) -> typing.Optional["AwsProviderDefaultTags"]:
        '''default_tags block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#default_tags AwsProvider#default_tags}
        '''
        result = self._values.get("default_tags")
        return typing.cast(typing.Optional["AwsProviderDefaultTags"], result)

    @builtins.property
    def endpoints(self) -> typing.Optional[typing.List["AwsProviderEndpoints"]]:
        '''endpoints block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#endpoints AwsProvider#endpoints}
        '''
        result = self._values.get("endpoints")
        return typing.cast(typing.Optional[typing.List["AwsProviderEndpoints"]], result)

    @builtins.property
    def forbidden_account_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#forbidden_account_ids AwsProvider#forbidden_account_ids}.'''
        result = self._values.get("forbidden_account_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def http_proxy(self) -> typing.Optional[builtins.str]:
        '''The address of an HTTP proxy to use when accessing the AWS API.

        Can also be configured using the ``HTTP_PROXY`` or ``HTTPS_PROXY`` environment variables.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#http_proxy AwsProvider#http_proxy}
        '''
        result = self._values.get("http_proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_tags(self) -> typing.Optional["AwsProviderIgnoreTags"]:
        '''ignore_tags block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#ignore_tags AwsProvider#ignore_tags}
        '''
        result = self._values.get("ignore_tags")
        return typing.cast(typing.Optional["AwsProviderIgnoreTags"], result)

    @builtins.property
    def insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Explicitly allow the provider to perform "insecure" SSL requests. If omitted, default value is ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#insecure AwsProvider#insecure}
        '''
        result = self._values.get("insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of times an AWS API request is being executed.

        If the API request still fails, an error is
        thrown.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#max_retries AwsProvider#max_retries}
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def profile(self) -> typing.Optional[builtins.str]:
        '''The profile for API operations. If not set, the default profile created with ``aws configure`` will be used.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#profile AwsProvider#profile}
        '''
        result = self._values.get("profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_force_path_style(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Set this to true to force the request to use path-style addressing, i.e., http://s3.amazonaws.com/BUCKET/KEY. By default, the S3 client will use virtual hosted bucket addressing when possible (http://BUCKET.s3.amazonaws.com/KEY). Specific to the Amazon S3 service.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#s3_force_path_style AwsProvider#s3_force_path_style}
        '''
        result = self._values.get("s3_force_path_style")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def secret_key(self) -> typing.Optional[builtins.str]:
        '''The secret key for API operations. You can retrieve this from the 'Security & Credentials' section of the AWS console.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#secret_key AwsProvider#secret_key}
        '''
        result = self._values.get("secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shared_credentials_file(self) -> typing.Optional[builtins.str]:
        '''The path to the shared credentials file. If not set this defaults to ~/.aws/credentials.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#shared_credentials_file AwsProvider#shared_credentials_file}
        '''
        result = self._values.get("shared_credentials_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_credentials_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Skip the credentials validation via STS API. Used for AWS API implementations that do not have STS available/implemented.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#skip_credentials_validation AwsProvider#skip_credentials_validation}
        '''
        result = self._values.get("skip_credentials_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def skip_get_ec2_platforms(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Skip getting the supported EC2 platforms. Used by users that don't have ec2:DescribeAccountAttributes permissions.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#skip_get_ec2_platforms AwsProvider#skip_get_ec2_platforms}
        '''
        result = self._values.get("skip_get_ec2_platforms")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def skip_metadata_api_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#skip_metadata_api_check AwsProvider#skip_metadata_api_check}.'''
        result = self._values.get("skip_metadata_api_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def skip_region_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Skip static validation of region name.

        Used by users of alternative AWS-like APIs or users w/ access to regions that are not public (yet).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#skip_region_validation AwsProvider#skip_region_validation}
        '''
        result = self._values.get("skip_region_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def skip_requesting_account_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Skip requesting the account ID. Used for AWS API implementations that do not have IAM/STS API and/or metadata API.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#skip_requesting_account_id AwsProvider#skip_requesting_account_id}
        '''
        result = self._values.get("skip_requesting_account_id")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''session token. A session token is only required if you are using temporary security credentials.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#token AwsProvider#token}
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.AwsProviderDefaultTags",
    jsii_struct_bases=[],
    name_mapping={"tags": "tags"},
)
class AwsProviderDefaultTags:
    def __init__(
        self,
        *,
        tags: typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    ) -> None:
        '''
        :param tags: Resource tags to default across all resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#tags AwsProvider#tags}
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        '''Resource tags to default across all resources.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#tags AwsProvider#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsProviderDefaultTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AwsProviderDefaultTagsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.AwsProviderDefaultTagsOutputReference",
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

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tagsInput")
    def tags_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "tagsInput"))

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


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.AwsProviderEndpoints",
    jsii_struct_bases=[],
    name_mapping={
        "accessanalyzer": "accessanalyzer",
        "acm": "acm",
        "acmpca": "acmpca",
        "amplify": "amplify",
        "apigateway": "apigateway",
        "appconfig": "appconfig",
        "applicationautoscaling": "applicationautoscaling",
        "applicationinsights": "applicationinsights",
        "appmesh": "appmesh",
        "apprunner": "apprunner",
        "appstream": "appstream",
        "appsync": "appsync",
        "athena": "athena",
        "auditmanager": "auditmanager",
        "autoscaling": "autoscaling",
        "autoscalingplans": "autoscalingplans",
        "backup": "backup",
        "batch": "batch",
        "budgets": "budgets",
        "chime": "chime",
        "cloud9": "cloud9",
        "cloudcontrolapi": "cloudcontrolapi",
        "cloudformation": "cloudformation",
        "cloudfront": "cloudfront",
        "cloudhsm": "cloudhsm",
        "cloudsearch": "cloudsearch",
        "cloudtrail": "cloudtrail",
        "cloudwatch": "cloudwatch",
        "cloudwatchevents": "cloudwatchevents",
        "cloudwatchlogs": "cloudwatchlogs",
        "codeartifact": "codeartifact",
        "codebuild": "codebuild",
        "codecommit": "codecommit",
        "codedeploy": "codedeploy",
        "codepipeline": "codepipeline",
        "codestarconnections": "codestarconnections",
        "cognitoidentity": "cognitoidentity",
        "cognitoidp": "cognitoidp",
        "configservice": "configservice",
        "connect": "connect",
        "cur": "cur",
        "dataexchange": "dataexchange",
        "datapipeline": "datapipeline",
        "datasync": "datasync",
        "dax": "dax",
        "detective": "detective",
        "devicefarm": "devicefarm",
        "directconnect": "directconnect",
        "dlm": "dlm",
        "dms": "dms",
        "docdb": "docdb",
        "ds": "ds",
        "dynamodb": "dynamodb",
        "ec2": "ec2",
        "ecr": "ecr",
        "ecrpublic": "ecrpublic",
        "ecs": "ecs",
        "efs": "efs",
        "eks": "eks",
        "elasticache": "elasticache",
        "elasticbeanstalk": "elasticbeanstalk",
        "elastictranscoder": "elastictranscoder",
        "elb": "elb",
        "emr": "emr",
        "emrcontainers": "emrcontainers",
        "es": "es",
        "firehose": "firehose",
        "fms": "fms",
        "forecast": "forecast",
        "fsx": "fsx",
        "gamelift": "gamelift",
        "glacier": "glacier",
        "globalaccelerator": "globalaccelerator",
        "glue": "glue",
        "greengrass": "greengrass",
        "guardduty": "guardduty",
        "iam": "iam",
        "identitystore": "identitystore",
        "imagebuilder": "imagebuilder",
        "inspector": "inspector",
        "iot": "iot",
        "iotanalytics": "iotanalytics",
        "iotevents": "iotevents",
        "kafka": "kafka",
        "kinesis": "kinesis",
        "kinesisanalytics": "kinesisanalytics",
        "kinesisanalyticsv2": "kinesisanalyticsv2",
        "kinesisvideo": "kinesisvideo",
        "kms": "kms",
        "lakeformation": "lakeformation",
        "lambda_": "lambda",
        "lexmodels": "lexmodels",
        "licensemanager": "licensemanager",
        "lightsail": "lightsail",
        "location": "location",
        "macie": "macie",
        "macie2": "macie2",
        "managedblockchain": "managedblockchain",
        "marketplacecatalog": "marketplacecatalog",
        "mediaconnect": "mediaconnect",
        "mediaconvert": "mediaconvert",
        "medialive": "medialive",
        "mediapackage": "mediapackage",
        "mediastore": "mediastore",
        "mediastoredata": "mediastoredata",
        "memorydb": "memorydb",
        "mq": "mq",
        "mwaa": "mwaa",
        "neptune": "neptune",
        "networkfirewall": "networkfirewall",
        "networkmanager": "networkmanager",
        "opsworks": "opsworks",
        "organizations": "organizations",
        "outposts": "outposts",
        "personalize": "personalize",
        "pinpoint": "pinpoint",
        "pricing": "pricing",
        "qldb": "qldb",
        "quicksight": "quicksight",
        "ram": "ram",
        "rds": "rds",
        "redshift": "redshift",
        "resourcegroups": "resourcegroups",
        "resourcegroupstaggingapi": "resourcegroupstaggingapi",
        "route53": "route53",
        "route53_domains": "route53Domains",
        "route53_recoverycontrolconfig": "route53Recoverycontrolconfig",
        "route53_recoveryreadiness": "route53Recoveryreadiness",
        "route53_resolver": "route53Resolver",
        "s3": "s3",
        "s3_control": "s3Control",
        "s3_outposts": "s3Outposts",
        "sagemaker": "sagemaker",
        "schemas": "schemas",
        "sdb": "sdb",
        "secretsmanager": "secretsmanager",
        "securityhub": "securityhub",
        "serverlessrepo": "serverlessrepo",
        "servicecatalog": "servicecatalog",
        "servicediscovery": "servicediscovery",
        "servicequotas": "servicequotas",
        "ses": "ses",
        "shield": "shield",
        "signer": "signer",
        "sns": "sns",
        "sqs": "sqs",
        "ssm": "ssm",
        "ssoadmin": "ssoadmin",
        "stepfunctions": "stepfunctions",
        "storagegateway": "storagegateway",
        "sts": "sts",
        "swf": "swf",
        "synthetics": "synthetics",
        "timestreamwrite": "timestreamwrite",
        "transfer": "transfer",
        "waf": "waf",
        "wafregional": "wafregional",
        "wafv2": "wafv2",
        "worklink": "worklink",
        "workmail": "workmail",
        "workspaces": "workspaces",
        "xray": "xray",
    },
)
class AwsProviderEndpoints:
    def __init__(
        self,
        *,
        accessanalyzer: typing.Optional[builtins.str] = None,
        acm: typing.Optional[builtins.str] = None,
        acmpca: typing.Optional[builtins.str] = None,
        amplify: typing.Optional[builtins.str] = None,
        apigateway: typing.Optional[builtins.str] = None,
        appconfig: typing.Optional[builtins.str] = None,
        applicationautoscaling: typing.Optional[builtins.str] = None,
        applicationinsights: typing.Optional[builtins.str] = None,
        appmesh: typing.Optional[builtins.str] = None,
        apprunner: typing.Optional[builtins.str] = None,
        appstream: typing.Optional[builtins.str] = None,
        appsync: typing.Optional[builtins.str] = None,
        athena: typing.Optional[builtins.str] = None,
        auditmanager: typing.Optional[builtins.str] = None,
        autoscaling: typing.Optional[builtins.str] = None,
        autoscalingplans: typing.Optional[builtins.str] = None,
        backup: typing.Optional[builtins.str] = None,
        batch: typing.Optional[builtins.str] = None,
        budgets: typing.Optional[builtins.str] = None,
        chime: typing.Optional[builtins.str] = None,
        cloud9: typing.Optional[builtins.str] = None,
        cloudcontrolapi: typing.Optional[builtins.str] = None,
        cloudformation: typing.Optional[builtins.str] = None,
        cloudfront: typing.Optional[builtins.str] = None,
        cloudhsm: typing.Optional[builtins.str] = None,
        cloudsearch: typing.Optional[builtins.str] = None,
        cloudtrail: typing.Optional[builtins.str] = None,
        cloudwatch: typing.Optional[builtins.str] = None,
        cloudwatchevents: typing.Optional[builtins.str] = None,
        cloudwatchlogs: typing.Optional[builtins.str] = None,
        codeartifact: typing.Optional[builtins.str] = None,
        codebuild: typing.Optional[builtins.str] = None,
        codecommit: typing.Optional[builtins.str] = None,
        codedeploy: typing.Optional[builtins.str] = None,
        codepipeline: typing.Optional[builtins.str] = None,
        codestarconnections: typing.Optional[builtins.str] = None,
        cognitoidentity: typing.Optional[builtins.str] = None,
        cognitoidp: typing.Optional[builtins.str] = None,
        configservice: typing.Optional[builtins.str] = None,
        connect: typing.Optional[builtins.str] = None,
        cur: typing.Optional[builtins.str] = None,
        dataexchange: typing.Optional[builtins.str] = None,
        datapipeline: typing.Optional[builtins.str] = None,
        datasync: typing.Optional[builtins.str] = None,
        dax: typing.Optional[builtins.str] = None,
        detective: typing.Optional[builtins.str] = None,
        devicefarm: typing.Optional[builtins.str] = None,
        directconnect: typing.Optional[builtins.str] = None,
        dlm: typing.Optional[builtins.str] = None,
        dms: typing.Optional[builtins.str] = None,
        docdb: typing.Optional[builtins.str] = None,
        ds: typing.Optional[builtins.str] = None,
        dynamodb: typing.Optional[builtins.str] = None,
        ec2: typing.Optional[builtins.str] = None,
        ecr: typing.Optional[builtins.str] = None,
        ecrpublic: typing.Optional[builtins.str] = None,
        ecs: typing.Optional[builtins.str] = None,
        efs: typing.Optional[builtins.str] = None,
        eks: typing.Optional[builtins.str] = None,
        elasticache: typing.Optional[builtins.str] = None,
        elasticbeanstalk: typing.Optional[builtins.str] = None,
        elastictranscoder: typing.Optional[builtins.str] = None,
        elb: typing.Optional[builtins.str] = None,
        emr: typing.Optional[builtins.str] = None,
        emrcontainers: typing.Optional[builtins.str] = None,
        es: typing.Optional[builtins.str] = None,
        firehose: typing.Optional[builtins.str] = None,
        fms: typing.Optional[builtins.str] = None,
        forecast: typing.Optional[builtins.str] = None,
        fsx: typing.Optional[builtins.str] = None,
        gamelift: typing.Optional[builtins.str] = None,
        glacier: typing.Optional[builtins.str] = None,
        globalaccelerator: typing.Optional[builtins.str] = None,
        glue: typing.Optional[builtins.str] = None,
        greengrass: typing.Optional[builtins.str] = None,
        guardduty: typing.Optional[builtins.str] = None,
        iam: typing.Optional[builtins.str] = None,
        identitystore: typing.Optional[builtins.str] = None,
        imagebuilder: typing.Optional[builtins.str] = None,
        inspector: typing.Optional[builtins.str] = None,
        iot: typing.Optional[builtins.str] = None,
        iotanalytics: typing.Optional[builtins.str] = None,
        iotevents: typing.Optional[builtins.str] = None,
        kafka: typing.Optional[builtins.str] = None,
        kinesis: typing.Optional[builtins.str] = None,
        kinesisanalytics: typing.Optional[builtins.str] = None,
        kinesisanalyticsv2: typing.Optional[builtins.str] = None,
        kinesisvideo: typing.Optional[builtins.str] = None,
        kms: typing.Optional[builtins.str] = None,
        lakeformation: typing.Optional[builtins.str] = None,
        lambda_: typing.Optional[builtins.str] = None,
        lexmodels: typing.Optional[builtins.str] = None,
        licensemanager: typing.Optional[builtins.str] = None,
        lightsail: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        macie: typing.Optional[builtins.str] = None,
        macie2: typing.Optional[builtins.str] = None,
        managedblockchain: typing.Optional[builtins.str] = None,
        marketplacecatalog: typing.Optional[builtins.str] = None,
        mediaconnect: typing.Optional[builtins.str] = None,
        mediaconvert: typing.Optional[builtins.str] = None,
        medialive: typing.Optional[builtins.str] = None,
        mediapackage: typing.Optional[builtins.str] = None,
        mediastore: typing.Optional[builtins.str] = None,
        mediastoredata: typing.Optional[builtins.str] = None,
        memorydb: typing.Optional[builtins.str] = None,
        mq: typing.Optional[builtins.str] = None,
        mwaa: typing.Optional[builtins.str] = None,
        neptune: typing.Optional[builtins.str] = None,
        networkfirewall: typing.Optional[builtins.str] = None,
        networkmanager: typing.Optional[builtins.str] = None,
        opsworks: typing.Optional[builtins.str] = None,
        organizations: typing.Optional[builtins.str] = None,
        outposts: typing.Optional[builtins.str] = None,
        personalize: typing.Optional[builtins.str] = None,
        pinpoint: typing.Optional[builtins.str] = None,
        pricing: typing.Optional[builtins.str] = None,
        qldb: typing.Optional[builtins.str] = None,
        quicksight: typing.Optional[builtins.str] = None,
        ram: typing.Optional[builtins.str] = None,
        rds: typing.Optional[builtins.str] = None,
        redshift: typing.Optional[builtins.str] = None,
        resourcegroups: typing.Optional[builtins.str] = None,
        resourcegroupstaggingapi: typing.Optional[builtins.str] = None,
        route53: typing.Optional[builtins.str] = None,
        route53_domains: typing.Optional[builtins.str] = None,
        route53_recoverycontrolconfig: typing.Optional[builtins.str] = None,
        route53_recoveryreadiness: typing.Optional[builtins.str] = None,
        route53_resolver: typing.Optional[builtins.str] = None,
        s3: typing.Optional[builtins.str] = None,
        s3_control: typing.Optional[builtins.str] = None,
        s3_outposts: typing.Optional[builtins.str] = None,
        sagemaker: typing.Optional[builtins.str] = None,
        schemas: typing.Optional[builtins.str] = None,
        sdb: typing.Optional[builtins.str] = None,
        secretsmanager: typing.Optional[builtins.str] = None,
        securityhub: typing.Optional[builtins.str] = None,
        serverlessrepo: typing.Optional[builtins.str] = None,
        servicecatalog: typing.Optional[builtins.str] = None,
        servicediscovery: typing.Optional[builtins.str] = None,
        servicequotas: typing.Optional[builtins.str] = None,
        ses: typing.Optional[builtins.str] = None,
        shield: typing.Optional[builtins.str] = None,
        signer: typing.Optional[builtins.str] = None,
        sns: typing.Optional[builtins.str] = None,
        sqs: typing.Optional[builtins.str] = None,
        ssm: typing.Optional[builtins.str] = None,
        ssoadmin: typing.Optional[builtins.str] = None,
        stepfunctions: typing.Optional[builtins.str] = None,
        storagegateway: typing.Optional[builtins.str] = None,
        sts: typing.Optional[builtins.str] = None,
        swf: typing.Optional[builtins.str] = None,
        synthetics: typing.Optional[builtins.str] = None,
        timestreamwrite: typing.Optional[builtins.str] = None,
        transfer: typing.Optional[builtins.str] = None,
        waf: typing.Optional[builtins.str] = None,
        wafregional: typing.Optional[builtins.str] = None,
        wafv2: typing.Optional[builtins.str] = None,
        worklink: typing.Optional[builtins.str] = None,
        workmail: typing.Optional[builtins.str] = None,
        workspaces: typing.Optional[builtins.str] = None,
        xray: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accessanalyzer: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#accessanalyzer AwsProvider#accessanalyzer}
        :param acm: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#acm AwsProvider#acm}
        :param acmpca: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#acmpca AwsProvider#acmpca}
        :param amplify: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#amplify AwsProvider#amplify}
        :param apigateway: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#apigateway AwsProvider#apigateway}
        :param appconfig: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#appconfig AwsProvider#appconfig}
        :param applicationautoscaling: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#applicationautoscaling AwsProvider#applicationautoscaling}
        :param applicationinsights: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#applicationinsights AwsProvider#applicationinsights}
        :param appmesh: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#appmesh AwsProvider#appmesh}
        :param apprunner: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#apprunner AwsProvider#apprunner}
        :param appstream: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#appstream AwsProvider#appstream}
        :param appsync: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#appsync AwsProvider#appsync}
        :param athena: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#athena AwsProvider#athena}
        :param auditmanager: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#auditmanager AwsProvider#auditmanager}
        :param autoscaling: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#autoscaling AwsProvider#autoscaling}
        :param autoscalingplans: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#autoscalingplans AwsProvider#autoscalingplans}
        :param backup: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#backup AwsProvider#backup}
        :param batch: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#batch AwsProvider#batch}
        :param budgets: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#budgets AwsProvider#budgets}
        :param chime: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#chime AwsProvider#chime}
        :param cloud9: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cloud9 AwsProvider#cloud9}
        :param cloudcontrolapi: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cloudcontrolapi AwsProvider#cloudcontrolapi}
        :param cloudformation: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cloudformation AwsProvider#cloudformation}
        :param cloudfront: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cloudfront AwsProvider#cloudfront}
        :param cloudhsm: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cloudhsm AwsProvider#cloudhsm}
        :param cloudsearch: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cloudsearch AwsProvider#cloudsearch}
        :param cloudtrail: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cloudtrail AwsProvider#cloudtrail}
        :param cloudwatch: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cloudwatch AwsProvider#cloudwatch}
        :param cloudwatchevents: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cloudwatchevents AwsProvider#cloudwatchevents}
        :param cloudwatchlogs: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cloudwatchlogs AwsProvider#cloudwatchlogs}
        :param codeartifact: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#codeartifact AwsProvider#codeartifact}
        :param codebuild: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#codebuild AwsProvider#codebuild}
        :param codecommit: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#codecommit AwsProvider#codecommit}
        :param codedeploy: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#codedeploy AwsProvider#codedeploy}
        :param codepipeline: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#codepipeline AwsProvider#codepipeline}
        :param codestarconnections: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#codestarconnections AwsProvider#codestarconnections}
        :param cognitoidentity: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cognitoidentity AwsProvider#cognitoidentity}
        :param cognitoidp: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cognitoidp AwsProvider#cognitoidp}
        :param configservice: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#configservice AwsProvider#configservice}
        :param connect: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#connect AwsProvider#connect}
        :param cur: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cur AwsProvider#cur}
        :param dataexchange: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#dataexchange AwsProvider#dataexchange}
        :param datapipeline: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#datapipeline AwsProvider#datapipeline}
        :param datasync: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#datasync AwsProvider#datasync}
        :param dax: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#dax AwsProvider#dax}
        :param detective: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#detective AwsProvider#detective}
        :param devicefarm: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#devicefarm AwsProvider#devicefarm}
        :param directconnect: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#directconnect AwsProvider#directconnect}
        :param dlm: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#dlm AwsProvider#dlm}
        :param dms: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#dms AwsProvider#dms}
        :param docdb: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#docdb AwsProvider#docdb}
        :param ds: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#ds AwsProvider#ds}
        :param dynamodb: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#dynamodb AwsProvider#dynamodb}
        :param ec2: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#ec2 AwsProvider#ec2}
        :param ecr: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#ecr AwsProvider#ecr}
        :param ecrpublic: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#ecrpublic AwsProvider#ecrpublic}
        :param ecs: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#ecs AwsProvider#ecs}
        :param efs: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#efs AwsProvider#efs}
        :param eks: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#eks AwsProvider#eks}
        :param elasticache: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#elasticache AwsProvider#elasticache}
        :param elasticbeanstalk: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#elasticbeanstalk AwsProvider#elasticbeanstalk}
        :param elastictranscoder: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#elastictranscoder AwsProvider#elastictranscoder}
        :param elb: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#elb AwsProvider#elb}
        :param emr: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#emr AwsProvider#emr}
        :param emrcontainers: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#emrcontainers AwsProvider#emrcontainers}
        :param es: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#es AwsProvider#es}
        :param firehose: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#firehose AwsProvider#firehose}
        :param fms: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#fms AwsProvider#fms}
        :param forecast: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#forecast AwsProvider#forecast}
        :param fsx: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#fsx AwsProvider#fsx}
        :param gamelift: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#gamelift AwsProvider#gamelift}
        :param glacier: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#glacier AwsProvider#glacier}
        :param globalaccelerator: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#globalaccelerator AwsProvider#globalaccelerator}
        :param glue: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#glue AwsProvider#glue}
        :param greengrass: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#greengrass AwsProvider#greengrass}
        :param guardduty: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#guardduty AwsProvider#guardduty}
        :param iam: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#iam AwsProvider#iam}
        :param identitystore: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#identitystore AwsProvider#identitystore}
        :param imagebuilder: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#imagebuilder AwsProvider#imagebuilder}
        :param inspector: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#inspector AwsProvider#inspector}
        :param iot: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#iot AwsProvider#iot}
        :param iotanalytics: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#iotanalytics AwsProvider#iotanalytics}
        :param iotevents: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#iotevents AwsProvider#iotevents}
        :param kafka: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#kafka AwsProvider#kafka}
        :param kinesis: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#kinesis AwsProvider#kinesis}
        :param kinesisanalytics: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#kinesisanalytics AwsProvider#kinesisanalytics}
        :param kinesisanalyticsv2: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#kinesisanalyticsv2 AwsProvider#kinesisanalyticsv2}
        :param kinesisvideo: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#kinesisvideo AwsProvider#kinesisvideo}
        :param kms: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#kms AwsProvider#kms}
        :param lakeformation: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#lakeformation AwsProvider#lakeformation}
        :param lambda_: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#lambda AwsProvider#lambda}
        :param lexmodels: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#lexmodels AwsProvider#lexmodels}
        :param licensemanager: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#licensemanager AwsProvider#licensemanager}
        :param lightsail: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#lightsail AwsProvider#lightsail}
        :param location: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#location AwsProvider#location}
        :param macie: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#macie AwsProvider#macie}
        :param macie2: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#macie2 AwsProvider#macie2}
        :param managedblockchain: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#managedblockchain AwsProvider#managedblockchain}
        :param marketplacecatalog: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#marketplacecatalog AwsProvider#marketplacecatalog}
        :param mediaconnect: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#mediaconnect AwsProvider#mediaconnect}
        :param mediaconvert: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#mediaconvert AwsProvider#mediaconvert}
        :param medialive: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#medialive AwsProvider#medialive}
        :param mediapackage: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#mediapackage AwsProvider#mediapackage}
        :param mediastore: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#mediastore AwsProvider#mediastore}
        :param mediastoredata: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#mediastoredata AwsProvider#mediastoredata}
        :param memorydb: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#memorydb AwsProvider#memorydb}
        :param mq: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#mq AwsProvider#mq}
        :param mwaa: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#mwaa AwsProvider#mwaa}
        :param neptune: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#neptune AwsProvider#neptune}
        :param networkfirewall: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#networkfirewall AwsProvider#networkfirewall}
        :param networkmanager: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#networkmanager AwsProvider#networkmanager}
        :param opsworks: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#opsworks AwsProvider#opsworks}
        :param organizations: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#organizations AwsProvider#organizations}
        :param outposts: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#outposts AwsProvider#outposts}
        :param personalize: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#personalize AwsProvider#personalize}
        :param pinpoint: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#pinpoint AwsProvider#pinpoint}
        :param pricing: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#pricing AwsProvider#pricing}
        :param qldb: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#qldb AwsProvider#qldb}
        :param quicksight: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#quicksight AwsProvider#quicksight}
        :param ram: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#ram AwsProvider#ram}
        :param rds: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#rds AwsProvider#rds}
        :param redshift: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#redshift AwsProvider#redshift}
        :param resourcegroups: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#resourcegroups AwsProvider#resourcegroups}
        :param resourcegroupstaggingapi: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#resourcegroupstaggingapi AwsProvider#resourcegroupstaggingapi}
        :param route53: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#route53 AwsProvider#route53}
        :param route53_domains: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#route53domains AwsProvider#route53domains}
        :param route53_recoverycontrolconfig: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#route53recoverycontrolconfig AwsProvider#route53recoverycontrolconfig}
        :param route53_recoveryreadiness: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#route53recoveryreadiness AwsProvider#route53recoveryreadiness}
        :param route53_resolver: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#route53resolver AwsProvider#route53resolver}
        :param s3: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#s3 AwsProvider#s3}
        :param s3_control: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#s3control AwsProvider#s3control}
        :param s3_outposts: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#s3outposts AwsProvider#s3outposts}
        :param sagemaker: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#sagemaker AwsProvider#sagemaker}
        :param schemas: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#schemas AwsProvider#schemas}
        :param sdb: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#sdb AwsProvider#sdb}
        :param secretsmanager: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#secretsmanager AwsProvider#secretsmanager}
        :param securityhub: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#securityhub AwsProvider#securityhub}
        :param serverlessrepo: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#serverlessrepo AwsProvider#serverlessrepo}
        :param servicecatalog: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#servicecatalog AwsProvider#servicecatalog}
        :param servicediscovery: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#servicediscovery AwsProvider#servicediscovery}
        :param servicequotas: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#servicequotas AwsProvider#servicequotas}
        :param ses: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#ses AwsProvider#ses}
        :param shield: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#shield AwsProvider#shield}
        :param signer: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#signer AwsProvider#signer}
        :param sns: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#sns AwsProvider#sns}
        :param sqs: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#sqs AwsProvider#sqs}
        :param ssm: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#ssm AwsProvider#ssm}
        :param ssoadmin: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#ssoadmin AwsProvider#ssoadmin}
        :param stepfunctions: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#stepfunctions AwsProvider#stepfunctions}
        :param storagegateway: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#storagegateway AwsProvider#storagegateway}
        :param sts: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#sts AwsProvider#sts}
        :param swf: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#swf AwsProvider#swf}
        :param synthetics: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#synthetics AwsProvider#synthetics}
        :param timestreamwrite: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#timestreamwrite AwsProvider#timestreamwrite}
        :param transfer: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#transfer AwsProvider#transfer}
        :param waf: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#waf AwsProvider#waf}
        :param wafregional: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#wafregional AwsProvider#wafregional}
        :param wafv2: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#wafv2 AwsProvider#wafv2}
        :param worklink: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#worklink AwsProvider#worklink}
        :param workmail: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#workmail AwsProvider#workmail}
        :param workspaces: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#workspaces AwsProvider#workspaces}
        :param xray: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#xray AwsProvider#xray}
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if accessanalyzer is not None:
            self._values["accessanalyzer"] = accessanalyzer
        if acm is not None:
            self._values["acm"] = acm
        if acmpca is not None:
            self._values["acmpca"] = acmpca
        if amplify is not None:
            self._values["amplify"] = amplify
        if apigateway is not None:
            self._values["apigateway"] = apigateway
        if appconfig is not None:
            self._values["appconfig"] = appconfig
        if applicationautoscaling is not None:
            self._values["applicationautoscaling"] = applicationautoscaling
        if applicationinsights is not None:
            self._values["applicationinsights"] = applicationinsights
        if appmesh is not None:
            self._values["appmesh"] = appmesh
        if apprunner is not None:
            self._values["apprunner"] = apprunner
        if appstream is not None:
            self._values["appstream"] = appstream
        if appsync is not None:
            self._values["appsync"] = appsync
        if athena is not None:
            self._values["athena"] = athena
        if auditmanager is not None:
            self._values["auditmanager"] = auditmanager
        if autoscaling is not None:
            self._values["autoscaling"] = autoscaling
        if autoscalingplans is not None:
            self._values["autoscalingplans"] = autoscalingplans
        if backup is not None:
            self._values["backup"] = backup
        if batch is not None:
            self._values["batch"] = batch
        if budgets is not None:
            self._values["budgets"] = budgets
        if chime is not None:
            self._values["chime"] = chime
        if cloud9 is not None:
            self._values["cloud9"] = cloud9
        if cloudcontrolapi is not None:
            self._values["cloudcontrolapi"] = cloudcontrolapi
        if cloudformation is not None:
            self._values["cloudformation"] = cloudformation
        if cloudfront is not None:
            self._values["cloudfront"] = cloudfront
        if cloudhsm is not None:
            self._values["cloudhsm"] = cloudhsm
        if cloudsearch is not None:
            self._values["cloudsearch"] = cloudsearch
        if cloudtrail is not None:
            self._values["cloudtrail"] = cloudtrail
        if cloudwatch is not None:
            self._values["cloudwatch"] = cloudwatch
        if cloudwatchevents is not None:
            self._values["cloudwatchevents"] = cloudwatchevents
        if cloudwatchlogs is not None:
            self._values["cloudwatchlogs"] = cloudwatchlogs
        if codeartifact is not None:
            self._values["codeartifact"] = codeartifact
        if codebuild is not None:
            self._values["codebuild"] = codebuild
        if codecommit is not None:
            self._values["codecommit"] = codecommit
        if codedeploy is not None:
            self._values["codedeploy"] = codedeploy
        if codepipeline is not None:
            self._values["codepipeline"] = codepipeline
        if codestarconnections is not None:
            self._values["codestarconnections"] = codestarconnections
        if cognitoidentity is not None:
            self._values["cognitoidentity"] = cognitoidentity
        if cognitoidp is not None:
            self._values["cognitoidp"] = cognitoidp
        if configservice is not None:
            self._values["configservice"] = configservice
        if connect is not None:
            self._values["connect"] = connect
        if cur is not None:
            self._values["cur"] = cur
        if dataexchange is not None:
            self._values["dataexchange"] = dataexchange
        if datapipeline is not None:
            self._values["datapipeline"] = datapipeline
        if datasync is not None:
            self._values["datasync"] = datasync
        if dax is not None:
            self._values["dax"] = dax
        if detective is not None:
            self._values["detective"] = detective
        if devicefarm is not None:
            self._values["devicefarm"] = devicefarm
        if directconnect is not None:
            self._values["directconnect"] = directconnect
        if dlm is not None:
            self._values["dlm"] = dlm
        if dms is not None:
            self._values["dms"] = dms
        if docdb is not None:
            self._values["docdb"] = docdb
        if ds is not None:
            self._values["ds"] = ds
        if dynamodb is not None:
            self._values["dynamodb"] = dynamodb
        if ec2 is not None:
            self._values["ec2"] = ec2
        if ecr is not None:
            self._values["ecr"] = ecr
        if ecrpublic is not None:
            self._values["ecrpublic"] = ecrpublic
        if ecs is not None:
            self._values["ecs"] = ecs
        if efs is not None:
            self._values["efs"] = efs
        if eks is not None:
            self._values["eks"] = eks
        if elasticache is not None:
            self._values["elasticache"] = elasticache
        if elasticbeanstalk is not None:
            self._values["elasticbeanstalk"] = elasticbeanstalk
        if elastictranscoder is not None:
            self._values["elastictranscoder"] = elastictranscoder
        if elb is not None:
            self._values["elb"] = elb
        if emr is not None:
            self._values["emr"] = emr
        if emrcontainers is not None:
            self._values["emrcontainers"] = emrcontainers
        if es is not None:
            self._values["es"] = es
        if firehose is not None:
            self._values["firehose"] = firehose
        if fms is not None:
            self._values["fms"] = fms
        if forecast is not None:
            self._values["forecast"] = forecast
        if fsx is not None:
            self._values["fsx"] = fsx
        if gamelift is not None:
            self._values["gamelift"] = gamelift
        if glacier is not None:
            self._values["glacier"] = glacier
        if globalaccelerator is not None:
            self._values["globalaccelerator"] = globalaccelerator
        if glue is not None:
            self._values["glue"] = glue
        if greengrass is not None:
            self._values["greengrass"] = greengrass
        if guardduty is not None:
            self._values["guardduty"] = guardduty
        if iam is not None:
            self._values["iam"] = iam
        if identitystore is not None:
            self._values["identitystore"] = identitystore
        if imagebuilder is not None:
            self._values["imagebuilder"] = imagebuilder
        if inspector is not None:
            self._values["inspector"] = inspector
        if iot is not None:
            self._values["iot"] = iot
        if iotanalytics is not None:
            self._values["iotanalytics"] = iotanalytics
        if iotevents is not None:
            self._values["iotevents"] = iotevents
        if kafka is not None:
            self._values["kafka"] = kafka
        if kinesis is not None:
            self._values["kinesis"] = kinesis
        if kinesisanalytics is not None:
            self._values["kinesisanalytics"] = kinesisanalytics
        if kinesisanalyticsv2 is not None:
            self._values["kinesisanalyticsv2"] = kinesisanalyticsv2
        if kinesisvideo is not None:
            self._values["kinesisvideo"] = kinesisvideo
        if kms is not None:
            self._values["kms"] = kms
        if lakeformation is not None:
            self._values["lakeformation"] = lakeformation
        if lambda_ is not None:
            self._values["lambda_"] = lambda_
        if lexmodels is not None:
            self._values["lexmodels"] = lexmodels
        if licensemanager is not None:
            self._values["licensemanager"] = licensemanager
        if lightsail is not None:
            self._values["lightsail"] = lightsail
        if location is not None:
            self._values["location"] = location
        if macie is not None:
            self._values["macie"] = macie
        if macie2 is not None:
            self._values["macie2"] = macie2
        if managedblockchain is not None:
            self._values["managedblockchain"] = managedblockchain
        if marketplacecatalog is not None:
            self._values["marketplacecatalog"] = marketplacecatalog
        if mediaconnect is not None:
            self._values["mediaconnect"] = mediaconnect
        if mediaconvert is not None:
            self._values["mediaconvert"] = mediaconvert
        if medialive is not None:
            self._values["medialive"] = medialive
        if mediapackage is not None:
            self._values["mediapackage"] = mediapackage
        if mediastore is not None:
            self._values["mediastore"] = mediastore
        if mediastoredata is not None:
            self._values["mediastoredata"] = mediastoredata
        if memorydb is not None:
            self._values["memorydb"] = memorydb
        if mq is not None:
            self._values["mq"] = mq
        if mwaa is not None:
            self._values["mwaa"] = mwaa
        if neptune is not None:
            self._values["neptune"] = neptune
        if networkfirewall is not None:
            self._values["networkfirewall"] = networkfirewall
        if networkmanager is not None:
            self._values["networkmanager"] = networkmanager
        if opsworks is not None:
            self._values["opsworks"] = opsworks
        if organizations is not None:
            self._values["organizations"] = organizations
        if outposts is not None:
            self._values["outposts"] = outposts
        if personalize is not None:
            self._values["personalize"] = personalize
        if pinpoint is not None:
            self._values["pinpoint"] = pinpoint
        if pricing is not None:
            self._values["pricing"] = pricing
        if qldb is not None:
            self._values["qldb"] = qldb
        if quicksight is not None:
            self._values["quicksight"] = quicksight
        if ram is not None:
            self._values["ram"] = ram
        if rds is not None:
            self._values["rds"] = rds
        if redshift is not None:
            self._values["redshift"] = redshift
        if resourcegroups is not None:
            self._values["resourcegroups"] = resourcegroups
        if resourcegroupstaggingapi is not None:
            self._values["resourcegroupstaggingapi"] = resourcegroupstaggingapi
        if route53 is not None:
            self._values["route53"] = route53
        if route53_domains is not None:
            self._values["route53_domains"] = route53_domains
        if route53_recoverycontrolconfig is not None:
            self._values["route53_recoverycontrolconfig"] = route53_recoverycontrolconfig
        if route53_recoveryreadiness is not None:
            self._values["route53_recoveryreadiness"] = route53_recoveryreadiness
        if route53_resolver is not None:
            self._values["route53_resolver"] = route53_resolver
        if s3 is not None:
            self._values["s3"] = s3
        if s3_control is not None:
            self._values["s3_control"] = s3_control
        if s3_outposts is not None:
            self._values["s3_outposts"] = s3_outposts
        if sagemaker is not None:
            self._values["sagemaker"] = sagemaker
        if schemas is not None:
            self._values["schemas"] = schemas
        if sdb is not None:
            self._values["sdb"] = sdb
        if secretsmanager is not None:
            self._values["secretsmanager"] = secretsmanager
        if securityhub is not None:
            self._values["securityhub"] = securityhub
        if serverlessrepo is not None:
            self._values["serverlessrepo"] = serverlessrepo
        if servicecatalog is not None:
            self._values["servicecatalog"] = servicecatalog
        if servicediscovery is not None:
            self._values["servicediscovery"] = servicediscovery
        if servicequotas is not None:
            self._values["servicequotas"] = servicequotas
        if ses is not None:
            self._values["ses"] = ses
        if shield is not None:
            self._values["shield"] = shield
        if signer is not None:
            self._values["signer"] = signer
        if sns is not None:
            self._values["sns"] = sns
        if sqs is not None:
            self._values["sqs"] = sqs
        if ssm is not None:
            self._values["ssm"] = ssm
        if ssoadmin is not None:
            self._values["ssoadmin"] = ssoadmin
        if stepfunctions is not None:
            self._values["stepfunctions"] = stepfunctions
        if storagegateway is not None:
            self._values["storagegateway"] = storagegateway
        if sts is not None:
            self._values["sts"] = sts
        if swf is not None:
            self._values["swf"] = swf
        if synthetics is not None:
            self._values["synthetics"] = synthetics
        if timestreamwrite is not None:
            self._values["timestreamwrite"] = timestreamwrite
        if transfer is not None:
            self._values["transfer"] = transfer
        if waf is not None:
            self._values["waf"] = waf
        if wafregional is not None:
            self._values["wafregional"] = wafregional
        if wafv2 is not None:
            self._values["wafv2"] = wafv2
        if worklink is not None:
            self._values["worklink"] = worklink
        if workmail is not None:
            self._values["workmail"] = workmail
        if workspaces is not None:
            self._values["workspaces"] = workspaces
        if xray is not None:
            self._values["xray"] = xray

    @builtins.property
    def accessanalyzer(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#accessanalyzer AwsProvider#accessanalyzer}
        '''
        result = self._values.get("accessanalyzer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def acm(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#acm AwsProvider#acm}
        '''
        result = self._values.get("acm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def acmpca(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#acmpca AwsProvider#acmpca}
        '''
        result = self._values.get("acmpca")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def amplify(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#amplify AwsProvider#amplify}
        '''
        result = self._values.get("amplify")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def apigateway(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#apigateway AwsProvider#apigateway}
        '''
        result = self._values.get("apigateway")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def appconfig(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#appconfig AwsProvider#appconfig}
        '''
        result = self._values.get("appconfig")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def applicationautoscaling(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#applicationautoscaling AwsProvider#applicationautoscaling}
        '''
        result = self._values.get("applicationautoscaling")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def applicationinsights(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#applicationinsights AwsProvider#applicationinsights}
        '''
        result = self._values.get("applicationinsights")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def appmesh(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#appmesh AwsProvider#appmesh}
        '''
        result = self._values.get("appmesh")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def apprunner(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#apprunner AwsProvider#apprunner}
        '''
        result = self._values.get("apprunner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def appstream(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#appstream AwsProvider#appstream}
        '''
        result = self._values.get("appstream")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def appsync(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#appsync AwsProvider#appsync}
        '''
        result = self._values.get("appsync")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def athena(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#athena AwsProvider#athena}
        '''
        result = self._values.get("athena")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auditmanager(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#auditmanager AwsProvider#auditmanager}
        '''
        result = self._values.get("auditmanager")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def autoscaling(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#autoscaling AwsProvider#autoscaling}
        '''
        result = self._values.get("autoscaling")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def autoscalingplans(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#autoscalingplans AwsProvider#autoscalingplans}
        '''
        result = self._values.get("autoscalingplans")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#backup AwsProvider#backup}
        '''
        result = self._values.get("backup")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def batch(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#batch AwsProvider#batch}
        '''
        result = self._values.get("batch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def budgets(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#budgets AwsProvider#budgets}
        '''
        result = self._values.get("budgets")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def chime(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#chime AwsProvider#chime}
        '''
        result = self._values.get("chime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud9(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cloud9 AwsProvider#cloud9}
        '''
        result = self._values.get("cloud9")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudcontrolapi(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cloudcontrolapi AwsProvider#cloudcontrolapi}
        '''
        result = self._values.get("cloudcontrolapi")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudformation(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cloudformation AwsProvider#cloudformation}
        '''
        result = self._values.get("cloudformation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudfront(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cloudfront AwsProvider#cloudfront}
        '''
        result = self._values.get("cloudfront")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudhsm(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cloudhsm AwsProvider#cloudhsm}
        '''
        result = self._values.get("cloudhsm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudsearch(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cloudsearch AwsProvider#cloudsearch}
        '''
        result = self._values.get("cloudsearch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudtrail(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cloudtrail AwsProvider#cloudtrail}
        '''
        result = self._values.get("cloudtrail")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudwatch(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cloudwatch AwsProvider#cloudwatch}
        '''
        result = self._values.get("cloudwatch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudwatchevents(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cloudwatchevents AwsProvider#cloudwatchevents}
        '''
        result = self._values.get("cloudwatchevents")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudwatchlogs(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cloudwatchlogs AwsProvider#cloudwatchlogs}
        '''
        result = self._values.get("cloudwatchlogs")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def codeartifact(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#codeartifact AwsProvider#codeartifact}
        '''
        result = self._values.get("codeartifact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def codebuild(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#codebuild AwsProvider#codebuild}
        '''
        result = self._values.get("codebuild")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def codecommit(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#codecommit AwsProvider#codecommit}
        '''
        result = self._values.get("codecommit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def codedeploy(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#codedeploy AwsProvider#codedeploy}
        '''
        result = self._values.get("codedeploy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def codepipeline(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#codepipeline AwsProvider#codepipeline}
        '''
        result = self._values.get("codepipeline")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def codestarconnections(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#codestarconnections AwsProvider#codestarconnections}
        '''
        result = self._values.get("codestarconnections")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cognitoidentity(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cognitoidentity AwsProvider#cognitoidentity}
        '''
        result = self._values.get("cognitoidentity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cognitoidp(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cognitoidp AwsProvider#cognitoidp}
        '''
        result = self._values.get("cognitoidp")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configservice(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#configservice AwsProvider#configservice}
        '''
        result = self._values.get("configservice")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connect(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#connect AwsProvider#connect}
        '''
        result = self._values.get("connect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cur(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#cur AwsProvider#cur}
        '''
        result = self._values.get("cur")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dataexchange(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#dataexchange AwsProvider#dataexchange}
        '''
        result = self._values.get("dataexchange")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datapipeline(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#datapipeline AwsProvider#datapipeline}
        '''
        result = self._values.get("datapipeline")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datasync(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#datasync AwsProvider#datasync}
        '''
        result = self._values.get("datasync")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dax(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#dax AwsProvider#dax}
        '''
        result = self._values.get("dax")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def detective(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#detective AwsProvider#detective}
        '''
        result = self._values.get("detective")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def devicefarm(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#devicefarm AwsProvider#devicefarm}
        '''
        result = self._values.get("devicefarm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def directconnect(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#directconnect AwsProvider#directconnect}
        '''
        result = self._values.get("directconnect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dlm(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#dlm AwsProvider#dlm}
        '''
        result = self._values.get("dlm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dms(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#dms AwsProvider#dms}
        '''
        result = self._values.get("dms")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docdb(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#docdb AwsProvider#docdb}
        '''
        result = self._values.get("docdb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ds(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#ds AwsProvider#ds}
        '''
        result = self._values.get("ds")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dynamodb(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#dynamodb AwsProvider#dynamodb}
        '''
        result = self._values.get("dynamodb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ec2(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#ec2 AwsProvider#ec2}
        '''
        result = self._values.get("ec2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ecr(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#ecr AwsProvider#ecr}
        '''
        result = self._values.get("ecr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ecrpublic(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#ecrpublic AwsProvider#ecrpublic}
        '''
        result = self._values.get("ecrpublic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ecs(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#ecs AwsProvider#ecs}
        '''
        result = self._values.get("ecs")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def efs(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#efs AwsProvider#efs}
        '''
        result = self._values.get("efs")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eks(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#eks AwsProvider#eks}
        '''
        result = self._values.get("eks")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elasticache(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#elasticache AwsProvider#elasticache}
        '''
        result = self._values.get("elasticache")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elasticbeanstalk(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#elasticbeanstalk AwsProvider#elasticbeanstalk}
        '''
        result = self._values.get("elasticbeanstalk")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elastictranscoder(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#elastictranscoder AwsProvider#elastictranscoder}
        '''
        result = self._values.get("elastictranscoder")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elb(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#elb AwsProvider#elb}
        '''
        result = self._values.get("elb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def emr(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#emr AwsProvider#emr}
        '''
        result = self._values.get("emr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def emrcontainers(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#emrcontainers AwsProvider#emrcontainers}
        '''
        result = self._values.get("emrcontainers")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def es(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#es AwsProvider#es}
        '''
        result = self._values.get("es")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firehose(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#firehose AwsProvider#firehose}
        '''
        result = self._values.get("firehose")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fms(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#fms AwsProvider#fms}
        '''
        result = self._values.get("fms")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def forecast(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#forecast AwsProvider#forecast}
        '''
        result = self._values.get("forecast")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fsx(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#fsx AwsProvider#fsx}
        '''
        result = self._values.get("fsx")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gamelift(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#gamelift AwsProvider#gamelift}
        '''
        result = self._values.get("gamelift")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def glacier(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#glacier AwsProvider#glacier}
        '''
        result = self._values.get("glacier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def globalaccelerator(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#globalaccelerator AwsProvider#globalaccelerator}
        '''
        result = self._values.get("globalaccelerator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def glue(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#glue AwsProvider#glue}
        '''
        result = self._values.get("glue")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def greengrass(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#greengrass AwsProvider#greengrass}
        '''
        result = self._values.get("greengrass")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def guardduty(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#guardduty AwsProvider#guardduty}
        '''
        result = self._values.get("guardduty")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#iam AwsProvider#iam}
        '''
        result = self._values.get("iam")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identitystore(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#identitystore AwsProvider#identitystore}
        '''
        result = self._values.get("identitystore")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def imagebuilder(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#imagebuilder AwsProvider#imagebuilder}
        '''
        result = self._values.get("imagebuilder")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inspector(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#inspector AwsProvider#inspector}
        '''
        result = self._values.get("inspector")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iot(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#iot AwsProvider#iot}
        '''
        result = self._values.get("iot")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iotanalytics(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#iotanalytics AwsProvider#iotanalytics}
        '''
        result = self._values.get("iotanalytics")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iotevents(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#iotevents AwsProvider#iotevents}
        '''
        result = self._values.get("iotevents")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kafka(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#kafka AwsProvider#kafka}
        '''
        result = self._values.get("kafka")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kinesis(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#kinesis AwsProvider#kinesis}
        '''
        result = self._values.get("kinesis")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kinesisanalytics(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#kinesisanalytics AwsProvider#kinesisanalytics}
        '''
        result = self._values.get("kinesisanalytics")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kinesisanalyticsv2(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#kinesisanalyticsv2 AwsProvider#kinesisanalyticsv2}
        '''
        result = self._values.get("kinesisanalyticsv2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kinesisvideo(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#kinesisvideo AwsProvider#kinesisvideo}
        '''
        result = self._values.get("kinesisvideo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#kms AwsProvider#kms}
        '''
        result = self._values.get("kms")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lakeformation(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#lakeformation AwsProvider#lakeformation}
        '''
        result = self._values.get("lakeformation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lambda_(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#lambda AwsProvider#lambda}
        '''
        result = self._values.get("lambda_")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lexmodels(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#lexmodels AwsProvider#lexmodels}
        '''
        result = self._values.get("lexmodels")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def licensemanager(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#licensemanager AwsProvider#licensemanager}
        '''
        result = self._values.get("licensemanager")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lightsail(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#lightsail AwsProvider#lightsail}
        '''
        result = self._values.get("lightsail")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#location AwsProvider#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def macie(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#macie AwsProvider#macie}
        '''
        result = self._values.get("macie")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def macie2(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#macie2 AwsProvider#macie2}
        '''
        result = self._values.get("macie2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managedblockchain(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#managedblockchain AwsProvider#managedblockchain}
        '''
        result = self._values.get("managedblockchain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def marketplacecatalog(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#marketplacecatalog AwsProvider#marketplacecatalog}
        '''
        result = self._values.get("marketplacecatalog")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mediaconnect(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#mediaconnect AwsProvider#mediaconnect}
        '''
        result = self._values.get("mediaconnect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mediaconvert(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#mediaconvert AwsProvider#mediaconvert}
        '''
        result = self._values.get("mediaconvert")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def medialive(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#medialive AwsProvider#medialive}
        '''
        result = self._values.get("medialive")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mediapackage(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#mediapackage AwsProvider#mediapackage}
        '''
        result = self._values.get("mediapackage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mediastore(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#mediastore AwsProvider#mediastore}
        '''
        result = self._values.get("mediastore")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mediastoredata(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#mediastoredata AwsProvider#mediastoredata}
        '''
        result = self._values.get("mediastoredata")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memorydb(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#memorydb AwsProvider#memorydb}
        '''
        result = self._values.get("memorydb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mq(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#mq AwsProvider#mq}
        '''
        result = self._values.get("mq")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mwaa(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#mwaa AwsProvider#mwaa}
        '''
        result = self._values.get("mwaa")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def neptune(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#neptune AwsProvider#neptune}
        '''
        result = self._values.get("neptune")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def networkfirewall(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#networkfirewall AwsProvider#networkfirewall}
        '''
        result = self._values.get("networkfirewall")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def networkmanager(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#networkmanager AwsProvider#networkmanager}
        '''
        result = self._values.get("networkmanager")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def opsworks(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#opsworks AwsProvider#opsworks}
        '''
        result = self._values.get("opsworks")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organizations(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#organizations AwsProvider#organizations}
        '''
        result = self._values.get("organizations")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outposts(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#outposts AwsProvider#outposts}
        '''
        result = self._values.get("outposts")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def personalize(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#personalize AwsProvider#personalize}
        '''
        result = self._values.get("personalize")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pinpoint(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#pinpoint AwsProvider#pinpoint}
        '''
        result = self._values.get("pinpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pricing(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#pricing AwsProvider#pricing}
        '''
        result = self._values.get("pricing")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def qldb(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#qldb AwsProvider#qldb}
        '''
        result = self._values.get("qldb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quicksight(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#quicksight AwsProvider#quicksight}
        '''
        result = self._values.get("quicksight")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ram(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#ram AwsProvider#ram}
        '''
        result = self._values.get("ram")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rds(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#rds AwsProvider#rds}
        '''
        result = self._values.get("rds")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redshift(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#redshift AwsProvider#redshift}
        '''
        result = self._values.get("redshift")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resourcegroups(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#resourcegroups AwsProvider#resourcegroups}
        '''
        result = self._values.get("resourcegroups")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resourcegroupstaggingapi(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#resourcegroupstaggingapi AwsProvider#resourcegroupstaggingapi}
        '''
        result = self._values.get("resourcegroupstaggingapi")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route53(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#route53 AwsProvider#route53}
        '''
        result = self._values.get("route53")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route53_domains(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#route53domains AwsProvider#route53domains}
        '''
        result = self._values.get("route53_domains")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route53_recoverycontrolconfig(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#route53recoverycontrolconfig AwsProvider#route53recoverycontrolconfig}
        '''
        result = self._values.get("route53_recoverycontrolconfig")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route53_recoveryreadiness(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#route53recoveryreadiness AwsProvider#route53recoveryreadiness}
        '''
        result = self._values.get("route53_recoveryreadiness")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route53_resolver(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#route53resolver AwsProvider#route53resolver}
        '''
        result = self._values.get("route53_resolver")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#s3 AwsProvider#s3}
        '''
        result = self._values.get("s3")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_control(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#s3control AwsProvider#s3control}
        '''
        result = self._values.get("s3_control")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_outposts(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#s3outposts AwsProvider#s3outposts}
        '''
        result = self._values.get("s3_outposts")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#sagemaker AwsProvider#sagemaker}
        '''
        result = self._values.get("sagemaker")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schemas(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#schemas AwsProvider#schemas}
        '''
        result = self._values.get("schemas")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sdb(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#sdb AwsProvider#sdb}
        '''
        result = self._values.get("sdb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secretsmanager(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#secretsmanager AwsProvider#secretsmanager}
        '''
        result = self._values.get("secretsmanager")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def securityhub(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#securityhub AwsProvider#securityhub}
        '''
        result = self._values.get("securityhub")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serverlessrepo(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#serverlessrepo AwsProvider#serverlessrepo}
        '''
        result = self._values.get("serverlessrepo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def servicecatalog(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#servicecatalog AwsProvider#servicecatalog}
        '''
        result = self._values.get("servicecatalog")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def servicediscovery(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#servicediscovery AwsProvider#servicediscovery}
        '''
        result = self._values.get("servicediscovery")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def servicequotas(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#servicequotas AwsProvider#servicequotas}
        '''
        result = self._values.get("servicequotas")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ses(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#ses AwsProvider#ses}
        '''
        result = self._values.get("ses")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shield(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#shield AwsProvider#shield}
        '''
        result = self._values.get("shield")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signer(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#signer AwsProvider#signer}
        '''
        result = self._values.get("signer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sns(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#sns AwsProvider#sns}
        '''
        result = self._values.get("sns")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sqs(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#sqs AwsProvider#sqs}
        '''
        result = self._values.get("sqs")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssm(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#ssm AwsProvider#ssm}
        '''
        result = self._values.get("ssm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssoadmin(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#ssoadmin AwsProvider#ssoadmin}
        '''
        result = self._values.get("ssoadmin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stepfunctions(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#stepfunctions AwsProvider#stepfunctions}
        '''
        result = self._values.get("stepfunctions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storagegateway(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#storagegateway AwsProvider#storagegateway}
        '''
        result = self._values.get("storagegateway")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sts(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#sts AwsProvider#sts}
        '''
        result = self._values.get("sts")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def swf(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#swf AwsProvider#swf}
        '''
        result = self._values.get("swf")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def synthetics(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#synthetics AwsProvider#synthetics}
        '''
        result = self._values.get("synthetics")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestreamwrite(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#timestreamwrite AwsProvider#timestreamwrite}
        '''
        result = self._values.get("timestreamwrite")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transfer(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#transfer AwsProvider#transfer}
        '''
        result = self._values.get("transfer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def waf(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#waf AwsProvider#waf}
        '''
        result = self._values.get("waf")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wafregional(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#wafregional AwsProvider#wafregional}
        '''
        result = self._values.get("wafregional")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wafv2(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#wafv2 AwsProvider#wafv2}
        '''
        result = self._values.get("wafv2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def worklink(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#worklink AwsProvider#worklink}
        '''
        result = self._values.get("worklink")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workmail(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#workmail AwsProvider#workmail}
        '''
        result = self._values.get("workmail")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workspaces(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#workspaces AwsProvider#workspaces}
        '''
        result = self._values.get("workspaces")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def xray(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#xray AwsProvider#xray}
        '''
        result = self._values.get("xray")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsProviderEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.AwsProviderIgnoreTags",
    jsii_struct_bases=[],
    name_mapping={"key_prefixes": "keyPrefixes", "keys": "keys"},
)
class AwsProviderIgnoreTags:
    def __init__(
        self,
        *,
        key_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key_prefixes: Resource tag key prefixes to ignore across all resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#key_prefixes AwsProvider#key_prefixes}
        :param keys: Resource tag keys to ignore across all resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#keys AwsProvider#keys}
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if key_prefixes is not None:
            self._values["key_prefixes"] = key_prefixes
        if keys is not None:
            self._values["keys"] = keys

    @builtins.property
    def key_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Resource tag key prefixes to ignore across all resources.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#key_prefixes AwsProvider#key_prefixes}
        '''
        result = self._values.get("key_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Resource tag keys to ignore across all resources.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws#keys AwsProvider#keys}
        '''
        result = self._values.get("keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsProviderIgnoreTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AwsProviderIgnoreTagsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.AwsProviderIgnoreTagsOutputReference",
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

    @jsii.member(jsii_name="resetKeyPrefixes")
    def reset_key_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyPrefixes", []))

    @jsii.member(jsii_name="resetKeys")
    def reset_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeys", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="keyPrefixesInput")
    def key_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "keyPrefixesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="keysInput")
    def keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "keysInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="keyPrefixes")
    def key_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "keyPrefixes"))

    @key_prefixes.setter
    def key_prefixes(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "keyPrefixes", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="keys")
    def keys(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "keys"))

    @keys.setter
    def keys(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "keys", value)


class CloudcontrolapiResource(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.CloudcontrolapiResource",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html aws_cloudcontrolapi_resource}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        desired_state: builtins.str,
        type_name: builtins.str,
        role_arn: typing.Optional[builtins.str] = None,
        schema: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional["CloudcontrolapiResourceTimeouts"] = None,
        type_version_id: typing.Optional[builtins.str] = None,
        count: typing.Optional[typing.Union[jsii.Number, cdktf.IResolvable]] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html aws_cloudcontrolapi_resource} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param desired_state: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#desired_state CloudcontrolapiResource#desired_state}.
        :param type_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#type_name CloudcontrolapiResource#type_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#role_arn CloudcontrolapiResource#role_arn}.
        :param schema: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#schema CloudcontrolapiResource#schema}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#timeouts CloudcontrolapiResource#timeouts}
        :param type_version_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#type_version_id CloudcontrolapiResource#type_version_id}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = CloudcontrolapiResourceConfig(
            desired_state=desired_state,
            type_name=type_name,
            role_arn=role_arn,
            schema=schema,
            timeouts=timeouts,
            type_version_id=type_version_id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#create CloudcontrolapiResource#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#delete CloudcontrolapiResource#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#update CloudcontrolapiResource#update}.
        '''
        value = CloudcontrolapiResourceTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetRoleArn")
    def reset_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoleArn", []))

    @jsii.member(jsii_name="resetSchema")
    def reset_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchema", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTypeVersionId")
    def reset_type_version_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTypeVersionId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="properties")
    def properties(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "properties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CloudcontrolapiResourceTimeoutsOutputReference":
        return typing.cast("CloudcontrolapiResourceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="desiredStateInput")
    def desired_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "desiredStateInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(self) -> typing.Optional["CloudcontrolapiResourceTimeouts"]:
        return typing.cast(typing.Optional["CloudcontrolapiResourceTimeouts"], jsii.get(self, "timeoutsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="typeNameInput")
    def type_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeNameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="typeVersionIdInput")
    def type_version_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeVersionIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="desiredState")
    def desired_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "desiredState"))

    @desired_state.setter
    def desired_state(self, value: builtins.str) -> None:
        jsii.set(self, "desiredState", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="typeName")
    def type_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "typeName"))

    @type_name.setter
    def type_name(self, value: builtins.str) -> None:
        jsii.set(self, "typeName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "roleArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="schema")
    def schema(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "schema", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="typeVersionId")
    def type_version_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeVersionId"))

    @type_version_id.setter
    def type_version_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "typeVersionId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.CloudcontrolapiResourceConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "desired_state": "desiredState",
        "type_name": "typeName",
        "role_arn": "roleArn",
        "schema": "schema",
        "timeouts": "timeouts",
        "type_version_id": "typeVersionId",
    },
)
class CloudcontrolapiResourceConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[typing.Union[jsii.Number, cdktf.IResolvable]] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        desired_state: builtins.str,
        type_name: builtins.str,
        role_arn: typing.Optional[builtins.str] = None,
        schema: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional["CloudcontrolapiResourceTimeouts"] = None,
        type_version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param desired_state: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#desired_state CloudcontrolapiResource#desired_state}.
        :param type_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#type_name CloudcontrolapiResource#type_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#role_arn CloudcontrolapiResource#role_arn}.
        :param schema: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#schema CloudcontrolapiResource#schema}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#timeouts CloudcontrolapiResource#timeouts}
        :param type_version_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#type_version_id CloudcontrolapiResource#type_version_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = CloudcontrolapiResourceTimeouts(**timeouts)
        self._values: typing.Dict[str, typing.Any] = {
            "desired_state": desired_state,
            "type_name": type_name,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if schema is not None:
            self._values["schema"] = schema
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if type_version_id is not None:
            self._values["type_version_id"] = type_version_id

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
    def desired_state(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#desired_state CloudcontrolapiResource#desired_state}.'''
        result = self._values.get("desired_state")
        assert result is not None, "Required property 'desired_state' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#type_name CloudcontrolapiResource#type_name}.'''
        result = self._values.get("type_name")
        assert result is not None, "Required property 'type_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#role_arn CloudcontrolapiResource#role_arn}.'''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#schema CloudcontrolapiResource#schema}.'''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CloudcontrolapiResourceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#timeouts CloudcontrolapiResource#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CloudcontrolapiResourceTimeouts"], result)

    @builtins.property
    def type_version_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#type_version_id CloudcontrolapiResource#type_version_id}.'''
        result = self._values.get("type_version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudcontrolapiResourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.CloudcontrolapiResourceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class CloudcontrolapiResourceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#create CloudcontrolapiResource#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#delete CloudcontrolapiResource#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#update CloudcontrolapiResource#update}.
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#create CloudcontrolapiResource#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#delete CloudcontrolapiResource#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudcontrolapi_resource.html#update CloudcontrolapiResource#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudcontrolapiResourceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudcontrolapiResourceTimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.CloudcontrolapiResourceTimeoutsOutputReference",
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

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="create")
    def create(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "create"))

    @create.setter
    def create(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "create", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="delete")
    def delete(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "delete", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="update")
    def update(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "update"))

    @update.setter
    def update(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "update", value)


class DataAwsCloudcontrolapiResource(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.DataAwsCloudcontrolapiResource",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/d/cloudcontrolapi_resource.html aws_cloudcontrolapi_resource}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        identifier: builtins.str,
        type_name: builtins.str,
        role_arn: typing.Optional[builtins.str] = None,
        type_version_id: typing.Optional[builtins.str] = None,
        count: typing.Optional[typing.Union[jsii.Number, cdktf.IResolvable]] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/d/cloudcontrolapi_resource.html aws_cloudcontrolapi_resource} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param identifier: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/cloudcontrolapi_resource.html#identifier DataAwsCloudcontrolapiResource#identifier}.
        :param type_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/cloudcontrolapi_resource.html#type_name DataAwsCloudcontrolapiResource#type_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/cloudcontrolapi_resource.html#role_arn DataAwsCloudcontrolapiResource#role_arn}.
        :param type_version_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/cloudcontrolapi_resource.html#type_version_id DataAwsCloudcontrolapiResource#type_version_id}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataAwsCloudcontrolapiResourceConfig(
            identifier=identifier,
            type_name=type_name,
            role_arn=role_arn,
            type_version_id=type_version_id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetRoleArn")
    def reset_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoleArn", []))

    @jsii.member(jsii_name="resetTypeVersionId")
    def reset_type_version_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTypeVersionId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="properties")
    def properties(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "properties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="identifierInput")
    def identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identifierInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="typeNameInput")
    def type_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeNameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="typeVersionIdInput")
    def type_version_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeVersionIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identifier"))

    @identifier.setter
    def identifier(self, value: builtins.str) -> None:
        jsii.set(self, "identifier", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="typeName")
    def type_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "typeName"))

    @type_name.setter
    def type_name(self, value: builtins.str) -> None:
        jsii.set(self, "typeName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "roleArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="typeVersionId")
    def type_version_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeVersionId"))

    @type_version_id.setter
    def type_version_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "typeVersionId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.DataAwsCloudcontrolapiResourceConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "identifier": "identifier",
        "type_name": "typeName",
        "role_arn": "roleArn",
        "type_version_id": "typeVersionId",
    },
)
class DataAwsCloudcontrolapiResourceConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[typing.Union[jsii.Number, cdktf.IResolvable]] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        identifier: builtins.str,
        type_name: builtins.str,
        role_arn: typing.Optional[builtins.str] = None,
        type_version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param identifier: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/cloudcontrolapi_resource.html#identifier DataAwsCloudcontrolapiResource#identifier}.
        :param type_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/cloudcontrolapi_resource.html#type_name DataAwsCloudcontrolapiResource#type_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/cloudcontrolapi_resource.html#role_arn DataAwsCloudcontrolapiResource#role_arn}.
        :param type_version_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/cloudcontrolapi_resource.html#type_version_id DataAwsCloudcontrolapiResource#type_version_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "identifier": identifier,
            "type_name": type_name,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if type_version_id is not None:
            self._values["type_version_id"] = type_version_id

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
    def identifier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/cloudcontrolapi_resource.html#identifier DataAwsCloudcontrolapiResource#identifier}.'''
        result = self._values.get("identifier")
        assert result is not None, "Required property 'identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/cloudcontrolapi_resource.html#type_name DataAwsCloudcontrolapiResource#type_name}.'''
        result = self._values.get("type_name")
        assert result is not None, "Required property 'type_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/cloudcontrolapi_resource.html#role_arn DataAwsCloudcontrolapiResource#role_arn}.'''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type_version_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/cloudcontrolapi_resource.html#type_version_id DataAwsCloudcontrolapiResource#type_version_id}.'''
        result = self._values.get("type_version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsCloudcontrolapiResourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAwsDefaultTags(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.DataAwsDefaultTags",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/d/default_tags.html aws_default_tags}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        tags: typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, cdktf.IResolvable]] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/d/default_tags.html aws_default_tags} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/default_tags.html#tags DataAwsDefaultTags#tags}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataAwsDefaultTagsConfig(
            tags=tags,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tagsInput")
    def tags_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "tagsInput"))

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


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.DataAwsDefaultTagsConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "tags": "tags",
    },
)
class DataAwsDefaultTagsConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[typing.Union[jsii.Number, cdktf.IResolvable]] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        tags: typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/default_tags.html#tags DataAwsDefaultTags#tags}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if tags is not None:
            self._values["tags"] = tags

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
    def tags(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/default_tags.html#tags DataAwsDefaultTags#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsDefaultTagsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAwsIdentitystoreGroup(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.DataAwsIdentitystoreGroup",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/d/identitystore_group.html aws_identitystore_group}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        filter: typing.Sequence["DataAwsIdentitystoreGroupFilter"],
        identity_store_id: builtins.str,
        group_id: typing.Optional[builtins.str] = None,
        count: typing.Optional[typing.Union[jsii.Number, cdktf.IResolvable]] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/d/identitystore_group.html aws_identitystore_group} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param filter: filter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_group.html#filter DataAwsIdentitystoreGroup#filter}
        :param identity_store_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_group.html#identity_store_id DataAwsIdentitystoreGroup#identity_store_id}.
        :param group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_group.html#group_id DataAwsIdentitystoreGroup#group_id}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataAwsIdentitystoreGroupConfig(
            filter=filter,
            identity_store_id=identity_store_id,
            group_id=group_id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetGroupId")
    def reset_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[typing.List["DataAwsIdentitystoreGroupFilter"]]:
        return typing.cast(typing.Optional[typing.List["DataAwsIdentitystoreGroupFilter"]], jsii.get(self, "filterInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="groupIdInput")
    def group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="identityStoreIdInput")
    def identity_store_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityStoreIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="filter")
    def filter(self) -> typing.List["DataAwsIdentitystoreGroupFilter"]:
        return typing.cast(typing.List["DataAwsIdentitystoreGroupFilter"], jsii.get(self, "filter"))

    @filter.setter
    def filter(self, value: typing.List["DataAwsIdentitystoreGroupFilter"]) -> None:
        jsii.set(self, "filter", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="identityStoreId")
    def identity_store_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityStoreId"))

    @identity_store_id.setter
    def identity_store_id(self, value: builtins.str) -> None:
        jsii.set(self, "identityStoreId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "groupId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.DataAwsIdentitystoreGroupConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "filter": "filter",
        "identity_store_id": "identityStoreId",
        "group_id": "groupId",
    },
)
class DataAwsIdentitystoreGroupConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[typing.Union[jsii.Number, cdktf.IResolvable]] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        filter: typing.Sequence["DataAwsIdentitystoreGroupFilter"],
        identity_store_id: builtins.str,
        group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param filter: filter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_group.html#filter DataAwsIdentitystoreGroup#filter}
        :param identity_store_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_group.html#identity_store_id DataAwsIdentitystoreGroup#identity_store_id}.
        :param group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_group.html#group_id DataAwsIdentitystoreGroup#group_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "filter": filter,
            "identity_store_id": identity_store_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if group_id is not None:
            self._values["group_id"] = group_id

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
    def filter(self) -> typing.List["DataAwsIdentitystoreGroupFilter"]:
        '''filter block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_group.html#filter DataAwsIdentitystoreGroup#filter}
        '''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast(typing.List["DataAwsIdentitystoreGroupFilter"], result)

    @builtins.property
    def identity_store_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_group.html#identity_store_id DataAwsIdentitystoreGroup#identity_store_id}.'''
        result = self._values.get("identity_store_id")
        assert result is not None, "Required property 'identity_store_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_group.html#group_id DataAwsIdentitystoreGroup#group_id}.'''
        result = self._values.get("group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsIdentitystoreGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.DataAwsIdentitystoreGroupFilter",
    jsii_struct_bases=[],
    name_mapping={
        "attribute_path": "attributePath",
        "attribute_value": "attributeValue",
    },
)
class DataAwsIdentitystoreGroupFilter:
    def __init__(
        self,
        *,
        attribute_path: builtins.str,
        attribute_value: builtins.str,
    ) -> None:
        '''
        :param attribute_path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_group.html#attribute_path DataAwsIdentitystoreGroup#attribute_path}.
        :param attribute_value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_group.html#attribute_value DataAwsIdentitystoreGroup#attribute_value}.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "attribute_path": attribute_path,
            "attribute_value": attribute_value,
        }

    @builtins.property
    def attribute_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_group.html#attribute_path DataAwsIdentitystoreGroup#attribute_path}.'''
        result = self._values.get("attribute_path")
        assert result is not None, "Required property 'attribute_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attribute_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_group.html#attribute_value DataAwsIdentitystoreGroup#attribute_value}.'''
        result = self._values.get("attribute_value")
        assert result is not None, "Required property 'attribute_value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsIdentitystoreGroupFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAwsIdentitystoreUser(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.DataAwsIdentitystoreUser",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/d/identitystore_user.html aws_identitystore_user}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        filter: typing.Sequence["DataAwsIdentitystoreUserFilter"],
        identity_store_id: builtins.str,
        user_id: typing.Optional[builtins.str] = None,
        count: typing.Optional[typing.Union[jsii.Number, cdktf.IResolvable]] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/d/identitystore_user.html aws_identitystore_user} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param filter: filter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_user.html#filter DataAwsIdentitystoreUser#filter}
        :param identity_store_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_user.html#identity_store_id DataAwsIdentitystoreUser#identity_store_id}.
        :param user_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_user.html#user_id DataAwsIdentitystoreUser#user_id}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataAwsIdentitystoreUserConfig(
            filter=filter,
            identity_store_id=identity_store_id,
            user_id=user_id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetUserId")
    def reset_user_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[typing.List["DataAwsIdentitystoreUserFilter"]]:
        return typing.cast(typing.Optional[typing.List["DataAwsIdentitystoreUserFilter"]], jsii.get(self, "filterInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="identityStoreIdInput")
    def identity_store_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityStoreIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="userIdInput")
    def user_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="filter")
    def filter(self) -> typing.List["DataAwsIdentitystoreUserFilter"]:
        return typing.cast(typing.List["DataAwsIdentitystoreUserFilter"], jsii.get(self, "filter"))

    @filter.setter
    def filter(self, value: typing.List["DataAwsIdentitystoreUserFilter"]) -> None:
        jsii.set(self, "filter", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="identityStoreId")
    def identity_store_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityStoreId"))

    @identity_store_id.setter
    def identity_store_id(self, value: builtins.str) -> None:
        jsii.set(self, "identityStoreId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="userId")
    def user_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userId"))

    @user_id.setter
    def user_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "userId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.DataAwsIdentitystoreUserConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "filter": "filter",
        "identity_store_id": "identityStoreId",
        "user_id": "userId",
    },
)
class DataAwsIdentitystoreUserConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[typing.Union[jsii.Number, cdktf.IResolvable]] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        filter: typing.Sequence["DataAwsIdentitystoreUserFilter"],
        identity_store_id: builtins.str,
        user_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param filter: filter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_user.html#filter DataAwsIdentitystoreUser#filter}
        :param identity_store_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_user.html#identity_store_id DataAwsIdentitystoreUser#identity_store_id}.
        :param user_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_user.html#user_id DataAwsIdentitystoreUser#user_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "filter": filter,
            "identity_store_id": identity_store_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if user_id is not None:
            self._values["user_id"] = user_id

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
    def filter(self) -> typing.List["DataAwsIdentitystoreUserFilter"]:
        '''filter block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_user.html#filter DataAwsIdentitystoreUser#filter}
        '''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast(typing.List["DataAwsIdentitystoreUserFilter"], result)

    @builtins.property
    def identity_store_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_user.html#identity_store_id DataAwsIdentitystoreUser#identity_store_id}.'''
        result = self._values.get("identity_store_id")
        assert result is not None, "Required property 'identity_store_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_user.html#user_id DataAwsIdentitystoreUser#user_id}.'''
        result = self._values.get("user_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsIdentitystoreUserConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.DataAwsIdentitystoreUserFilter",
    jsii_struct_bases=[],
    name_mapping={
        "attribute_path": "attributePath",
        "attribute_value": "attributeValue",
    },
)
class DataAwsIdentitystoreUserFilter:
    def __init__(
        self,
        *,
        attribute_path: builtins.str,
        attribute_value: builtins.str,
    ) -> None:
        '''
        :param attribute_path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_user.html#attribute_path DataAwsIdentitystoreUser#attribute_path}.
        :param attribute_value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_user.html#attribute_value DataAwsIdentitystoreUser#attribute_value}.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "attribute_path": attribute_path,
            "attribute_value": attribute_value,
        }

    @builtins.property
    def attribute_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_user.html#attribute_path DataAwsIdentitystoreUser#attribute_path}.'''
        result = self._values.get("attribute_path")
        assert result is not None, "Required property 'attribute_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attribute_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/identitystore_user.html#attribute_value DataAwsIdentitystoreUser#attribute_value}.'''
        result = self._values.get("attribute_value")
        assert result is not None, "Required property 'attribute_value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsIdentitystoreUserFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AwsProvider",
    "AwsProviderAssumeRole",
    "AwsProviderAssumeRoleOutputReference",
    "AwsProviderConfig",
    "AwsProviderDefaultTags",
    "AwsProviderDefaultTagsOutputReference",
    "AwsProviderEndpoints",
    "AwsProviderIgnoreTags",
    "AwsProviderIgnoreTagsOutputReference",
    "CloudcontrolapiResource",
    "CloudcontrolapiResourceConfig",
    "CloudcontrolapiResourceTimeouts",
    "CloudcontrolapiResourceTimeoutsOutputReference",
    "DataAwsCloudcontrolapiResource",
    "DataAwsCloudcontrolapiResourceConfig",
    "DataAwsDefaultTags",
    "DataAwsDefaultTagsConfig",
    "DataAwsIdentitystoreGroup",
    "DataAwsIdentitystoreGroupConfig",
    "DataAwsIdentitystoreGroupFilter",
    "DataAwsIdentitystoreUser",
    "DataAwsIdentitystoreUserConfig",
    "DataAwsIdentitystoreUserFilter",
]

publication.publish()
