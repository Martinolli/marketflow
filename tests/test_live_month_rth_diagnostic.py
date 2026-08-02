from __future__ import annotations

import ast
import inspect
import json
import re
import stat
import subprocess
import sys
from dataclasses import FrozenInstanceError, replace
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

import pytest

from marketflow.historical_data import artifacts
from marketflow.historical_data import frozen_calendar
from marketflow.historical_data import live_month_rth_diagnostic as diag
from marketflow.historical_data import rth_bar_engine as rth
from marketflow.research import acquisition_contract_v2 as acv2
from marketflow.research import acquisition_contract_v2_1 as acv21
from marketflow.research import fixed_date_acquisition_contract as fdac


REPO_ROOT = Path(__file__).resolve().parents[1]
V1_DIGEST = "29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e"
V2_DIGEST = "59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0"
V21_DIGEST = "538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6"


@pytest.fixture()
def complete_source(tmp_path: Path):
    spec = diag._build_synthetic_smoke_source(tmp_path, complete=True)
    return tmp_path, spec


@pytest.fixture()
def partial_source(tmp_path: Path):
    spec = diag._build_synthetic_smoke_source(tmp_path, complete=False)
    return tmp_path, spec


def _write_receipt(root: Path, spec: diag.LiveMonthRthDiagnosticSpec, receipt: dict) -> diag.LiveMonthRthDiagnosticSpec:
    path = root / spec.source_smoke_run_id / "smoke_receipt" / "smoke-receipt.json"
    path.write_bytes(artifacts.canonical_json_bytes(receipt))
    return replace(spec, source_smoke_receipt_sha256=artifacts.sha256_file(path))


def _rewrite_monthly_payload(root: Path, manifest_ref: str, mutate) -> tuple[dict, dict]:
    manifest_path = artifacts._safe_ref_to_path(root, manifest_ref)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    payload_path = artifacts._safe_ref_to_path(root, str(manifest["payload_ref"]))
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    mutate(payload, manifest)
    payload_bytes = artifacts.canonical_json_bytes(payload)
    payload_path.write_bytes(payload_bytes)
    manifest["payload_sha256"] = artifacts.sha256_bytes(payload_bytes)
    manifest["payload_byte_size"] = len(payload_bytes)
    manifest["semantic_payload_digest"] = artifacts.semantic_digest(payload)
    manifest_path.write_bytes(artifacts.canonical_json_bytes(manifest))
    return manifest, payload


def _rewrite_monthly_manifest(root: Path, manifest_ref: str, mutate) -> dict:
    manifest_path = artifacts._safe_ref_to_path(root, manifest_ref)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    mutate(manifest)
    manifest_path.write_bytes(artifacts.canonical_json_bytes(manifest))
    return manifest


def _completeness_manifest_ref(root: Path, spec: diag.LiveMonthRthDiagnosticSpec) -> str:
    evidence = diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)
    return str(evidence.ohlcv_manifest["primary_parent_manifest_ref"])


def _completeness_manifest_and_payload(root: Path, manifest_ref: str) -> tuple[dict, dict]:
    manifest_path = artifacts._safe_ref_to_path(root, manifest_ref)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    payload_path = artifacts._safe_ref_to_path(root, str(manifest["payload_ref"]))
    return manifest, json.loads(payload_path.read_text(encoding="utf-8"))


def _symlink_or_skip(link: Path, target: Path, *, target_is_directory: bool = False) -> None:
    try:
        link.symlink_to(target, target_is_directory=target_is_directory)
    except (OSError, NotImplementedError) as exc:
        pytest.skip(f"symlink creation is unavailable on this host: {exc}")


def _normalized_ohlcv_manifest_ref(root: Path, spec: diag.LiveMonthRthDiagnosticSpec) -> str:
    evidence = diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)
    return str(evidence.smoke_receipt["normalized_artifact_receipts"][0]["manifest_ref"])


def _replace_manifest_payload_with_symlink(root: Path, manifest_ref: str, target: Path) -> Path:
    manifest_path = artifacts._safe_ref_to_path(root, manifest_ref)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    payload_path = artifacts._safe_ref_to_path(root, str(manifest["payload_ref"]))
    target.write_bytes(payload_path.read_bytes())
    payload_path.unlink()
    _symlink_or_skip(payload_path, target)
    return payload_path


def test_fixed_diagnostic_specification_and_digest():
    spec = diag.default_diagnostic_spec()
    digest = diag.diagnostic_spec_digest()

    assert digest == "d5bcaedb84148d9c69a18852a4d6e2b8984d16d6e8d25f3901426c10f3574257"
    assert spec.schema_version == "marketflow.live_month_rth_diagnostic.v1"
    assert spec.classification == "NONCANONICAL_LIVE_MONTH_RTH_DERIVATION"
    assert spec.source_smoke_run_id == "smoke-c3388f68530c4131a090a895953e3d89"
    assert spec.source_smoke_receipt_sha256 == "70b48e1c859d01cae7c0555f934fdaf3807863bbb1addffdc05b6f1c3197369f"
    assert spec.requested_primary_listing_mic == "XNAS"
    assert spec.requested_calendar_token == "XNAS"
    assert spec.calendar_authority == "NOT_OPERATOR_FROZEN"
    assert digest == diag._diagnostic_spec_digest_for_spec(diag.default_diagnostic_spec())
    assert len(digest) == 64


def test_no_caller_overrides_and_frozen_spec():
    spec = diag.default_diagnostic_spec()

    with pytest.raises(TypeError):
        diag.default_diagnostic_spec(source_ticker="MSFT")  # type: ignore[call-arg]
    with pytest.raises(FrozenInstanceError):
        spec.source_ticker = "MSFT"  # type: ignore[misc]
    with pytest.raises(TypeError):
        diag.diagnostic_spec_digest(spec)  # type: ignore[call-arg]
    with pytest.raises(TypeError):
        diag.build_calendar_candidate(spec)  # type: ignore[call-arg]
    with pytest.raises(TypeError):
        diag.validate_source_evidence(spec=spec, smoke_root=Path("elsewhere"))  # type: ignore[call-arg]
    with pytest.raises(TypeError):
        diag.run_diagnostic(spec=spec, smoke_root=Path("elsewhere"))  # type: ignore[call-arg]
    assert set(inspect.signature(diag.run_local_diagnostic).parameters) == {"confirmation"}
    for forbidden in (
        "candidate_factory",
        "uuid_factory",
        "source_smoke_root",
        "smoke_root",
        "run_root",
        "output_root",
        "artifact_root",
        "run_id",
        "run_id_factory",
        "repository_root",
        "ticker",
        "month",
        "MIC",
        "calendar",
    ):
        assert forbidden not in inspect.signature(diag.run_local_diagnostic).parameters
    confirmation = diag.diagnostic_confirmation_phrase()
    for kwargs in (
        {"source_smoke_root": Path("elsewhere")},
        {"smoke_root": Path("elsewhere")},
        {"candidate_factory": lambda: "rthdiag-caller"},
        {"uuid_factory": lambda: "rthdiag-caller"},
        {"run_root": Path("elsewhere")},
        {"output_root": Path("elsewhere")},
        {"artifact_root": Path("elsewhere")},
        {"run_id": "rthdiag-caller"},
        {"run_id_factory": lambda: "rthdiag-caller"},
        {"repository_root": Path("elsewhere")},
        {"ticker": "MSFT"},
        {"month": "2025-02"},
        {"MIC": "XNYS"},
        {"calendar": "XNYS"},
    ):
        with pytest.raises(TypeError):
            diag.run_local_diagnostic(confirmation, **kwargs)  # type: ignore[arg-type]
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.run(
            [sys.executable, "-m", "marketflow.historical_data", "--live-month-rth-derivation-plan", "--ticker", "MSFT"],
            cwd=REPO_ROOT,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )


