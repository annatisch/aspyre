#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   --------------------------------------------------------------------------------

import subprocess
import pytest
import os
import difflib
import random
import string
import pathlib
import functools
import re


SUPPRESS_WARNINGS = [
    "ASPIREDOCKERFILEBUILDER001",
    "ASPIREPROBES001",
    "ASPIREPROXYENDPOINTS001",
    "ASPIRECSHARPAPPS001",
]
DOTNET_ERRORS = re.compile(r"^(?P<file>.*)\((?P<line>\d+),(?P<column>\d+)\):\s+(?P<type>error|warning)\s+(?P<code>\w+):\s*(?P<message>.*)")

def _generate_suffix(length: int = 5, /) -> str:
    return "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length)).lower()


def _get_output_dir() -> pathlib.Path:
    test_dir = os.path.dirname(os.path.realpath(__file__))
    return pathlib.Path(test_dir) / "generated_outputs"


def _build_outputs(record_dir: pathlib.Path):
    apphost = record_dir / "apphost.cs"
    suppressions = ",".join(SUPPRESS_WARNINGS)
    args = ["dotnet", "build", apphost, f"/p:NoWarn={suppressions}"]
    output = subprocess.run(args, check=False, capture_output=True, text=True)
    if output.returncode != 0:
        errors = []
        for line in output.stdout.splitlines():
            match = DOTNET_ERRORS.match(line)
            if match:
                error_info = match.groupdict()
                test_file = "/".join(pathlib.Path(error_info["file"]).parts[-2:])
                errors.append(
                    f'{error_info["type"].title()}: {error_info["code"]}\nFile: {test_file}\nLine: {error_info["line"]}, Column: {error_info["column"]}\n{error_info["message"].strip()}')
        if errors:
            pytest.fail(f"Build failed for generated apphost.cs:\n\n{'\n\n'.join(errors)}\n")
        pytest.fail(f"Build failed for generated apphost.cs:\n\n{output.stdout}")


def _compare_outputs(ref_dir: pathlib.Path, test_dir: pathlib.Path):
    if ref_dir.exists() is False:
        pytest.fail(f"Recording directory does not exist: {ref_dir}. Please run test in recording mode first.")
    ref_files = set(os.listdir(ref_dir))
    if not ref_files:
        pytest.fail(f"Recording directory is empty: {ref_dir}. Please run test in recording mode first.")
    for _, _, files in os.walk(ref_dir):
        try:
            for filename in files:
                with open(ref_dir / filename, "r") as _ref:
                    ref_file = _ref.readlines()
                with open(test_dir / filename, "r") as _test:
                    test_file = _test.readlines()
                diff = difflib.unified_diff(
                    ref_file,
                    test_file,
                    fromfile=f"{ref_dir}/{filename}",
                    tofile=f"{test_dir}/{filename}",
                )
                changes = "".join(diff)
                has_changes = bool(changes)
                assert not has_changes, "\n" + changes
        finally:
            for filename in files:
                os.remove(test_dir / filename)
            os.rmdir(test_dir)


@pytest.fixture
def _compare_exports(request):
    output_dir = _get_output_dir()
    reference_dir = output_dir / request.node.name
    test_dir = output_dir / f"_{request.node.name}_{_generate_suffix()}"
    verify = functools.partial(_compare_outputs, reference_dir, test_dir)
    return test_dir, verify


@pytest.fixture
def _record_exports(request):
    output_dir = _get_output_dir()
    record_dir = output_dir / request.node.name
    verify = functools.partial(_build_outputs, record_dir)
    return record_dir, verify



verify_dotnet_apphost = _record_exports if os.environ.get("TEST_EXPORT_RECORD", "").lower() == "true" else _compare_exports
