"""Simple pipeline runner used for a smoke test and CLI entry point.

Keep heavy work out of import-time scope; use `run_pipeline` from tests.
"""

from __future__ import annotations

def run_pipeline() -> bool:
	"""Minimal pipeline function used by tests and CLI.

	Returns True to indicate the pipeline ran (smoke-test behavior).
	Replace with real orchestration logic as you expand the project.
	"""
	# placeholder for orchestration: scraping -> db -> processing -> reporting
	return True


def main() -> None:
	"""CLI entrypoint for running the pipeline manually."""
	ok = run_pipeline()
	if ok:
		print("Pipeline completed successfully.")
	else:
		print("Pipeline failed. Check logs for details.")


if __name__ == "__main__":
	main()

