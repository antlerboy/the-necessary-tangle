# Next work

## Current packet: 0.42 exact baseline regeneration

Status: locally reviewed fix; one full Ubuntu CI run pending. PR 106 diagnostic run 42342764685 found 13 historical layout coordinates differing by at most 2.23e-16, and four unchanged 0.41 evidence records reappended in a different order. Restore the reviewed coordinate values and evidence positions in the 0.42 generator with narrow preconditions; preserve all strict ordered hashes, source records, profiles, and reader content. Verify the actual Ubuntu differences and rejection of material, textual, missing-record, and unrelated-order mutations. After exact local review, the coordinator may push one PR update for one Ubuntu CI run and stop. No merge, manual dispatch, Pages retry, deployment, or release is authorised. Edition 0.41's Pages deployment timed out twice; the independently verified public edition remains 0.40.