def test_cli_package_and_source_runtime_boundary_are_sealed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    import marketflow.historical_data as historical_data

    help_result = subprocess.run(
        [sys.executable, "-m", "marketflow.historical_data", "--help"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    help_text = help_result.stdout + help_result.stderr
    for forbidden in (
        "--source-smoke-root",
        "--smoke-root",
        "--repository-root",
        "--run-root",
        "--output-root",
        "--artifact-root",
        "--run-id",
        "--run-id-factory",
    ):
        assert forbidden not in help_text

    assert "_run_local_diagnostic_core" not in historical_data.__all__
    assert "_production_source_smoke_root" not in historical_data.__all__
    assert "_generate_diagnostic_run_id" not in historical_data.__all__
    assert not hasattr(historical_data, "_run_local_diagnostic_core")

    expected_root = (REPO_ROOT / ".marketflow" / "rth_derivation_smoke" / "runs").resolve(strict=False)
    expected_source_root = (REPO_ROOT / ".marketflow" / "provider_smoke" / "runs").resolve(strict=False)
    assert diag._repository_root() == REPO_ROOT
    assert diag._production_runtime_root() == expected_root
    assert diag._production_source_smoke_root() == expected_source_root
    monkeypatch.chdir(tmp_path)
    assert diag._production_runtime_root() == expected_root
    assert diag._production_source_smoke_root() == expected_source_root
    ignored = subprocess.run(
        ["git", "check-ignore", ".marketflow/rth_derivation_smoke/runs"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert ignored.stdout.strip() == ".marketflow/rth_derivation_smoke/runs"

    module_source = (REPO_ROOT / "marketflow" / "historical_data" / "live_month_rth_diagnostic.py").read_text(encoding="utf-8")
    cli_source = (REPO_ROOT / "marketflow" / "historical_data" / "__main__.py").read_text(encoding="utf-8")
    assert 'DIAGNOSTIC_RUNTIME_ROOT = Path(".marketflow/rth_derivation_smoke/runs")' in module_source
    assert "smoke_root=_production_source_smoke_root()" in module_source
    assert "_run_diagnostic_for_spec(spec=default_diagnostic_spec(), smoke_root=SOURCE_SMOKE_ROOT)" not in module_source
    assert "_run_diagnostic_for_spec(spec=spec, smoke_root=SOURCE_SMOKE_ROOT)" not in module_source
    assert "MARKETFLOW_TEST_ROOT" not in module_source
    assert "getenv" not in module_source
    assert "environ" not in module_source
    assert "MAX_DIAGNOSTIC_RUN_ID_GENERATION_ATTEMPTS = 32" in module_source
    assert "DIAGNOSTIC_RUN_ID_GENERATION_EXHAUSTED" in module_source
    assert "while " not in module_source[module_source.index("def _generate_diagnostic_run_id") : module_source.index("def self_check")]
    assert "candidate_factory" not in cli_source
    assert "uuid_factory" not in cli_source
    assert "run_live_month_rth_derivation(confirmation)" in cli_source
    assert "_run_local_diagnostic_core" not in cli_source


def test_internal_run_id_is_opaque_and_path_safe():
    run_id = diag._generate_diagnostic_run_id()

    assert run_id.startswith("rthdiag-")
    assert re.fullmatch(r"rthdiag-[0-9a-f]{32}", run_id)
    assert diag._opaque_run_id(run_id) == run_id
    assert all(part not in run_id for part in ("/", "\\", "..", ":", "*", "?", "[", "]", "\x00"))
    rendered = run_id.upper()
    for forbidden in ("AAPL", "2025", "XNAS", "OPERATOR", str(REPO_ROOT).upper()):
        assert forbidden not in rendered


def test_generated_run_id_retries_forbidden_fragment_then_returns_safe_candidate():
    calls: list[str] = []
    candidates = iter(
        (
            "rthdiag-11111111111120251111111111111111",
            "rthdiag-11111111111111111111111111111111",
        )
    )

    def factory() -> str:
        candidate = next(candidates)
        calls.append(candidate)
        return candidate

    run_id = diag._generate_diagnostic_run_id(candidate_factory=factory)

    assert run_id == "rthdiag-11111111111111111111111111111111"
    assert calls == [
        "rthdiag-11111111111120251111111111111111",
        "rthdiag-11111111111111111111111111111111",
    ]


def test_generated_run_id_retries_multiple_unsafe_candidates_with_exact_bound():
    calls: list[str] = []
    unsafe = (
        "rthdiag-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaapl",
        "rthdiag-11111111111120251111111111111111",
        "rthdiag-2222222222222222222222222222xnas",
    )
    safe = "rthdiag-33333333333333333333333333333333"
    candidates = iter((*unsafe, safe))

    def factory() -> str:
        candidate = next(candidates)
        calls.append(candidate)
        return candidate

    assert diag._generate_diagnostic_run_id(candidate_factory=factory) == safe
    assert calls == [*unsafe, safe]


def test_generated_run_id_retries_structural_failure_then_returns_safe_candidate():
    calls: list[str] = []
    candidates = iter(
        (
            "rthdiag-not-a-hex-uuid",
            "rthdiag-44444444444444444444444444444444",
        )
    )

    def factory() -> str:
        candidate = next(candidates)
        calls.append(candidate)
        return candidate

    assert diag._generate_diagnostic_run_id(candidate_factory=factory) == "rthdiag-44444444444444444444444444444444"
    assert calls == ["rthdiag-not-a-hex-uuid", "rthdiag-44444444444444444444444444444444"]


def test_generated_run_id_safe_first_candidate_uses_one_factory_call():
    calls: list[str] = []

    def factory() -> str:
        calls.append("called")
        return "rthdiag-55555555555555555555555555555555"

    assert diag._generate_diagnostic_run_id(candidate_factory=factory) == "rthdiag-55555555555555555555555555555555"
    assert calls == ["called"]


def test_generated_run_id_exhaustion_is_fixed_and_writes_no_runtime_directory(tmp_path: Path):
    calls = 0
    run_root = tmp_path / "runtime"
    smoke_root = tmp_path / "missing-smoke"
    smoke_root.mkdir()

    def factory() -> str:
        nonlocal calls
        calls += 1
        return "rthdiag-11111111111120251111111111111111"

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match=diag.DIAGNOSTIC_RUN_ID_GENERATION_EXHAUSTED):
        diag._run_local_diagnostic_core(
            diag.diagnostic_confirmation_phrase(),
            smoke_root=smoke_root,
            run_root=run_root,
            run_id_factory=lambda: diag._generate_diagnostic_run_id(candidate_factory=factory),
        )

    assert calls == diag.MAX_DIAGNOSTIC_RUN_ID_GENERATION_ATTEMPTS
    assert not run_root.exists()


def test_generated_run_id_factory_failure_is_sanitized_without_runtime_output(tmp_path: Path):
    run_root = tmp_path / "runtime"
    smoke_root = tmp_path / "missing-smoke"
    smoke_root.mkdir()

    def factory() -> str:
        raise StopIteration("raw factory exhaustion")

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match=diag.DIAGNOSTIC_RUN_ID_GENERATION_EXHAUSTED):
        diag._run_local_diagnostic_core(
            diag.diagnostic_confirmation_phrase(),
            smoke_root=smoke_root,
            run_root=run_root,
            run_id_factory=lambda: diag._generate_diagnostic_run_id(candidate_factory=factory),
        )

    assert not run_root.exists()


def test_private_local_diagnostic_core_uses_tmp_root_and_collision_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    confirmation = diag.diagnostic_confirmation_phrase()
    smoke_root = tmp_path / "smoke"
    smoke_root.mkdir()
    monkeypatch.setattr(
        diag,
        "_run_diagnostic_for_spec",
        lambda **_kwargs: diag._blocked_receipt(diag.default_diagnostic_spec(), diag.LIVE_MONTH_RTH_DERIVATION_BLOCKED, ()),
    )
    receipt = diag._run_local_diagnostic_core(
        confirmation,
        smoke_root=smoke_root,
        run_root=tmp_path,
        run_id_factory=lambda: "rthdiag-private-core",
    )

    assert receipt["diagnostic_run_id"] == "rthdiag-private-core"
    assert receipt["source_smoke_receipt_sha256"] == diag.default_diagnostic_spec().source_smoke_receipt_sha256
    assert receipt["diagnostic_status"] in {
        diag.LIVE_MONTH_RTH_DERIVATION_COMPLETE,
        diag.LIVE_MONTH_RTH_DERIVATION_PARTIAL,
        diag.LIVE_MONTH_RTH_DERIVATION_BLOCKED,
        diag.LIVE_MONTH_SOURCE_EVIDENCE_INVALID,
    }
    assert (tmp_path / "rthdiag-private-core" / "live-month-rth-diagnostic-receipt.json").is_file()
    before = (tmp_path / "rthdiag-private-core" / "live-month-rth-diagnostic-receipt.json").read_bytes()

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match="already exists"):
        diag._run_local_diagnostic_core(
            confirmation,
            smoke_root=smoke_root,
            run_root=tmp_path,
            run_id_factory=lambda: "rthdiag-private-core",
        )
    assert (tmp_path / "rthdiag-private-core" / "live-month-rth-diagnostic-receipt.json").read_bytes() == before


def test_private_local_diagnostic_core_rejects_unsafe_root_and_run_ids(tmp_path: Path):
    confirmation = diag.diagnostic_confirmation_phrase()
    smoke_root = tmp_path / "smoke"
    diag._build_synthetic_smoke_source(smoke_root, complete=True)
    file_root = tmp_path / "not-a-directory"
    file_root.write_text("not a directory", encoding="utf-8")

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match="directory"):
        diag._run_local_diagnostic_core(
            confirmation,
            smoke_root=smoke_root,
            run_root=file_root,
            run_id_factory=lambda: "rthdiag-safe",
        )
    with pytest.raises(diag.LiveMonthRthDiagnosticError, match="runtime root"):
        diag._run_local_diagnostic_core(
            confirmation,
            smoke_root=smoke_root,
            run_root=tmp_path / "nested" / ".." / "escape",
            run_id_factory=lambda: "rthdiag-safe",
        )
    with pytest.raises(diag.LiveMonthRthDiagnosticError, match="source smoke root"):
        diag._run_local_diagnostic_core(
            confirmation,
            smoke_root=tmp_path / "nested" / ".." / "escape",
            run_root=tmp_path,
            run_id_factory=lambda: "rthdiag-safe",
        )
    for unsafe_run_id in ("../bad", "bad:name", "rthdiag-AAPL-2025-XNAS-operator"):
        with pytest.raises(diag.LiveMonthRthDiagnosticError, match="opaque"):
            diag._run_local_diagnostic_core(
                confirmation,
                smoke_root=smoke_root,
                run_root=tmp_path,
                run_id_factory=lambda value=unsafe_run_id: value,
            )


