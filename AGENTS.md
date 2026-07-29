# Repository Rules

- Default tests must be deterministic and offline.
- Default tests must not require credentials or network access.
- Default tests must not modify tracked repository files.
- Generated reports and generated packaging metadata are not source files.
- Manual/network checks must be separated from the default pytest suite.
- A pytest test must assert outcomes and return None.
- Tests must fail rather than print a failure and return False.
- Test output must use pytest temporary directories or explicitly isolated ignored runtime directories.
- No strategy-semantic change may be hidden inside a packaging, warning, or test-cleanup task.
- Generated egg-info, dist-info, build, wheel, and distribution artifacts must not be committed.
- No dependency may be installed automatically by application code.
- Tests must not silently catch broad exceptions and report success.
- Warnings from project-owned source must not be ignored merely to make the suite green.
- The working tree must remain clean after the default test suite.
- Any change to default test count must be explicitly explained.
- MarketFlow remains research and decision-support software, not execution software.
