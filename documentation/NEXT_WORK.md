# Next work

## Current packet: 0.42 Ubuntu reproducibility diagnostic

Status: diagnostic-only candidate accepted for one PR CI run; outcome pending. PR 106 CI run 42341157810 failed the 0.42 nodes guard after the historical rebuild; browser steps did not run. Compare each rebuilt public collection with committed HEAD before the existing guards, report bounded public differences and retain every assertion and ordered hash. Validate the diagnostic against unchanged and deliberately changed local fixtures. Preserve all data, source packets, profiles, routes, and guards. After exact local review, the coordinator may push one normal-branch update for one PR CI run, record the outcome, and stop. No merge, manual workflow dispatch, Pages retry, deployment, release, content correction, or further retry is authorised in this packet. The 0.41 Pages checkpoint remains in force; public edition 0.40 remains independently verified.