def test_public_source_evidence_and_plan_are_cwd_independent(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    expected_source_root = (REPO_ROOT / ".marketflow" / "provider_smoke" / "runs").resolve(strict=False)
    expected_runtime_root = (REPO_ROOT / ".marketflow" / "rth_derivation_smoke" / "runs").resolve(strict=False)
    plan_before = diag.plan_receipt()
    original_cwd = Path.cwd()

    try:
        monkeypatch.chdir(tmp_path)
        evidence = diag.validate_source_evidence()
        plan_after = diag.plan_receipt()

        assert Path.cwd() == tmp_path
        assert plan_after == plan_before
        assert diag._production_source_smoke_root() == expected_source_root
        assert diag._production_runtime_root() == expected_runtime_root
        assert evidence.spec.source_smoke_run_id == diag.default_diagnostic_spec().source_smoke_run_id
        assert evidence.spec.source_smoke_receipt_sha256 == diag.default_diagnostic_spec().source_smoke_receipt_sha256
        assert evidence.smoke_receipt["ticker"] == diag.default_diagnostic_spec().source_ticker
        assert len(evidence.ohlcv_payload["rows"]) == diag.default_diagnostic_spec().source_normalized_row_count
        assert not (tmp_path / ".marketflow").exists()
        assert diag.diagnostic_spec_digest() == "d5bcaedb84148d9c69a18852a4d6e2b8984d16d6e8d25f3901426c10f3574257"
    finally:
        monkeypatch.chdir(original_cwd)

    assert Path.cwd() == original_cwd


def test_shadow_cwd_marketflow_tree_is_not_read(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    shadow_receipt = (
        tmp_path
        / ".marketflow"
        / "provider_smoke"
        / "runs"
        / diag.default_diagnostic_spec().source_smoke_run_id
        / "smoke_receipt"
        / "smoke-receipt.json"
    )
    shadow_receipt.parent.mkdir(parents=True)
    shadow_receipt.write_text('{"smoke_status":"SHADOW_SHOULD_NOT_BE_READ"}', encoding="utf-8")

    monkeypatch.chdir(tmp_path)
    evidence = diag.validate_source_evidence()

    assert evidence.smoke_receipt["smoke_status"] == "SMOKE_COMPLETED_NONCANONICAL"
    assert shadow_receipt.read_text(encoding="utf-8") == '{"smoke_status":"SHADOW_SHOULD_NOT_BE_READ"}'
    assert not (tmp_path / ".marketflow" / "rth_derivation_smoke").exists()


def test_self_check_leaves_no_production_runtime_output():
    root = diag._production_runtime_root()
    before = {item.name for item in root.iterdir()} if root.exists() else set()

    receipt = diag.self_check()

    after = {item.name for item in root.iterdir()} if root.exists() else set()
    assert receipt["status"] == "LIVE_MONTH_RTH_DERIVATION_SELF_CHECK"
    assert after == before


def test_correct_smoke_receipt_hash_validation(complete_source):
    root, spec = complete_source

    evidence = diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)

    assert evidence.smoke_receipt["smoke_status"] == "SMOKE_COMPLETED_NONCANONICAL"
    assert evidence.ohlcv_manifest["artifact_id"] == spec.source_normalized_ohlcv_artifact_id
    assert evidence.audit_manifest["artifact_id"] == spec.source_normalized_audit_artifact_id
    assert evidence.completeness_payload["scope"] == "PROVIDER_RETRIEVAL_COMPLETE"


def test_wrong_smoke_hash_rejected(complete_source):
    root, spec = complete_source
    wrong = replace(spec, source_smoke_receipt_sha256="0" * 64)

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match="hash mismatch"):
        diag._validate_source_evidence_for_spec(spec=wrong, smoke_root=root)


def test_wrong_smoke_status_rejected(complete_source):
    root, spec = complete_source
    path = root / spec.source_smoke_run_id / "smoke_receipt" / "smoke-receipt.json"
    receipt = json.loads(path.read_text())
    receipt["smoke_status"] = "SMOKE_INVALID"
    updated = _write_receipt(root, spec, receipt)

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match="smoke_status"):
        diag._validate_source_evidence_for_spec(spec=updated, smoke_root=root)


def test_wrong_normalized_artifact_id_or_digest_rejected(complete_source):
    root, spec = complete_source

    with pytest.raises(diag.LiveMonthRthDiagnosticError):
        diag._validate_source_evidence_for_spec(spec=replace(spec, source_normalized_ohlcv_artifact_id="wrong-artifact"), smoke_root=root)
    with pytest.raises(diag.LiveMonthRthDiagnosticError):
        diag._validate_source_evidence_for_spec(spec=replace(spec, source_normalized_audit_semantic_digest="1" * 64), smoke_root=root)


def test_ohlcv_audit_row_count_mismatch_rejected(complete_source):
    root, spec = complete_source

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match="row count"):
        diag._validate_source_evidence_for_spec(spec=replace(spec, source_normalized_row_count=spec.source_normalized_row_count + 1), smoke_root=root)


def test_source_evidence_contained_regular_payload_is_accepted(complete_source):
    root, spec = complete_source

    evidence = diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)

    assert len(evidence.ohlcv_payload["rows"]) == spec.source_normalized_row_count
    assert evidence.ohlcv_manifest["payload_ref"]


def test_source_evidence_payload_symlink_to_outside_root_rejected_before_read(complete_source, tmp_path: Path):
    root, spec = complete_source
    manifest_ref = _normalized_ohlcv_manifest_ref(root, spec)
    payload_path = _replace_manifest_payload_with_symlink(root, manifest_ref, tmp_path / "outside-payload.json")

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match=diag.SOURCE_EVIDENCE_SYMLINK_REJECTED):
        diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)
    assert payload_path.is_symlink()


def test_source_evidence_payload_symlink_to_inside_root_rejected(complete_source):
    root, spec = complete_source
    manifest_ref = _normalized_ohlcv_manifest_ref(root, spec)
    inside_target = root / "inside-copy.json"
    payload_path = _replace_manifest_payload_with_symlink(root, manifest_ref, inside_target)

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match=diag.SOURCE_EVIDENCE_SYMLINK_REJECTED):
        diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)
    assert payload_path.resolve(strict=True).is_relative_to(root.resolve(strict=True))


def test_source_evidence_intermediate_directory_symlink_rejected(complete_source, tmp_path: Path):
    root, spec = complete_source
    manifest_ref = _normalized_ohlcv_manifest_ref(root, spec)
    target_dir = tmp_path / "target-dir"
    target_dir.mkdir()
    manifest_path = artifacts._safe_ref_to_path(root, manifest_ref)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    original_payload = artifacts._safe_ref_to_path(root, str(manifest["payload_ref"]))
    redirected_payload = target_dir / "payload.json"
    redirected_payload.write_bytes(original_payload.read_bytes())
    link_dir = root / "linked-payload-dir"
    _symlink_or_skip(link_dir, target_dir, target_is_directory=True)
    manifest["payload_ref"] = "linked-payload-dir/payload.json"
    manifest_path.write_bytes(artifacts.canonical_json_bytes(manifest))

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match=diag.SOURCE_EVIDENCE_SYMLINK_REJECTED):
        diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)


def test_source_evidence_reparse_metadata_rejected_without_real_junction():
    class ReparseMetadata:
        st_mode = stat.S_IFDIR
        st_file_attributes = diag.WINDOWS_REPARSE_POINT_ATTRIBUTE

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match=diag.SOURCE_EVIDENCE_REPARSE_POINT_REJECTED):
        diag._reject_source_reparse_metadata(ReparseMetadata())


def test_source_evidence_root_prefix_confusion_is_not_a_containment_check():
    source = (REPO_ROOT / "marketflow" / "historical_data" / "live_month_rth_diagnostic.py").read_text(encoding="utf-8")
    helper_source = source[source.index("def _validate_source_evidence_file") : source.index("def _reject_source_ref_schema")]

    assert ".startswith(" not in helper_source
    assert ".relative_to(" in helper_source


