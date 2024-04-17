'''
# `provider`

Refer to the Terraform Registry for docs: [`vellum`](https://registry.terraform.io/providers/vellum-ai/vellum/0.0.2/docs).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class VellumProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="vellum-ai_vellum.provider.VellumProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.2/docs vellum}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        alias: typing.Optional[builtins.str] = None,
        api_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.2/docs vellum} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.2/docs#alias VellumProvider#alias}
        :param api_key: API Key to authenticate with the Vellum API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.2/docs#api_key VellumProvider#api_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f332a1b6664893e57a3554abbbfd334296d68a0c02222521351772fec263177)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = VellumProviderConfig(alias=alias, api_key=api_key)

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a VellumProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VellumProvider to import.
        :param import_from_id: The id of the existing VellumProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.2/docs#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VellumProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43f598a9f664a05d63c3b7644f2981a0397df03284b98ca077e6d7265f6aebcb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetApiKey")
    def reset_api_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiKey", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="apiKeyInput")
    def api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15a78e7b117167a258d082de10d77ec8038e1f5fcc5ff5ef0caadbce4dec2c02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value)

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__402b9018cf60ba05eb9ab72153d7f52235bd10a5f5615a074a53880068a8779b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value)


@jsii.data_type(
    jsii_type="vellum-ai_vellum.provider.VellumProviderConfig",
    jsii_struct_bases=[],
    name_mapping={"alias": "alias", "api_key": "apiKey"},
)
class VellumProviderConfig:
    def __init__(
        self,
        *,
        alias: typing.Optional[builtins.str] = None,
        api_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.2/docs#alias VellumProvider#alias}
        :param api_key: API Key to authenticate with the Vellum API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.2/docs#api_key VellumProvider#api_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb8c32f1d43f1344224f7a690abc6e2489c4dff67cb93921483ed2cc4b5410e1)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias
        if api_key is not None:
            self._values["api_key"] = api_key

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.2/docs#alias VellumProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_key(self) -> typing.Optional[builtins.str]:
        '''API Key to authenticate with the Vellum API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.2/docs#api_key VellumProvider#api_key}
        '''
        result = self._values.get("api_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VellumProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "VellumProvider",
    "VellumProviderConfig",
]

publication.publish()

def _typecheckingstub__8f332a1b6664893e57a3554abbbfd334296d68a0c02222521351772fec263177(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    alias: typing.Optional[builtins.str] = None,
    api_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43f598a9f664a05d63c3b7644f2981a0397df03284b98ca077e6d7265f6aebcb(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15a78e7b117167a258d082de10d77ec8038e1f5fcc5ff5ef0caadbce4dec2c02(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__402b9018cf60ba05eb9ab72153d7f52235bd10a5f5615a074a53880068a8779b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb8c32f1d43f1344224f7a690abc6e2489c4dff67cb93921483ed2cc4b5410e1(
    *,
    alias: typing.Optional[builtins.str] = None,
    api_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
