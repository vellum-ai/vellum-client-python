from typing import TYPE_CHECKING

from vellum.workflows.descriptors.base import BaseDescriptor
from vellum.workflows.types.core import VellumSecret

if TYPE_CHECKING:
    from vellum.workflows.state.base import BaseState


class VellumSecretReference(BaseDescriptor[VellumSecret]):
    def __init__(self, name: str):
        super().__init__(name=name, types=(VellumSecret,))

    def resolve(self, state: "BaseState") -> VellumSecret:
        return VellumSecret(name=self.name)