def test_source_evidence_payload_directory_rejected(complete_source):
    root, spec = complete_source
    manifest_ref = _normalized_ohlcv_manifest_ref(root, spec)
    manifest_path = artifacts._safe_ref_to_path(root, manifest_ref)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    payload_path = artifacts._safe_ref_to_path(root, str(manifest["payload_ref"]))
    payload_path.unlink()
    payload_path.mkdir()

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match=diag.SOURCE_EVIDENCE_NOT_REGULAR_FILE):
        diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)


def test_source_evidence_fake_nonregular_metadata_rejected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    payload = tmp_path / "payload.json"
    payload.write_text("{}", encoding="utf-8")
    source_file = diag.ValidatedSourceFile(path=payload, identity=(None, None, 2, 1))

    monkeypatch.setattr(
        diag,
        "_source_file_identity",
        lambda _path: (_ for _ in ()).throw(diag.LiveMonthRthDiagnosticError(diag.SOURCE_EVIDENCE_NOT_REGULAR_FILE)),
    )

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match=diag.SOURCE_EVIDENCE_NOT_REGULAR_FILE):
        diag._read_validated_source_file(source_file)


def test_source_evidence_source_root_symlink_rejected(tmp_path: Path):
    real_root = tmp_path / "real-source"
    spec = diag._build_synthetic_smoke_source(real_root, complete=True)
    link_root = tmp_path / "source-link"
    _symlink_or_skip(link_root, real_root, target_is_directory=True)

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match=diag.SOURCE_EVIDENCE_SYMLINK_REJECTED):
        diag._validate_source_evidence_for_spec(spec=spec, smoke_root=link_root)


def test_source_evidence_manifest_symlink_rejected(complete_source, tmp_path: Path):
    root, spec = complete_source
    manifest_ref = _normalized_ohlcv_manifest_ref(root, spec)
    manifest_path = artifacts._safe_ref_to_path(root, manifest_ref)
    outside_manifest = tmp_path / "outside-manifest.json"
    outside_manifest.write_bytes(manifest_path.read_bytes())
    manifest_path.unlink()
    _symlink_or_skip(manifest_path, outside_manifest)

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match=diag.SOURCE_EVIDENCE_SYMLINK_REJECTED):
        diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)


def test_raw_page_payload_symlink_rejected_without_reading_raw_body(complete_source, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    root, spec = complete_source
    manifest_ref = _completeness_manifest_ref(root, spec)
    completeness_manifest, _payload = _completeness_manifest_and_payload(root, manifest_ref)
    raw_ref = str(completeness_manifest["input_manifest_refs"][0])
    raw_manifest_path = artifacts._safe_ref_to_path(root, raw_ref)
    raw_manifest = json.loads(raw_manifest_path.read_text(encoding="utf-8"))
    raw_payload_path = artifacts._safe_ref_to_path(root, str(raw_manifest["payload_ref"]))
    outside_raw = tmp_path / "outside-raw.bin"
    outside_raw.write_bytes(raw_payload_path.read_bytes())
    raw_payload_path.unlink()
    _symlink_or_skip(raw_payload_path, outside_raw)

    read_bytes = Path.read_bytes

    def guarded_read_bytes(path: Path):
        if path == raw_payload_path:
            raise AssertionError("raw provider payload body was read")
        return read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", guarded_read_bytes)

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match=diag.SOURCE_EVIDENCE_SYMLINK_REJECTED):
        diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)


def test_source_evidence_file_identity_change_rejected(complete_source, monkeypatch: pytest.MonkeyPatch):
    root, spec = complete_source
    receipt_ref = diag._smoke_receipt_ref(spec.source_smoke_run_id)
    source_file = diag._validate_source_evidence_file(root, receipt_ref, expected_kind="smoke_receipt")
    original = diag._source_file_identity
    calls = 0

    def changed_identity(path: Path):
        nonlocal calls
        identity = original(path)
        if path == source_file.path:
            calls += 1
            if calls > 1:
                return (identity[0], identity[1], identity[2] + 1, identity[3])
        return identity

    monkeypatch.setattr(diag, "_source_file_identity", changed_identity)

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match=diag.SOURCE_EVIDENCE_FILE_IDENTITY_CHANGED):
        diag._read_validated_source_file(source_file)


def test_source_evidence_opened_file_identity_mismatch_rejected_before_read(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    payload = tmp_path / "payload.json"
    payload.write_text("{}", encoding="utf-8")
    source_file = diag._validate_source_evidence_file(tmp_path, "payload.json", expected_kind="json_payload")

    monkeypatch.setattr(
        diag,
        "_opened_source_file_identity",
        lambda _handle: (source_file.identity[0], source_file.identity[1], source_file.identity[2] + 1, source_file.identity[3]),
    )

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match=diag.SOURCE_EVIDENCE_FILE_IDENTITY_CHANGED):
        diag._read_validated_source_file(source_file)


def test_source_evidence_path_indirection_after_open_rejected_before_read(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    payload = tmp_path / "payload.json"
    payload.write_text("{}", encoding="utf-8")
    source_file = diag._validate_source_evidence_file(tmp_path, "payload.json", expected_kind="json_payload")
    original_open = Path.open
    original_reparse_check = diag._reject_source_reparse_components
    opened = False

    class GuardedHandle:
        def __init__(self, handle):
            self._handle = handle

        def __enter__(self):
            nonlocal opened
            opened = True
            return self

        def __exit__(self, exc_type, exc, traceback):
            self._handle.close()
            return False

        def fileno(self):
            return self._handle.fileno()

        def read(self):
            raise AssertionError("source payload was read after path indirection")

    def swapped_open(path: Path, *args, **kwargs):
        handle = original_open(path, *args, **kwargs)
        return GuardedHandle(handle)

    def post_open_indirection(path: Path) -> None:
        if path == source_file.path and opened:
            raise diag.LiveMonthRthDiagnosticError(diag.SOURCE_EVIDENCE_SYMLINK_REJECTED)
        original_reparse_check(path)

    monkeypatch.setattr(Path, "open", swapped_open)
    monkeypatch.setattr(diag, "_reject_source_reparse_components", post_open_indirection)

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match=diag.SOURCE_EVIDENCE_SYMLINK_REJECTED):
        diag._read_validated_source_file(source_file)


def test_source_evidence_disappearing_resolved_path_uses_fixed_category(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    payload = tmp_path / "payload.json"
    payload.write_text("{}", encoding="utf-8")
    original = diag._reject_source_reparse_components
    calls: dict[Path, int] = {}

    def disappearing_second_walk(path: Path) -> None:
        resolved = path.resolve(strict=False)
        calls[resolved] = calls.get(resolved, 0) + 1
        if resolved == payload.resolve(strict=True) and calls[resolved] == 2:
            raise FileNotFoundError(str(path))
        original(path)

    monkeypatch.setattr(diag, "_reject_source_reparse_components", disappearing_second_walk)

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match=diag.SOURCE_EVIDENCE_PATH_INVALID):
        diag._validate_source_evidence_file(tmp_path, "payload.json", expected_kind="json_payload")


def test_source_path_failure_occurs_before_import_calendar_or_rth(complete_source, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    root, spec = complete_source
    manifest_ref = _normalized_ohlcv_manifest_ref(root, spec)
    _replace_manifest_payload_with_symlink(root, manifest_ref, tmp_path / "outside-payload.json")
    calls: list[str] = []
    monkeypatch.setattr(diag, "import_source_bars", lambda _evidence: calls.append("import") or ())
    monkeypatch.setattr(diag, "_build_calendar_candidate_for_spec", lambda _spec: calls.append("calendar") or None)
    monkeypatch.setattr(diag.rth, "derive_profile_bars", lambda *_args, **_kwargs: calls.append("rth") or None)

    receipt = diag._run_diagnostic_for_spec(spec=spec, smoke_root=root)

    assert receipt["diagnostic_status"] == diag.LIVE_MONTH_SOURCE_EVIDENCE_INVALID
    assert receipt["fixed_session_findings"] == [{"finding": diag.SOURCE_EVIDENCE_SYMLINK_REJECTED}]
    assert calls == []


def test_source_path_failure_creates_no_local_run_artifact(complete_source, tmp_path: Path):
    smoke_root, spec = complete_source
    manifest_ref = _normalized_ohlcv_manifest_ref(smoke_root, spec)
    _replace_manifest_payload_with_symlink(smoke_root, manifest_ref, tmp_path / "outside-payload.json")
    run_root = tmp_path / "runs"

    receipt = diag._run_local_diagnostic_core(
        diag.diagnostic_confirmation_phrase(),
        smoke_root=smoke_root,
        run_root=run_root,
        run_id_factory=lambda: "rthdiag-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )

    assert receipt["diagnostic_status"] == diag.LIVE_MONTH_SOURCE_EVIDENCE_INVALID
    assert not run_root.exists()
    assert "swing_produced_bar_count" not in receipt


def test_source_path_failure_receipt_is_sanitized(complete_source, tmp_path: Path):
    root, spec = complete_source
    manifest_ref = _normalized_ohlcv_manifest_ref(root, spec)
    outside = tmp_path / "outside-payload.json"
    _replace_manifest_payload_with_symlink(root, manifest_ref, outside)

    receipt = diag._run_diagnostic_for_spec(spec=spec, smoke_root=root)
    serialized = json.dumps(receipt, sort_keys=True)

    assert str(outside) not in serialized
    assert str(root) not in serialized
    assert "outside-payload" not in serialized
    assert '"open"' not in serialized
    assert "Authorization" not in serialized


def test_timestamp_alignment_mismatch_rejected(complete_source):
    root, spec = complete_source
    evidence = diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)
    audit = dict(evidence.audit_payload)
    audit["rows"] = list(audit["rows"])
    audit["rows"][0] = dict(audit["rows"][0])
    audit["rows"][0]["window_start_utc"] = "2025-01-02T00:00:00Z"

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match="timestamp alignment"):
        diag._validate_normalized_pair(spec, evidence.ohlcv_payload, audit)


