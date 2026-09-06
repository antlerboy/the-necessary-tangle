# Next work

Status: implemented and locally validated; publishing the public interface. Benjamin P Taylor requested removal of the GitHub sign-in barrier on 6 September 2026.

## Outcome

Allow visitors to submit a public event link directly on the map without an account or email address, receive a durable receipt, and enter the existing extraction and review process.

## In scope

The systemsmap submission form, public review queue, collection workflow, and a D1-backed submission endpoint in the existing events redirect service. Preserve all existing event filters and the legacy PSTA redirects. In this repository, update the pinned systemsmap revision in workflows, integration checks, and the current work/state records, including their release-22 build inputs.

## Out of scope

Atlas graph edits, domain changes, automatic publication of unreviewed submissions, and requirements for a visitor account.

## Acceptance checks

- Only a public URL is required; no account, email address, or GitHub redirect.
- The success response follows durable storage; failures preserve the visitor’s input.
- Duplicates, request size, origin, honeypot, and daily limits are handled.
- The public inbox feeds the maintained parser and review queue; no unreviewed event is automatically published.
- Event and language filters, calendar exports, and existing redirects remain intact.
- Service persistence tests, systemsmap tests, syntax checks, and `make validate` pass.
- Publish the endpoint and interface, verify a real receipt, and check the live page.

## Stop conditions

Stop after the anonymous submission route is live and verified, or report a concrete deployment blocker. Existing authorisation covers publication to the current public audience.

## Model route

Implementation and focused verification in the current session. No additional agents are required.

## Verification

The submission service was published from source commit `97d1a162994ff7abdd2104e5cb8682ebd74b9391`. A public POST of Nick’s supplied SCiO Polska link returned HTTP 201 and receipt `af54c356-c0b6-4732-bcbe-e868d622e5b2`; a separate database read confirmed storage. Public extraction imported that receipt and recognised the event already on the map. The systemsmap interface and collection pipeline are pinned to `27aaa618a1b68a52442e6232b08cd614f733ac73`. Service tests, systemsmap tests, and `make validate` passed.
