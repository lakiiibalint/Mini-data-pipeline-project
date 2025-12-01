"""Smoke tests for the pipeline module."""

from src.pipeline import run_pipeline


def test_run_pipeline_smoke():
    """A tiny smoke test that verifies the pipeline entrypoint is importable and runs."""
    assert run_pipeline() is True