def test_raw_page_ancestry_count_mismatch_rejected(complete_source):
    root, spec = complete_source
    evidence = diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)
    manifest_ref = str(evidence.ohlcv_manifest["primary_parent_manifest_ref"])
    manifest_path = artifacts._safe_ref_to_path(root, manifest_ref)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["input_manifest_refs"] = []
    manifest_path.write_bytes(artifacts.canonical_json_bytes(manifest))

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match="raw-page ancestry count"):
        diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)


def test_raw_page_accepted_page_id_matches_manifest_id(complete_source):
    root, spec = complete_source
    manifest_ref = _completeness_manifest_ref(root, spec)
    completeness_manifest, completeness_payload = _completeness_manifest_and_payload(root, manifest_ref)
    raw_ref = str(completeness_manifest["input_manifest_refs"][0])
    raw_manifest_path = artifacts._safe_ref_to_path(root, raw_ref)
    raw_manifest = json.loads(raw_manifest_path.read_text(encoding="utf-8"))

    accepted = completeness_payload["accepted_pages"][0]

    assert accepted["raw_page_artifact_id"] == raw_manifest["artifact_id"]
    assert accepted["raw_page_sha256"] == raw_manifest["payload_sha256"]
    assert diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root).completeness_payload["page_count"] == 1


def test_raw_page_accepted_page_artifact_id_mismatch_rejected_before_derivation(complete_source):
    root, spec = complete_source
    manifest_ref = _completeness_manifest_ref(root, spec)

    _rewrite_monthly_payload(root, manifest_ref, lambda payload, _manifest: payload["accepted_pages"][0].update(raw_page_artifact_id="month-art-wrong-raw-page"))

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match="RAW_PAGE_ARTIFACT_ID_MISMATCH"):
        diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)
    receipt = diag._run_diagnostic_for_spec(spec=spec, smoke_root=root)
    assert receipt["diagnostic_status"] == diag.LIVE_MONTH_SOURCE_EVIDENCE_INVALID
    assert receipt["fixed_session_findings"] == [{"finding": "SOURCE_RAW_PAGE_ANCESTRY_INVALID"}]
    assert "swing_produced_bar_count" not in receipt


def test_raw_page_accepted_page_payload_sha_mismatch_rejected(complete_source):
    root, spec = complete_source
    manifest_ref = _completeness_manifest_ref(root, spec)

    _rewrite_monthly_payload(root, manifest_ref, lambda payload, _manifest: payload["accepted_pages"][0].update(raw_page_sha256="0" * 64))

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match="RAW_PAGE_PAYLOAD_DIGEST_MISMATCH"):
        diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)


def test_raw_page_missing_manifest_rejected(complete_source):
    root, spec = complete_source
    manifest_ref = _completeness_manifest_ref(root, spec)
    completeness_manifest, _payload = _completeness_manifest_and_payload(root, manifest_ref)
    raw_ref = str(completeness_manifest["input_manifest_refs"][0])
    artifacts._safe_ref_to_path(root, raw_ref).unlink()

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match="RAW_PAGE_MANIFEST_MISSING"):
        diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)


def test_raw_page_directory_neighbor_cannot_replace_declared_manifest(complete_source):
    root, spec = complete_source
    manifest_ref = _completeness_manifest_ref(root, spec)
    completeness_manifest, _payload = _completeness_manifest_and_payload(root, manifest_ref)
    raw_ref = str(completeness_manifest["input_manifest_refs"][0])
    raw_manifest_path = artifacts._safe_ref_to_path(root, raw_ref)
    neighbor_path = raw_manifest_path.with_name("month-art-neighbor-raw-provider-page.bin.manifest.json")
    neighbor_path.write_bytes(raw_manifest_path.read_bytes())
    _rewrite_monthly_manifest(root, raw_ref, lambda manifest: manifest.update(artifact_id="month-art-declared-tampered"))

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match="RAW_PAGE_INPUT_UNDECLARED"):
        diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)


def test_raw_page_accepted_page_count_mismatch_rejected(complete_source):
    root, spec = complete_source
    manifest_ref = _completeness_manifest_ref(root, spec)

    _rewrite_monthly_payload(root, manifest_ref, lambda payload, _manifest: payload.update(accepted_pages=[]))

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match="RAW_PAGE_ANCESTRY_COUNT_MISMATCH"):
        diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)


def test_raw_page_duplicate_accepted_artifact_id_rejected(complete_source):
    root, spec = complete_source
    manifest_ref = _completeness_manifest_ref(root, spec)
    completeness_manifest, _payload = _completeness_manifest_and_payload(root, manifest_ref)
    raw_ref = str(completeness_manifest["input_manifest_refs"][0])

    def duplicate(payload, manifest):
        payload["accepted_pages"] = [dict(payload["accepted_pages"][0]), dict(payload["accepted_pages"][0], page_ordinal=2)]
        payload["page_count"] = 2
        manifest["input_manifest_refs"] = [raw_ref, raw_ref]
        manifest["input_artifact_ids"] = [payload["accepted_pages"][0]["raw_page_artifact_id"]] * 2

    _rewrite_monthly_payload(root, manifest_ref, duplicate)
    completeness_manifest, completeness_payload = _completeness_manifest_and_payload(root, manifest_ref)

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match="RAW_PAGE_ANCESTRY_DUPLICATE"):
        diag._validate_monthly_parentage(root, completeness_manifest, completeness_payload, expected_raw_page_count=2)


def test_raw_page_accepted_page_order_mismatch_rejected(complete_source):
    root, spec = complete_source
    manifest_ref = _completeness_manifest_ref(root, spec)

    _rewrite_monthly_payload(root, manifest_ref, lambda payload, _manifest: payload["accepted_pages"][0].update(page_ordinal=2))

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match="RAW_PAGE_ANCESTRY_ORDER_MISMATCH"):
        diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)


def test_raw_page_cross_run_manifest_rejected(complete_source):
    root, spec = complete_source
    manifest_ref = _completeness_manifest_ref(root, spec)
    completeness_manifest, _payload = _completeness_manifest_and_payload(root, manifest_ref)
    raw_ref = str(completeness_manifest["input_manifest_refs"][0])
    _rewrite_monthly_manifest(root, raw_ref, lambda manifest: manifest.update(run_id="other-run"))

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match="RAW_PAGE_INPUT_UNDECLARED"):
        diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)
    receipt = diag._run_diagnostic_for_spec(spec=spec, smoke_root=root)
    assert receipt["diagnostic_status"] == diag.LIVE_MONTH_SOURCE_EVIDENCE_INVALID
    assert receipt["fixed_session_findings"] == [{"finding": "SOURCE_RAW_PAGE_ANCESTRY_INVALID"}]


def test_raw_page_cross_month_or_request_manifest_rejected(complete_source):
    root, spec = complete_source
    manifest_ref = _completeness_manifest_ref(root, spec)
    completeness_manifest, _payload = _completeness_manifest_and_payload(root, manifest_ref)
    raw_ref = str(completeness_manifest["input_manifest_refs"][0])
    _rewrite_monthly_manifest(root, raw_ref, lambda manifest: manifest.update(month_key="2025-02"))

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match="RAW_PAGE_INPUT_UNDECLARED"):
        diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)


