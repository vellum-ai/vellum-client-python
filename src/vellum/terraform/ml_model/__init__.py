'''
# `vellum_ml_model`

Refer to the Terraform Registry for docs: [`vellum_ml_model`](https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model).
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


class MlModel(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vellum-ai_vellum.mlModel.MlModel",
):
    '''Represents a {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model vellum_ml_model}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        developed_by: builtins.str,
        exec_config: typing.Union["MlModelExecConfig", typing.Dict[builtins.str, typing.Any]],
        family: builtins.str,
        hosted_by: builtins.str,
        name: builtins.str,
        visibility: builtins.str,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model vellum_ml_model} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param developed_by: The organization that developed the ML Model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#developed_by MlModel#developed_by}
        :param exec_config: The execution configuration of the ML Model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#exec_config MlModel#exec_config}
        :param family: The family of the ML Model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#family MlModel#family}
        :param hosted_by: The organization hosting the ML Model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#hosted_by MlModel#hosted_by}
        :param name: A name that uniquely identifies this ML Model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#name MlModel#name}
        :param visibility: The visibility of the ML Model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#visibility MlModel#visibility}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f5770609c9e007f726d44f32fd136172a03655c2380a9b3c83504aac134e29a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = MlModelConfig(
            developed_by=developed_by,
            exec_config=exec_config,
            family=family,
            hosted_by=hosted_by,
            name=name,
            visibility=visibility,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

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
        '''Generates CDKTF code for importing a MlModel resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MlModel to import.
        :param import_from_id: The id of the existing MlModel that should be imported. Refer to the {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MlModel to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0453f34be46be9f6e7945b1cc5ce547530fb25343e8d7f9db612883c0e78b32b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putExecConfig")
    def put_exec_config(
        self,
        *,
        base_url: builtins.str,
        features: typing.Sequence[builtins.str],
        metadata: typing.Mapping[builtins.str, builtins.str],
        model_identifier: builtins.str,
    ) -> None:
        '''
        :param base_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#base_url MlModel#base_url}.
        :param features: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#features MlModel#features}.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#metadata MlModel#metadata}.
        :param model_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#model_identifier MlModel#model_identifier}.
        '''
        value = MlModelExecConfig(
            base_url=base_url,
            features=features,
            metadata=metadata,
            model_identifier=model_identifier,
        )

        return typing.cast(None, jsii.invoke(self, "putExecConfig", [value]))

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
    @jsii.member(jsii_name="execConfig")
    def exec_config(self) -> "MlModelExecConfigOutputReference":
        return typing.cast("MlModelExecConfigOutputReference", jsii.get(self, "execConfig"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="developedByInput")
    def developed_by_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "developedByInput"))

    @builtins.property
    @jsii.member(jsii_name="execConfigInput")
    def exec_config_input(
        self,
    ) -> typing.Optional[typing.Union["MlModelExecConfig", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["MlModelExecConfig", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "execConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="familyInput")
    def family_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "familyInput"))

    @builtins.property
    @jsii.member(jsii_name="hostedByInput")
    def hosted_by_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostedByInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="visibilityInput")
    def visibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "visibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="developedBy")
    def developed_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "developedBy"))

    @developed_by.setter
    def developed_by(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ec43331bd7fafd8350c3f2d400f49584743d02a9695374d8511cf2455f1f0fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "developedBy", value)

    @builtins.property
    @jsii.member(jsii_name="family")
    def family(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "family"))

    @family.setter
    def family(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eccdb890011d8efe15b8530cd24861fe69440843204d16aac022bfa90e60729b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "family", value)

    @builtins.property
    @jsii.member(jsii_name="hostedBy")
    def hosted_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostedBy"))

    @hosted_by.setter
    def hosted_by(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b540ebcd83e978800a72855783a3e04fa7fa45932517a00556955f24a4ba0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostedBy", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2834794a1a16c331213fe75bccbbfa8b551d950d268e915929c914e9e2407932)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="visibility")
    def visibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visibility"))

    @visibility.setter
    def visibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f42a50ff9d8140ea1fd22013750ed23a41b97e1c9fe164e99a9b981775a5ae4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibility", value)


@jsii.data_type(
    jsii_type="vellum-ai_vellum.mlModel.MlModelConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "developed_by": "developedBy",
        "exec_config": "execConfig",
        "family": "family",
        "hosted_by": "hostedBy",
        "name": "name",
        "visibility": "visibility",
    },
)
class MlModelConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        developed_by: builtins.str,
        exec_config: typing.Union["MlModelExecConfig", typing.Dict[builtins.str, typing.Any]],
        family: builtins.str,
        hosted_by: builtins.str,
        name: builtins.str,
        visibility: builtins.str,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param developed_by: The organization that developed the ML Model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#developed_by MlModel#developed_by}
        :param exec_config: The execution configuration of the ML Model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#exec_config MlModel#exec_config}
        :param family: The family of the ML Model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#family MlModel#family}
        :param hosted_by: The organization hosting the ML Model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#hosted_by MlModel#hosted_by}
        :param name: A name that uniquely identifies this ML Model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#name MlModel#name}
        :param visibility: The visibility of the ML Model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#visibility MlModel#visibility}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(exec_config, dict):
            exec_config = MlModelExecConfig(**exec_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3d1b492e753e07ce481b7879b6f159fefc04adb9d9eeaa23bcff894fb0c09ef)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument developed_by", value=developed_by, expected_type=type_hints["developed_by"])
            check_type(argname="argument exec_config", value=exec_config, expected_type=type_hints["exec_config"])
            check_type(argname="argument family", value=family, expected_type=type_hints["family"])
            check_type(argname="argument hosted_by", value=hosted_by, expected_type=type_hints["hosted_by"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument visibility", value=visibility, expected_type=type_hints["visibility"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "developed_by": developed_by,
            "exec_config": exec_config,
            "family": family,
            "hosted_by": hosted_by,
            "name": name,
            "visibility": visibility,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def developed_by(self) -> builtins.str:
        '''The organization that developed the ML Model.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#developed_by MlModel#developed_by}
        '''
        result = self._values.get("developed_by")
        assert result is not None, "Required property 'developed_by' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exec_config(self) -> "MlModelExecConfig":
        '''The execution configuration of the ML Model.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#exec_config MlModel#exec_config}
        '''
        result = self._values.get("exec_config")
        assert result is not None, "Required property 'exec_config' is missing"
        return typing.cast("MlModelExecConfig", result)

    @builtins.property
    def family(self) -> builtins.str:
        '''The family of the ML Model.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#family MlModel#family}
        '''
        result = self._values.get("family")
        assert result is not None, "Required property 'family' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hosted_by(self) -> builtins.str:
        '''The organization hosting the ML Model.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#hosted_by MlModel#hosted_by}
        '''
        result = self._values.get("hosted_by")
        assert result is not None, "Required property 'hosted_by' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''A name that uniquely identifies this ML Model.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#name MlModel#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def visibility(self) -> builtins.str:
        '''The visibility of the ML Model.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#visibility MlModel#visibility}
        '''
        result = self._values.get("visibility")
        assert result is not None, "Required property 'visibility' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MlModelConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vellum-ai_vellum.mlModel.MlModelExecConfig",
    jsii_struct_bases=[],
    name_mapping={
        "base_url": "baseUrl",
        "features": "features",
        "metadata": "metadata",
        "model_identifier": "modelIdentifier",
    },
)
class MlModelExecConfig:
    def __init__(
        self,
        *,
        base_url: builtins.str,
        features: typing.Sequence[builtins.str],
        metadata: typing.Mapping[builtins.str, builtins.str],
        model_identifier: builtins.str,
    ) -> None:
        '''
        :param base_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#base_url MlModel#base_url}.
        :param features: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#features MlModel#features}.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#metadata MlModel#metadata}.
        :param model_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#model_identifier MlModel#model_identifier}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c784282f736cf32b66b9651cd4452753c77b4f6e1f99a8c68a9c8997badcc6ba)
            check_type(argname="argument base_url", value=base_url, expected_type=type_hints["base_url"])
            check_type(argname="argument features", value=features, expected_type=type_hints["features"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument model_identifier", value=model_identifier, expected_type=type_hints["model_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "base_url": base_url,
            "features": features,
            "metadata": metadata,
            "model_identifier": model_identifier,
        }

    @builtins.property
    def base_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#base_url MlModel#base_url}.'''
        result = self._values.get("base_url")
        assert result is not None, "Required property 'base_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def features(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#features MlModel#features}.'''
        result = self._values.get("features")
        assert result is not None, "Required property 'features' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#metadata MlModel#metadata}.'''
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def model_identifier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vellum-ai/vellum/0.0.7/docs/resources/ml_model#model_identifier MlModel#model_identifier}.'''
        result = self._values.get("model_identifier")
        assert result is not None, "Required property 'model_identifier' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MlModelExecConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MlModelExecConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vellum-ai_vellum.mlModel.MlModelExecConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43fc3316762ca85a1036e22132ce4a4260d687b34c9456a6c74c09b91f7e1ef2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="baseUrlInput")
    def base_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="featuresInput")
    def features_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "featuresInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="modelIdentifierInput")
    def model_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="baseUrl")
    def base_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseUrl"))

    @base_url.setter
    def base_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b7a9658f45325eed897dff1cd3db98b1f5957ba50eada8892db4e4d16cfd01f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseUrl", value)

    @builtins.property
    @jsii.member(jsii_name="features")
    def features(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "features"))

    @features.setter
    def features(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaf7c7e76489d0570cbd3740a2e2e806536d5f8472bec5dc00c8475aced34b3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "features", value)

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f93121b1a61e7dddefae33ede4fcb1795948f5405513c00a28d5e45b1080615c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value)

    @builtins.property
    @jsii.member(jsii_name="modelIdentifier")
    def model_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelIdentifier"))

    @model_identifier.setter
    def model_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b2bc1e2cd7f30694799c24996b86af3699ce8904c15341987885600203b285e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MlModelExecConfig, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MlModelExecConfig, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MlModelExecConfig, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c008a6bf93234ee88aa1473d90814128b94f61f4325e2b19c106d3cc4a389d66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "MlModel",
    "MlModelConfig",
    "MlModelExecConfig",
    "MlModelExecConfigOutputReference",
]

