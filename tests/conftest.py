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


SUPPRESS_WARNINGS = ["ASPIREDOCKERFILEBUILDER001"]


def _generate_suffix(length: int = 5, /) -> str:
    return "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length)).lower()


def _get_output_dir() -> pathlib.Path:
    test_dir = os.path.dirname(os.path.realpath(__file__))
    return pathlib.Path(test_dir) / "generated_outputs"


def _build_outputs(record_dir: pathlib.Path):
    apphost = record_dir / "apphost.cs"
    args = ["dotnet", "build", apphost]
    for suppress in SUPPRESS_WARNINGS:
        args.append(f"/p:NoWarn={suppress}")
    print("Building with dotnet to validate generated apphost.cs", args)
    output = subprocess.run(args, check=False, capture_output=True, text=True)
    if output.returncode != 0:
        print("Build failed:")
        print(output.stdout)
        print(output.stderr)
        pytest.fail(f"Build failed for generated apphost.cs in {apphost}")


def _compare_outputs(ref_dir: pathlib.Path, test_dir: pathlib.Path):
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