def test_raw_page_ancestry_failure_writes_no_diagnostic_runtime_artifact(complete_source, tmp_path: Path):
    smoke_root, spec = complete_source
    manifest_ref = _completeness_manifest_ref(smoke_root, spec)
    _rewrite_monthly_payload(smoke_root, manifest_ref, lambda payload, _manifest: payload["accepted_pages"][0].update(raw_page_sha256="0" * 64))
    run_root = tmp_path / "runs"

    receipt = diag._run_diagnostic_for_spec(spec=spec, smoke_root=smoke_root)

    assert receipt["diagnostic_status"] == diag.LIVE_MONTH_SOURCE_EVIDENCE_INVALID
    assert not run_root.exists()
    assert "swing_produced_bar_count" not in receipt


def test_local_run_does_not_write_runtime_artifact_for_raw_page_ancestry_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    run_root = tmp_path / "runs"
    smoke_root = tmp_path / "smoke"
    smoke_root.mkdir()
    monkeypatch.setattr(
        diag,
        "_run_diagnostic_for_spec",
        lambda **_kwargs: {
            "diagnostic_status": diag.LIVE_MONTH_SOURCE_EVIDENCE_INVALID,
            "diagnostic_specification_digest": diag.diagnostic_spec_digest(),
            "fixed_session_findings": [{"finding": "SOURCE_RAW_PAGE_ANCESTRY_INVALID"}],
            "canonical_eligibility": False,
            "registry_eligibility": False,
            "strategy_enabled": False,
            "performance_enabled": False,
            "acquisition_enabled": False,
            "runtime_migration_enabled": False,
        },
    )

    receipt = diag._run_local_diagnostic_core(
        diag.diagnostic_confirmation_phrase(),
        smoke_root=smoke_root,
        run_root=run_root,
        run_id_factory=lambda: "rthdiag-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )

    assert receipt["fixed_session_findings"] == [{"finding": "SOURCE_RAW_PAGE_ANCESTRY_INVALID"}]
    assert not run_root.exists()


def test_raw_page_ancestry_source_uses_declared_inputs_before_derivation():
    source = (REPO_ROOT / "marketflow" / "historical_data" / "live_month_rth_diagnostic.py").read_text(encoding="utf-8")
    parentage_source = source[source.index("def _validate_monthly_parentage") : source.index("def _validate_monthly_manifest_metadata")]

    assert "accepted_pages = _required_list" in parentage_source
    assert "zip(accepted_pages, input_manifest_refs, input_artifact_ids, strict=True)" in parentage_source
    assert "RAW_PAGE_ARTIFACT_ID_MISMATCH" in parentage_source
    assert "RAW_PAGE_PAYLOAD_DIGEST_MISMATCH" in parentage_source
    assert ".rglob(" not in parentage_source
    assert ".glob(" not in parentage_source
    assert "iterdir(" not in parentage_source
    assert "latest" not in parentage_source.lower()
    assert "first" not in parentage_source.lower()
    assert source.index("_validate_monthly_parentage(root, completeness_manifest, completeness_payload") < source.index("source_bars = import_source_bars(evidence)")
    assert source.index("_validate_monthly_parentage(root, completeness_manifest, completeness_payload") < source.index("rth.derive_profile_bars")


def test_source_evidence_paths_use_authoritative_containment_helper_before_reads():
    source = (REPO_ROOT / "marketflow" / "historical_data" / "live_month_rth_diagnostic.py").read_text(encoding="utf-8")
    validation_source = source[source.index("def _validate_source_evidence_file") : source.index("def _reject_source_ref_schema")]
    monthly_source = source[source.index("def _load_monthly_payload") : source.index("def _validate_monthly_parentage")]
    parentage_source = source[source.index("def _validate_monthly_parentage") : source.index("def _validate_monthly_manifest_metadata")]

    assert "def _validate_source_evidence_file" in source
    assert "artifacts._safe_ref_to_path(root, str(manifest[\"payload_ref\"]))" not in source
    assert "payload_path.read_text" not in source
    assert "artifacts.sha256_file(payload_path)" not in source
    assert "payload_path.stat()" not in source
    assert "_validate_source_evidence_file(root, manifest_ref, expected_kind=\"manifest\")" in monthly_source
    assert "_validate_source_evidence_file(root, str(manifest[\"payload_ref\"]), expected_kind=\"json_payload\")" in monthly_source
    assert "_validate_source_evidence_file(root, str(input_ref), expected_kind=\"manifest\")" in parentage_source
    assert "_validate_source_evidence_file(root, str(raw_manifest[\"payload_ref\"]), expected_kind=\"raw_payload\")" in parentage_source
    assert ".startswith(" not in validation_source
    assert ".resolve(strict=True)" in validation_source
    assert ".relative_to(root)" in validation_source
    assert "stat.S_ISREG" in source
    assert "WINDOWS_REPARSE_POINT_ATTRIBUTE" in source
    assert source.index("_validate_source_evidence_for_spec(spec=actual, smoke_root=smoke_root)") < source.index("source_bars = import_source_bars(evidence)")
    assert source.index("_validate_source_evidence_for_spec(spec=actual, smoke_root=smoke_root)") < source.index("rth.derive_profile_bars")


def test_exact_decimal_source15minute_import(complete_source):
    root, spec = complete_source
    evidence = diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)
    bars = diag.import_source_bars(evidence)

    assert len(bars) == spec.source_normalized_row_count
    assert isinstance(bars[0].open, Decimal)
    assert bars[0].window_start_utc.tzinfo == UTC
    assert bars[0].window_end_utc - bars[0].window_start_utc == rth.SOURCE_INTERVAL


def test_no_source_row_sorting_or_repair(complete_source):
    root, spec = complete_source
    evidence = diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)
    payload = dict(evidence.ohlcv_payload)
    payload["rows"] = list(reversed(payload["rows"]))
    broken = replace(evidence, ohlcv_payload=payload)

    with pytest.raises(diag.LiveMonthRthDiagnosticError, match="strictly ascending"):
        diag.import_source_bars(broken)


def test_xnas_identity_retained_separately_from_resolved_calendar():
    calendar = diag.build_calendar_candidate()

    assert calendar.requested_primary_listing_mic == "XNAS"
    assert calendar.requested_calendar_token == "XNAS"
    assert calendar.resolved_calendar == "XNYS"


def test_package_alias_recorded_without_rewriting_mic():
    calendar = diag.build_calendar_candidate()

    assert calendar.calendar_alias_relationship == "XNAS_USES_XNYS_SCHEDULE"
    assert calendar.requested_primary_listing_mic == "XNAS"


def test_calendar_remains_pending_freeze():
    calendar = diag.build_calendar_candidate()

    assert calendar.status == frozen_calendar.CALENDAR_GENERATED_PENDING_OFFICIAL_EVIDENCE
    assert calendar.official_exchange_evidence_identity == diag.OPERATOR_DECLARED_DIAGNOSTIC_IDENTITY
    assert calendar.official_exchange_evidence_digest == "OFFICIAL_EVIDENCE_DIGEST_PENDING"


def test_january_session_view_is_deterministic():
    calendar = diag.build_calendar_candidate()
    first = diag.january_session_view(calendar)
    second = diag.january_session_view(calendar)

    assert first.month_view_digest == second.month_view_digest
    assert first.full_session_count > 0
    assert all(session.session_date.startswith("2025-01-") for session in first.calendar.sessions)


def test_full_ordinary_session_requires_exact_26_slots(complete_source):
    root, spec = complete_source
    evidence = diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)
    bars = diag.import_source_bars(evidence)
    view = diag.january_session_view(diag._build_calendar_candidate_for_spec(spec))
    session = next(item for item in view.calendar.sessions if item.session_classification == frozen_calendar.NORMAL_FULL_SESSION)
    by_date = diag._bars_by_local_date(view.calendar, bars)

    validation = rth.validate_session_sources(view.calendar, session, by_date[session.session_date])

    assert validation.outcome == rth.SESSION_COMPLETE
    assert len(validation.accepted_source_bars) == 26


def test_missing_first_middle_or_final_rth_slot_blocks_session(complete_source):
    root, spec = complete_source
    evidence = diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)
    bars = diag.import_source_bars(evidence)
    view = diag.january_session_view(diag._build_calendar_candidate_for_spec(spec))
    session = next(item for item in view.calendar.sessions if item.session_classification == frozen_calendar.NORMAL_FULL_SESSION)
    session_bars = list(diag._bars_by_local_date(view.calendar, bars)[session.session_date])

    for missing_index in (0, 12, 25):
        candidate = tuple(item for index, item in enumerate(session_bars) if index != missing_index)
        validation = rth.validate_session_sources(view.calendar, session, candidate)
        assert validation.outcome == rth.SESSION_SOURCE_INCOMPLETE


