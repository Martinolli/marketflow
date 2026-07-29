from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_IDENTITY_BASE_COMMIT = "f3c2ca8f841030c46657332371b155ad6bd81e68"
MANUAL_CHECKS = {
    "scripts/manual_checks/real_market_data_check.py",
    "scripts/manual_checks/data_provider_simple_check.py",
    "scripts/manual_checks/complete_integration_check.py",
    "scripts/manual_checks/enhanced_query_engine_check.py",
    "scripts/manual_checks/enhanced_rag_check.py",
    "scripts/manual_checks/candle_analyzer_real_data_check.py",
    "scripts/manual_checks/wyckoff_real_data_check.py",
    "scripts/manual_checks/marketflow_reports_check.py",
    "scripts/manual_checks/point_in_time_analyzer_real_data_check.py",
    "scripts/manual_checks/pattern_recognizer_real_data_check.py",
    "scripts/manual_checks/support_and_resistance_real_data_check.py",
    "scripts/manual_checks/trend_analyzer_real_data_check.py",
    "scripts/manual_checks/marketflow_facade_real_data_check.py",
    "scripts/manual_checks/multi_timeframe_analyzer_real_data_check.py",
}
PROTECTED_STRATEGY_FILES = {
    "marketflow/services/backtesting/outcome_engine.py",
    "marketflow/services/eigen_service.py",
    "marketflow/services/monte_carlo_service.py",
}
PROTECTED_STRATEGY_FORMULAS = {
    "_atr",
    "_rr",
    "_phase_score",
    "_event_score",
    "_pnf_score_neutral",
    "_derive_sl_tp_long",
    "_extract_context",
}
PROTECTED_WALK_FORWARD_SEMANTICS = {
    "_minimum_lookback_rows_from_profile",
    "_profile_horizon",
    "_row_matches_event_filters",
    "build_walk_forward_candidate_from_row",
    "evaluate_walk_forward_cases",
    "summarize_walk_forward_validation",
}


def _test_modules() -> list[Path]:
    return sorted(REPO_ROOT.joinpath("tests").glob("test*.py"))


class _DirectReturnVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.non_none_returns: list[int] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        return

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        return

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        return

    def visit_Return(self, node: ast.Return) -> None:
        if node.value is not None:
            self.non_none_returns.append(node.lineno)


def test_default_pytest_test_functions_do_not_return_values():
    offenders: list[str] = []
    for path in _test_modules():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test"):
                visitor = _DirectReturnVisitor()
                for statement in node.body:
                    visitor.visit(statement)
                for line in visitor.non_none_returns:
                    offenders.append(f"{path.relative_to(REPO_ROOT)}:{line}:{node.name}")

    assert offenders == []


def test_no_test_module_creates_repository_test_outputs_at_import_time():
    offenders: list[str] = []
    for path in _test_modules():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                rendered = ast.unparse(node)
                if "test_outputs" in rendered and ".mkdir(" in rendered:
                    offenders.append(f"{path.relative_to(REPO_ROOT)}:{node.lineno}")

    assert offenders == []


