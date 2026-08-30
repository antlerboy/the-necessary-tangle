# Reader update 0.20.3

Date: 30 August 2026

This update takes the next independent tranche from the running update thread. It deliberately does not publish the modified Hadorn/Schwarz/Hirsbrunner Systemic Evolution derivative, which remains behind source-owner verification and curator approval.

## Reader changes

- The living mark is now interactive. A click selects another mark from the existing local manifest. A double-click opens the mark itself full-screen; Escape uses the browser's normal full-screen exit. Keyboard activation selects another mark. Reduced-motion preferences continue to receive a still representation.
- The main map already supported clicking any rendered node to make it the new centre. That behaviour is retained rather than reimplemented.
- A new `Card view` presents the current map focus and its visible connections grouped by relation family. Selecting a connected entry makes it the new centre while retaining the current layer.
- The header displays one randomly selected `little RedQuadrant rule #x: ...` on each fresh load. Selecting the rule deals another. `all 256` opens a dedicated readable list. The canonical text remains the public running-update comment and is cached in the browser rather than maintained as a second hand-edited list.
- Existing whole-card click behaviour and the public-language change from `Claims and disputes` to `Statements and disputes` are retained.

## Donella Meadows map correction

Donella Meadows already had documentary authorship connections to *Thinking in Systems*, *Leverage Points* and *Dancing With Systems*. The default substantive map suppresses documentary authorship, so the person entry could appear isolated despite those connections.

The live reader now adds one source-established substantive relation before the graph is indexed:

- Donella Meadows `developed` Leverage points — source: the Donella Meadows Project publication of *Leverage Points: Places to Intervene in a System*.

This is deliberately narrow. It fixes the misleading isolation without converting authorship into a generic claim of influence or priority.

## SCiO source refresh

The live reader now replaces the old `SCiO CF Resources v9 draft` / no-public-link record with the current public `SCiO CF Resources v10 Jan2025` guide.

It also registers two current bounded source corpora:

- SCiO resource library: https://www.systemspractice.org/resources — 572 records shown in the live public index when checked on 30 August 2026. Preserve SCiO's resource types, categories, authorship and item-level reuse conditions during ingestion.
- SysBoK, from SCiO: https://www.systemspractice.org/sysbok-from-scio and https://kumu.io/koryckaa/scio-sysbok-v1#map — use as an explicitly attributed comparator/source-discovery graph. SCiO describes it as incomplete and work in progress, with particular emphasis on `Precedents` and `Dependent Derivatives`.

Existing SysBoK snapshot source records in the reader now point to the public SCiO SysBoK page rather than appearing as private/no-link records. Their item-level wording remains tied to the named snapshot until it is reconciled against the live Kumu graph.

## What is intentionally not claimed as complete

This update registers and corrects the live SCiO corpus boundary; it does not pretend that all 572 resource records have already been normalised into the canonical graph. The next data pass is a reproducible item-level import, deduplication and reconciliation job. The same applies to the live Kumu node-and-link structure.

The Systemic Evolution candidate reconciliation remains unpublished until the explicit source-owner review condition has been satisfied.

## Verification target

Before merge:

- validate the changed JavaScript;
- check the dedicated 256-rule page parses and has a useful failure state;
- inspect the PR diff for accidental changes to canonical comparator data;
- run the repository validation workflow;
- after merge, verify the exact Pages deployment commit and spot-check the live reader interactions.
