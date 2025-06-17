# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    deno_lint.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dfine <coding@dfine.tech>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/05/12 11:43:51 by dfine             #+#    #+#              #
#    Updated: 2025/05/12 11:43:54 by dfine            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import json
import subprocess
from pathlib import Path

from pydantic import BaseModel, HttpUrl

from tools import DENO_PATH
from tools.wrap_funcs import get_time_sync


class Position(BaseModel):
    line: int
    col: int
    bytePos: int


class Range(BaseModel):
    start: Position
    end: Position


class Diagnostic(BaseModel):
    filename: str
    range: Range
    message: str
    code: str
    hint: str | None


class LintError(BaseModel):
    file_path: str
    message: str


class DenoLintResult(BaseModel):
    version: int
    diagnostics: list[Diagnostic]
    errors: list[LintError]
    checked_files: list[str] | None


@get_time_sync
def lint(code_path: Path) -> tuple[DenoLintResult | None, Exception | None]:
    if not code_path.exists():
        return None, FileNotFoundError(f"File does not exist: {code_path}")
    if code_path.suffix not in [".ts", ".tsx"]:
        return None, ValueError(f"Unsupported file type: {code_path.suffix}")

    try:
        result = subprocess.run(
            [DENO_PATH, "lint", "--json", str(code_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        output = result.stdout.strip()
        if not output:
            return None, RuntimeError(
                f"Deno lint returned empty output.\nstderr: {result.stderr}"
            )

        data = DenoLintResult.model_validate(json.loads(output))

        return data, None
    except Exception as e:
        return None, e