def test_duplicate_and_extra_rth_slot_block_session(complete_source):
    root, spec = complete_source
    evidence = diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)
    bars = diag.import_source_bars(evidence)
    view = diag.january_session_view(diag._build_calendar_candidate_for_spec(spec))
    session = next(item for item in view.calendar.sessions if item.session_classification == frozen_calendar.NORMAL_FULL_SESSION)
    session_bars = list(diag._bars_by_local_date(view.calendar, bars)[session.session_date])
    extra = rth.SourceBar(
        window_start_utc=datetime(2025, 1, 2, 16, 7, tzinfo=UTC),
        window_end_utc=datetime(2025, 1, 2, 16, 22, tzinfo=UTC),
        open=Decimal("1"),
        high=Decimal("1"),
        low=Decimal("1"),
        close=Decimal("1"),
        volume=Decimal("1"),
    )

    duplicate = rth.validate_session_sources(view.calendar, session, tuple(session_bars + [session_bars[0]]))
    extra_bars = tuple(sorted((*session_bars, extra), key=lambda item: item.window_start_utc))
    extra_result = rth.validate_session_sources(view.calendar, session, extra_bars)

    assert duplicate.outcome == rth.SESSION_SOURCE_INVALID
    assert extra_result.outcome == rth.SESSION_SOURCE_EXTRA_SLOT


def test_extended_hours_rows_are_excluded_not_used_as_replacements(complete_source):
    root, spec = complete_source
    evidence = diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)
    bars = diag.import_source_bars(evidence)
    view = diag.january_session_view(diag._build_calendar_candidate_for_spec(spec))
    session = next(item for item in view.calendar.sessions if item.session_classification == frozen_calendar.NORMAL_FULL_SESSION)
    session_bars = list(diag._bars_by_local_date(view.calendar, bars)[session.session_date])
    extended = rth.SourceBar.build(
        window_start_utc=datetime(2025, 1, 2, 9, 0, tzinfo=UTC),
        window_end_utc=datetime(2025, 1, 2, 9, 15, tzinfo=UTC),
        open="1",
        high="1",
        low="1",
        close="1",
        volume="1",
    )

    validation = rth.validate_session_sources(view.calendar, session, tuple([extended] + session_bars[1:]))

    assert validation.outcome == rth.SESSION_SOURCE_INCOMPLETE
    assert validation.extended_hours_exclusion_count == 1


def test_complete_receipt_reports_reconciled_rth_source_rows(complete_source):
    receipt = diag._run_diagnostic_for_spec(spec=complete_source[1], smoke_root=complete_source[0])

    assert receipt["expected_rth_source_row_count"] == 520
    assert receipt["validated_rth_source_row_count"] == 520
    assert receipt["rth_source_row_reconciliation_status"] == diag.RTH_SOURCE_ROWS_RECONCILED
    assert receipt["source_row_count"] - receipt["extended_hours_rows_excluded"] == receipt["validated_rth_source_row_count"]
    assert receipt["complete_ordinary_session_count"] * 26 == receipt["expected_rth_source_row_count"]


def test_accepted_source_receipt_reports_january_rth_row_reconciliation():
    receipt = diag.run_diagnostic()

    assert receipt["diagnostic_specification_digest"] == "d5bcaedb84148d9c69a18852a4d6e2b8984d16d6e8d25f3901426c10f3574257"
    assert receipt["diagnostic_status"] == diag.LIVE_MONTH_RTH_DERIVATION_COMPLETE
    assert receipt["source_row_count"] == 1277
    assert receipt["extended_hours_rows_excluded"] == 757
    assert receipt["expected_rth_source_row_count"] == 520
    assert receipt["validated_rth_source_row_count"] == 520
    assert receipt["rth_source_row_reconciliation_status"] == diag.RTH_SOURCE_ROWS_RECONCILED
    assert receipt["complete_ordinary_session_count"] == 20
    assert receipt["incomplete_ordinary_session_count"] == 0
    assert receipt["swing_produced_bar_count"] == 40
    assert receipt["position_swing_produced_bar_count"] == 20
    assert receipt["swing_dataset_semantic_digest"] == "48b97d83b737e2a591d2145e3b9a0395d08578cad57ec98f1b7f35d007bb72f0"
    assert receipt["position_swing_dataset_semantic_digest"] == "1f43aa14824892a13d45c6c124e78a997d8c4cd3e24933ba6c16922bc41324c7"
    assert receipt["canonical_eligibility"] is False
    assert receipt["registry_eligibility"] is False
    assert receipt["strategy_enabled"] is False
    assert receipt["performance_enabled"] is False


def test_missing_exact_rth_slot_reports_incomplete_validated_count(complete_source):
    root, spec = complete_source
    evidence = diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)
    bars = diag.import_source_bars(evidence)
    calendar = diag.january_session_view(diag._build_calendar_candidate_for_spec(spec)).calendar
    missing_one = tuple(bar for index, bar in enumerate(bars) if index != 0)

    summary = diag._session_validation_summary(calendar, missing_one)

    assert summary["expected_rth_source_row_count"] == 520
    assert summary["validated_rth_source_row_count"] == 519
    assert summary["rth_source_row_reconciliation_status"] == diag.RTH_SOURCE_ROWS_INCOMPLETE
    assert summary["incomplete_ordinary_session_count"] == 1


def test_extended_hours_rows_do_not_increase_validated_rth_count(complete_source):
    root, spec = complete_source
    evidence = diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)
    bars = diag.import_source_bars(evidence)
    calendar = diag.january_session_view(diag._build_calendar_candidate_for_spec(spec)).calendar
    extended = rth.SourceBar.build(
        window_start_utc=datetime(2025, 1, 2, 9, 0, tzinfo=UTC),
        window_end_utc=datetime(2025, 1, 2, 9, 15, tzinfo=UTC),
        open="1",
        high="1",
        low="1",
        close="1",
        volume="1",
    )

    summary = diag._session_validation_summary(calendar, tuple(sorted((*bars, extended), key=lambda item: item.window_start_utc)))

    assert summary["extended_hours_rows_excluded"] == 1
    assert summary["expected_rth_source_row_count"] == 520
    assert summary["validated_rth_source_row_count"] == 520
    assert summary["rth_source_row_reconciliation_status"] == diag.RTH_SOURCE_ROWS_RECONCILED


def test_duplicate_rth_slot_does_not_inflate_validated_rth_count(complete_source):
    root, spec = complete_source
    evidence = diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)
    bars = diag.import_source_bars(evidence)
    calendar = diag.january_session_view(diag._build_calendar_candidate_for_spec(spec)).calendar
    duplicate_bars = tuple(sorted((*bars, bars[0]), key=lambda item: item.window_start_utc))

    summary = diag._session_validation_summary(calendar, duplicate_bars)

    assert summary["expected_rth_source_row_count"] == 520
    assert summary["validated_rth_source_row_count"] == 520
    assert summary["rth_source_row_reconciliation_status"] == diag.RTH_SOURCE_ROWS_INVALID
    assert summary["incomplete_ordinary_session_count"] == 1


def test_extra_rth_slot_does_not_inflate_validated_rth_count(complete_source):
    root, spec = complete_source
    evidence = diag._validate_source_evidence_for_spec(spec=spec, smoke_root=root)
    bars = diag.import_source_bars(evidence)
    calendar = diag.january_session_view(diag._build_calendar_candidate_for_spec(spec)).calendar
    extra = rth.SourceBar(
        window_start_utc=datetime(2025, 1, 2, 16, 7, tzinfo=UTC),
        window_end_utc=datetime(2025, 1, 2, 16, 22, tzinfo=UTC),
        open=Decimal("1"),
        high=Decimal("1"),
        low=Decimal("1"),
        close=Decimal("1"),
        volume=Decimal("1"),
    )

    summary = diag._session_validation_summary(calendar, tuple(sorted((*bars, extra), key=lambda item: item.window_start_utc)))

    assert summary["expected_rth_source_row_count"] == 520
    assert summary["validated_rth_source_row_count"] == 520
    assert summary["rth_source_row_reconciliation_status"] == diag.RTH_SOURCE_ROWS_INVALID
    assert summary["incomplete_ordinary_session_count"] == 1


def test_early_close_session_excluded_entirely():
    calendar = diag.build_calendar_candidate()
    early = next(session for session in calendar.sessions if session.session_classification == frozen_calendar.EARLY_CLOSE_SESSION)

    validation = rth.validate_session_sources(calendar, early, ())

    assert validation.outcome == rth.EARLY_CLOSE_SESSION_EXCLUDED


def test_swing_half_session_derivation_counts(complete_source):
    receipt = diag._run_diagnostic_for_spec(spec=complete_source[1], smoke_root=complete_source[0])

    assert receipt["diagnostic_status"] == diag.LIVE_MONTH_RTH_DERIVATION_COMPLETE
    assert receipt["swing_produced_bar_count"] == receipt["january_full_session_count"] * 2


def test_position_swing_full_session_derivation_counts(complete_source):
    receipt = diag._run_diagnostic_for_spec(spec=complete_source[1], smoke_root=complete_source[0])

    assert receipt["position_swing_produced_bar_count"] == receipt["january_full_session_count"]


