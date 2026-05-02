from __future__ import annotations

from typing import Iterable

from ..models import Finding


class ValidationPipeline:
    def __init__(self, validators: Iterable[object]) -> None:
        self.validators = list(validators)

    def run(self, findings: Iterable[Finding]) -> list[Finding]:
        validated: list[Finding] = []
        for finding in findings:
            candidate = finding
            for validator in self.validators:
                candidate = validator.validate(candidate)
                if candidate is None:
                    break
            if candidate is not None:
                validated.append(candidate)
        return validated
