# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations


class VellumEnvironment:
    PRODUCTION: VellumEnvironment

    def __init__(self, *, default: str, documents: str, predict: str):
        self.default = default
        self.documents = documents
        self.predict = predict


VellumEnvironment.PRODUCTION = VellumEnvironment(
    default="https://api.vellum.ai", documents="https://documents.vellum.ai", predict="https://predict.vellum.ai"
)
