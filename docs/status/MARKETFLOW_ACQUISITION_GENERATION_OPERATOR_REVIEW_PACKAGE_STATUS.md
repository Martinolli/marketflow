# MarketFlow Acquisition Generation Operator Review Package Status

## Purpose
- Branch: `feature/acquisition-generation-operator-review-package-v1`
- Base commit: `8df3f6de8328f7251a59c30f31ee8b82d40b9979`
- Purpose: create an offline, digest-bound operator review package for the full 2022-2025 live acquisition generation candidate and targeted per-session triage evidence.
- This status document does not create an acquisition-generation freeze.

## Reviewed Acquisition Candidate
- Artifact kind: `ACQUISITION_GENERATION_CANDIDATE_REVIEW_PACKAGE`
- Review status: `ACQUISITION_GENERATION_CANDIDATE_REVIEW_PACKAGE_READY`
- Binding mode: `LIVE_ACQUISITION_AND_TRIAGE_STATUS_BINDING`
- Acquisition candidate digest: `5b1f7507c4549b0cd590737e37571cd0ff18f5710c5bfb853bd04aeec6b3f1cb`
- Acquisition candidate status: `ACQUISITION_GENERATION_READY_FOR_OPERATOR_REVIEW`

## Full Generation Summary
- Expected chunks: `48`
- Completed chunks: `48`
- Failed chunks: `0`
- Total raw rows: `63804`
- Total normalized source rows: `63804`
- Total RTH rows: `25970`
- Total extended-hours rows: `37834`
- Out-of-calendar/unknown rows: `0`

## 2025-01 Cross-Check
- Cross-check status: `PASSED`
- Normalized source rows: `1277`
- Validated RTH rows: `520`

## Monthly Reconciliation Summary
- Monthly reconciled count: `39`
- Monthly not-reconciled count: `9`

## Targeted Per-Session Triage
- Targeted diagnostic status: `READY_AFTER_TRIAGE`
- All monthly mismatches explained: `True`
- Mismatch explanation: `EXPLAINED_BY_SPECIAL_SESSION_EXPECTATION`
- Per-session issue summary: `{"RECONCILED":188}`
- Per-session severity summary: `{"INFO":188}`

## Frozen Authority Bindings
- Identity frozen digest: `57a698979e827d7c95737c12ad3435563486e44559a7f1ddd49c94006d27d24e`
- Calendar frozen digest: `25258b528e45a7f36d1cf96a4a40a8f2c89243c69d034f480dd10c4464d847a6`
- Schedule digest: `b0194dfed46ee06bd0954cc76f9e76d144d84c5e6f1a836acf2f486c083aeef0`
- Split-event audit frozen digest: `9bf3ff52f599757add22e01889c9ee3e72b4ff31e831ae312b94483b37f05fae`
- Dividend-event audit frozen digest: `0ef4e69954d67a5df8a246f623b2904651d579e5ebbe620a9647e16b42b95141`
- Acquisition contract digest: `538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6`

## Dividend Adjustment Implication
- In-range dividends found: `True`
- In-range dividend count: `16`
- Implication: `ACQUISITION_GENERATION_MUST_ACCOUNT_FOR_ADJUSTED_DATA_AND_DIVIDEND_POLICY`

## Checklist Summary
- Total checks: `52`
- Passed checks: `52`
- Failed checks: `0`
- Blocker count: `0`
- Ready for operator assessment: `True`
- Software freeze authorized: `False`

## Failed Checks
- None.

## Authority Boundary
- identity_segment_frozen: `True`
- calendar_operator_frozen: `True`
- split_event_audit_frozen: `True`
- dividend_event_audit_frozen: `True`
- acquisition_generation_freeze: `False`
- canonical_eligibility: `False`
- registry_eligibility: `False`
- strategy_runtime_migration: `False`
- automatic_stitching: `False`
- predictive_usefulness: `not accepted`
- profitability: `not accepted`

## Remaining Required Tasks
1. Digest-bound acquisition generation operator freeze ceremony.
2. SWING canonical dataset candidate.
3. SWING canonical dataset operator review/freeze.
4. SWING registry approval.
5. POSITION_SWING canonical dataset candidate.
6. POSITION_SWING canonical dataset operator review/freeze.
7. POSITION_SWING registry approval.
8. Normal runtime migration.
9. Applicability/research campaign.
10. Predictive and profitability evaluation.

## Guardrails
- Created offline: `True`
- Provider requests made in review: `False`
- API key stored: `False`
- No acquisition-generation freeze was created by this review package.
- No canonical, registry, runtime, predictive, or profitability approval occurred.

## Follow-On Acquisition Generation Freeze
- Freeze artifact: `ACQUISITION_GENERATION_FROZEN`
- Freeze status: `ACQUISITION_GENERATION_FROZEN`
- Status document: `docs/status/MARKETFLOW_ACQUISITION_GENERATION_OPERATOR_FREEZE_STATUS.md`
- The review package remains the source evidence for the freeze ceremony.
- Canonical eligibility, registry eligibility, and Strategy/runtime migration remain future work.

## Digests
- Chunk manifest digest: `8a4bf37f501fb7da5ea23e04d5ebe90da2cdfda1bf9e06e55e4c459be53fa374`
- Provider raw response digest: `aea820006bb458b9e51a1cda23ae24be02f476aafb36bec6c65d3740812d06c7`
- Normalized source rows digest: `0844164e1056732b0a887f19e569312cebab51e2e9c3db787415b4f56d533bdc`
- Monthly reconciliation digest: `d34effcf3129d630f14c61f5d0621aa0d89cdc51471f65f3d5effabeb42f16a4`
- Acquisition receipt digest: `63b1934fbaf4b146fadcfbb5cb4649e18b1e91d8d304cf3afdee71220d005eed`
- Targeted chunk manifest digest: `aac91eaa82859c88c29cfcef07c9f2f2f8da68d198a17572affc2cd3a0a9239c`
- Targeted provider raw response digest: `041c7da634d43463c8ce37a6b3da7aa1bf77c558f02aa18a2b820f290368dc1f`
- Targeted normalized rows digest: `b5a82e3d8266a55fa520a2c2a5c01d3bd15ccbe27db806cfa0e4b21225e07c28`
- Targeted monthly reconciliation digest: `f002b833511b102e8136d00354dbe6c410abd30a947242e881e44e12d3cc9191`
- Per-session diagnostics digest: `f810bfd3fcb1d2056bbf5ba0cff8b1aa4276119721c697ce17eaef6bab069faa`
- Targeted diagnostic receipt digest: `82ec97bbc5eba73a275cc8221bb4a59235ed093a6e6dbe14058eac26980d26c8`
- Review package digest: `70dcc5a06ed368399cf367e3c12199d3e3f329d6a2990ab0cb9cb3c3436924a3`