def test_profile_results_are_independent(complete_source):
    receipt = diag._run_diagnostic_for_spec(spec=complete_source[1], smoke_root=complete_source[0])

    assert receipt["swing_dataset_semantic_digest"] != receipt["position_swing_dataset_semantic_digest"]
    assert receipt["swing_produced_bar_count"] != receipt["position_swing_produced_bar_count"]


def test_complete_diagnostic_receipt_is_sanitized(complete_source):
    receipt = diag._run_diagnostic_for_spec(spec=complete_source[1], smoke_root=complete_source[0])
    rendered = json.dumps(receipt, sort_keys=True)

    assert receipt["diagnostic_status"] == diag.LIVE_MONTH_RTH_DERIVATION_COMPLETE
    assert receipt["expected_rth_source_row_count"] == 520
    assert receipt["validated_rth_source_row_count"] == 520
    assert receipt["rth_source_row_reconciliation_status"] == diag.RTH_SOURCE_ROWS_RECONCILED
    assert receipt["canonical_eligibility"] is False
    assert receipt["registry_eligibility"] is False
    assert receipt["strategy_enabled"] is False
    assert receipt["performance_enabled"] is False
    for forbidden in ('"open"', '"high"', '"low"', '"close"', '"volume"', "Authorization", "apiKey", "request_id"):
        assert forbidden not in rendered


def test_partial_diagnostic_receipt_lists_incomplete_session(partial_source):
    receipt = diag._run_diagnostic_for_spec(spec=partial_source[1], smoke_root=partial_source[0])

    assert receipt["diagnostic_status"] == diag.LIVE_MONTH_RTH_DERIVATION_PARTIAL
    assert receipt["expected_rth_source_row_count"] == 520
    assert receipt["validated_rth_source_row_count"] == 519
    assert receipt["rth_source_row_reconciliation_status"] == diag.RTH_SOURCE_ROWS_INCOMPLETE
    assert receipt["incomplete_ordinary_session_count"] == 1
    assert receipt["fixed_session_findings"][0]["finding"] == rth.SESSION_SOURCE_INCOMPLETE


def test_plan_command_is_offline_sanitized():
    result = subprocess.run(
        [sys.executable, "-m", "marketflow.historical_data", "--live-month-rth-derivation-plan"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    receipt = json.loads(result.stdout)

    assert receipt["status"] == diag.LIVE_MONTH_RTH_PLAN_VALID
    assert receipt["diagnostic_specification_digest"] == "d5bcaedb84148d9c69a18852a4d6e2b8984d16d6e8d25f3901426c10f3574257"
    assert receipt["diagnostic_specification_digest_prefix"] == "d5bcaedb8414"
    assert receipt["required_confirmation_phrase"] == diag.diagnostic_confirmation_phrase()
    assert receipt["network_execution_enabled"] is False
    assert receipt["credential_prompted"] is False
    assert receipt["runtime_artifact_written"] is False


def test_live_run_prints_plan_phrase_then_prompt_without_writing_on_wrong_phrase():
    root = diag._production_runtime_root()
    before = {item.name for item in root.iterdir()} if root.exists() else set()
    result = subprocess.run(
        [sys.executable, "-m", "marketflow.historical_data", "--live-month-rth-derivation-run"],
        cwd=REPO_ROOT,
        input="WRONG CONFIRMATION\n",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    after = {item.name for item in root.iterdir()} if root.exists() else set()
    stdout = result.stdout
    expected_phrase = diag.diagnostic_confirmation_phrase()
    digest = diag.diagnostic_spec_digest()
    prefix = digest[: diag.LOCAL_RUN_DIGEST_PREFIX_LENGTH]

    assert result.returncode == 2
    assert after == before
    assert stdout.index('"status": "LIVE_MONTH_RTH_PLAN_VALID"') < stdout.index("NONCANONICAL CLASSIFICATION:")
    assert stdout.index("NONCANONICAL CLASSIFICATION:") < stdout.index("Required operator confirmation phrase:")
    assert stdout.index(f"Required operator confirmation phrase: {expected_phrase}") < stdout.index("Type confirmation phrase:")
    assert f'"diagnostic_specification_digest": "{digest}"' in stdout
    assert f'"diagnostic_specification_digest_prefix": "{prefix}"' in stdout
    assert f"Diagnostic specification digest: {digest}" in stdout
    assert f"Diagnostic digest prefix: {prefix}" in stdout
    assert expected_phrase in stdout
    assert "DIAGNOSTIC_AUTHORIZATION_REJECTED" in stdout
    for forbidden in (str(root), "apiKey", "Authorization", '"open"', '"high"', '"low"', '"close"', '"volume"'):
        assert forbidden not in stdout


def test_live_run_displayed_phrase_matches_internal_acceptance(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]):
    from marketflow.historical_data import __main__ as historical_cli

    calls: list[str] = []
    monkeypatch.setattr("builtins.input", lambda prompt: calls.append(prompt) or diag.diagnostic_confirmation_phrase())
    monkeypatch.setattr(
        historical_cli,
        "run_live_month_rth_derivation",
        lambda confirmation: {
            "diagnostic_status": diag.LIVE_MONTH_RTH_DERIVATION_BLOCKED,
            "diagnostic_specification_digest": diag.diagnostic_spec_digest(),
            "confirmation_seen": confirmation,
        },
    )

    assert historical_cli.main(["--live-month-rth-derivation-run"]) == 0
    stdout = capsys.readouterr().out

    assert calls == ["Type confirmation phrase: "]
    assert f"Required operator confirmation phrase: {diag.diagnostic_confirmation_phrase()}" in stdout
    assert '"confirmation_seen": "RUN MARKETFLOW LIVE MONTH RTH d5bcaedb8414"' in stdout


def test_wrong_public_confirmation_does_not_resolve_runtime_root_or_execute(monkeypatch: pytest.MonkeyPatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("runtime path or diagnostic execution was reached before confirmation")

    monkeypatch.setattr(diag, "_production_runtime_root", fail_if_called)
    monkeypatch.setattr(diag, "_run_diagnostic_for_spec", fail_if_called)

    receipt = diag.run_local_diagnostic("WRONG CONFIRMATION")

    assert receipt["diagnostic_status"] == diag.LIVE_MONTH_RTH_DERIVATION_BLOCKED
    assert receipt["fixed_session_findings"] == [{"finding": "DIAGNOSTIC_AUTHORIZATION_REJECTED"}]


def test_self_check_command_uses_synthetic_temporary_artifacts():
    result = subprocess.run(
        [sys.executable, "-m", "marketflow.historical_data", "--live-month-rth-derivation-self-check"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    receipt = json.loads(result.stdout)

    assert receipt["status"] == "LIVE_MONTH_RTH_DERIVATION_SELF_CHECK"
    assert receipt["mock_source_only"] is True
    assert receipt["provider_execution_enabled"] is False
    assert receipt["complete_status"] == diag.LIVE_MONTH_RTH_DERIVATION_COMPLETE
    assert receipt["partial_status"] == diag.LIVE_MONTH_RTH_DERIVATION_PARTIAL


def test_no_socket_provider_key_or_credential_imports():
    source = (REPO_ROOT / "marketflow" / "historical_data" / "live_month_rth_diagnostic.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    forbidden = {"httpx", "requests", "socket", "urllib", "getpass"}
    imported = {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    imported_from = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}

    assert forbidden.isdisjoint(imported)
    assert forbidden.isdisjoint(imported_from)
    assert "ProviderApiKey" not in source
    assert "MassiveRestTransport" not in source
    assert "getenv" not in source
    assert "environ" not in source
    assert "raw_page_payload" not in source


def test_no_strategy_registry_or_runtime_migration_imports():
    source = (REPO_ROOT / "marketflow" / "historical_data" / "live_month_rth_diagnostic.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    forbidden = {
        "marketflow.marketflow_strategy",
        "marketflow.marketflow_wyckoff",
        "marketflow.services.monte_carlo_service",
        "marketflow.services.backtest_result_service",
        "marketflow.backtesting.outcome_engine",
        "marketflow.services.walk_forward_run_registry_service",
    }
    imported = {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    imported_from = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}

    assert forbidden.isdisjoint(imported)
    assert forbidden.isdisjoint(imported_from)
    assert "runtime_migration_enabled = True" not in source
    assert "canonical_eligibility = True" not in source
    assert "registry_eligibility = True" not in source


def test_contract_digests_remain_unchanged():
    assert fdac.contract_digest(fdac.load_contract_toml(REPO_ROOT / "config" / "fixed_date_acquisition_contract.example.toml")) == V1_DIGEST
    assert acv2.contract_digest(acv2.default_contract()) == V2_DIGEST
    assert acv21.contract_digest(acv21.default_contract()) == V21_DIGEST