publication.publish()

def _typecheckingstub__7f5770609c9e007f726d44f32fd136172a03655c2380a9b3c83504aac134e29a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    developed_by: builtins.str,
    exec_config: typing.Union[MlModelExecConfig, typing.Dict[builtins.str, typing.Any]],
    family: builtins.str,
    hosted_by: builtins.str,
    name: builtins.str,
    visibility: builtins.str,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0453f34be46be9f6e7945b1cc5ce547530fb25343e8d7f9db612883c0e78b32b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ec43331bd7fafd8350c3f2d400f49584743d02a9695374d8511cf2455f1f0fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eccdb890011d8efe15b8530cd24861fe69440843204d16aac022bfa90e60729b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b540ebcd83e978800a72855783a3e04fa7fa45932517a00556955f24a4ba0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2834794a1a16c331213fe75bccbbfa8b551d950d268e915929c914e9e2407932(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f42a50ff9d8140ea1fd22013750ed23a41b97e1c9fe164e99a9b981775a5ae4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3d1b492e753e07ce481b7879b6f159fefc04adb9d9eeaa23bcff894fb0c09ef(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    developed_by: builtins.str,
    exec_config: typing.Union[MlModelExecConfig, typing.Dict[builtins.str, typing.Any]],
    family: builtins.str,
    hosted_by: builtins.str,
    name: builtins.str,
    visibility: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c784282f736cf32b66b9651cd4452753c77b4f6e1f99a8c68a9c8997badcc6ba(
    *,
    base_url: builtins.str,
    features: typing.Sequence[builtins.str],
    metadata: typing.Mapping[builtins.str, builtins.str],
    model_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43fc3316762ca85a1036e22132ce4a4260d687b34c9456a6c74c09b91f7e1ef2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b7a9658f45325eed897dff1cd3db98b1f5957ba50eada8892db4e4d16cfd01f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaf7c7e76489d0570cbd3740a2e2e806536d5f8472bec5dc00c8475aced34b3b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f93121b1a61e7dddefae33ede4fcb1795948f5405513c00a28d5e45b1080615c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b2bc1e2cd7f30694799c24996b86af3699ce8904c15341987885600203b285e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c008a6bf93234ee88aa1473d90814128b94f61f4325e2b19c106d3cc4a389d66(
    value: typing.Optional[typing.Union[MlModelExecConfig, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