def test_default_tests_do_not_write_tracked_report_paths():
    tracked_result = subprocess.run(
        ["git", "ls-files", "test_outputs"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    tracked_report_paths = set(tracked_result.stdout.replace("\\", "/").splitlines())
    offenders: list[str] = []
    for path in _test_modules():
        if path.name == "test_source_assurance.py":
            continue
        source = path.read_text(encoding="utf-8")
        for tracked_path in tracked_report_paths:
            if tracked_path in source.replace("\\", "/") and ("write_text" in source or "open(" in source):
                offenders.append(f"{path.relative_to(REPO_ROOT)}:{tracked_path}")

    assert offenders == []


def test_manual_real_market_checks_are_not_collected_by_default_pytest():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    collected = result.stdout.replace("\\", "/")
    for manual_check in MANUAL_CHECKS:
        assert manual_check not in collected


def test_default_tests_do_not_instantiate_real_provider_without_mock_boundary():
    offenders: list[str] = []
    allowed_files = {
        "tests/test_data_provider.py",
        "tests/test_data_provider_async.py",
    }
    for path in _test_modules():
        relative = path.relative_to(REPO_ROOT).as_posix()
        if relative in allowed_files:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "PolygonIOProvider":
                offenders.append(f"{relative}:{node.lineno}")

    assert offenders == []


def test_packaging_metadata_directory_is_ignored_and_untracked():
    ignored = subprocess.run(
        ["git", "check-ignore", "marketflow.egg-info"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    tracked = subprocess.run(
        ["git", "ls-files", "marketflow.egg-info"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    assert ignored.stdout.strip() == "marketflow.egg-info"
    assert tracked.stdout.strip() == ""


def test_strategy_semantic_files_unchanged_in_this_task():
    result = subprocess.run(
        ["git", "diff", SOURCE_IDENTITY_BASE_COMMIT, "--name-only"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    changed = set(result.stdout.splitlines())

    assert changed.isdisjoint(PROTECTED_STRATEGY_FILES)


def _function_bodies(source: str) -> dict[str, str]:
    tree = ast.parse(source)
    bodies: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            bodies[node.name] = ast.unparse(node)
    return bodies


def test_marketflow_strategy_formulas_unchanged_outside_source_identity():
    base = subprocess.run(
        ["git", "show", f"{SOURCE_IDENTITY_BASE_COMMIT}:marketflow/marketflow_strategy.py"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    current_source = REPO_ROOT.joinpath("marketflow/marketflow_strategy.py").read_text(encoding="utf-8")
    base_bodies = _function_bodies(base.stdout)
    current_bodies = _function_bodies(current_source)

    for function_name in PROTECTED_STRATEGY_FORMULAS:
        assert current_bodies[function_name] == base_bodies[function_name]


def test_walk_forward_semantics_unchanged_outside_source_identity():
    base = subprocess.run(
        ["git", "show", f"{SOURCE_IDENTITY_BASE_COMMIT}:marketflow/services/walk_forward_validation_service.py"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    current_source = REPO_ROOT.joinpath("marketflow/services/walk_forward_validation_service.py").read_text(
        encoding="utf-8"
    )
    base_bodies = _function_bodies(base.stdout)
    current_bodies = _function_bodies(current_source)

    for function_name in PROTECTED_WALK_FORWARD_SEMANTICS:
        assert current_bodies[function_name] == base_bodies[function_name]


def test_strategy_source_identity_forbids_timeframe_only_and_first_file_fallbacks():
    source = REPO_ROOT.joinpath("marketflow/marketflow_strategy.py").read_text(encoding="utf-8")
    functions = _function_bodies(source)
    resolver = functions["resolve_strategy_source_identity"]
    ranker = functions["rank_long_candidates"]

    assert "timeframe_canonical" not in source
    assert "_csv_matches_timeframe_any_ticker(" not in resolver
    assert "_newest_csv(" not in resolver
    assert "falling back to annotated CSV matching timeframe only" not in source
    assert "source_identity.ticker" in ranker
    assert "source_identity.timeframe" in ranker
    assert "{'ticker': t" not in ranker


def test_strategy_candidate_reopen_paths_are_scoped_before_raw_path_acceptance():
    studio_source = REPO_ROOT.joinpath("apps/marketflow_studio.py").read_text(encoding="utf-8")
    studio_functions = _function_bodies(studio_source)
    candidate_csv_path = studio_functions["_candidate_csv_path"]
    trade_plan = studio_functions["_trade_plan_from_strategy_candidate"]
    diagnostics = studio_functions["_strategy_diagnostics_dataframe"]

    assert candidate_csv_path.index("source_report_dir = prefill.get('source_report_dir')") < candidate_csv_path.index("path.exists()")
    assert "return None" in candidate_csv_path
    assert "resolved.relative_to(report_root)" in candidate_csv_path
    assert "_candidate_csv_path(candidate) or candidate.get(\"csv\")" not in trade_plan
    assert "if not resolved_csv and candidate.get('source_report_dir'):" in trade_plan
    assert "matching_timeframe_csvs" not in diagnostics
    assert "'source_status': check.get('source_status')" in diagnostics

    backtest_source = REPO_ROOT.joinpath("marketflow/services/backtest_candidate_service.py").read_text(encoding="utf-8")
    backtest_functions = _function_bodies(backtest_source)
    candidate_source_path = backtest_functions["_candidate_source_path"]
    scoped_block_start = candidate_source_path.index("if source_report_dir:")
    raw_append_start = candidate_source_path.index("candidates.append(raw_path)")

    assert scoped_block_start < raw_append_start
    assert "relative_to(report_root.resolve(strict=True))" in candidate_source_path


def test_wyckoff_phase_annotation_uses_stable_dtype_without_semantic_changes():
    source = REPO_ROOT.joinpath("marketflow/marketflow_wyckoff.py").read_text(encoding="utf-8")

    assert 'phase_series = pd.Series({p[\'timestamp\']: p[\'phase_name\'] for p in self.phases}, dtype="string")' in source
    assert 'phase_series.reindex(annotated_df.index).ffill().fillna("UNKNOWN")' in source
