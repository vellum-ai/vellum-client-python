from vellum.workflows.references import EnvironmentVariableReference


class Environment:
    @staticmethod
    def get(name: str) -> EnvironmentVariableReference:
        return EnvironmentVariableReference(name=name)
