# Review Cycle 2026-09-26: Global `Saurian` terminology

## Scope

- Role: terminology follow-up reviewer and editor
- Target: active Korean PO entries containing the `Saurian/saurian`
  race name
- Decision: use `사우리안` and `사우리안들`

## Changes

- Replaced active `도마뱀`, `도마뱀들`, `도마뱀족`, `사우리안족`, and
  `사우리언` forms when the English source was `Saurian/saurians`.
- Updated race labels, faction labels, unit names, campaign text, help,
  manual, multiplayer, and unit descriptions.
- Synchronized the glossary entries for `Saurian`, `Saurians`, related unit
  names, and `Fanatical Saurian`.
- Preserved translations whose English source is `Lizard`, `lizards`, or
  `wyrm`, such as `늪 도마뱀` and dialogue that explicitly says `Lizard`.
- Preserved obsolete (`#~`) historical entries.

## Verification

- `msgfmt --check --check-format` for modified PO files: passed
- `audit_po_structure.py`: passed
- `audit_glossary.py`: passed
- No active `사우리언`, `사우리안족`, or `도마뱀족` Saurian usage remains.
