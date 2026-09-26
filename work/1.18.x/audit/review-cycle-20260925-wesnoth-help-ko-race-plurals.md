# Review Cycle 2026-09-25: `wesnoth-help-ko.po` race plurality

## Scope

- Role: approved edit and verification
- Target: `work/1.18.x/ko/wesnoth-help-ko.po`
- Related reference: matching `race_name` rows in
  `work/1.18.x/glossary.tsv`
- Rule: when the English race label is plural, use Korean `들`; do not use
  `족` as a plural marker. Singular labels remain singular.

## Changes

| Location | Source context | Before | After |
| --- | --- | --- | --- |
| `wesnoth-help-ko.po:6461-6467` | `race^Saurian`, `race+female^Saurian` | `도마뱀족` | `도마뱀` |
| `wesnoth-help-ko.po:6471` | `race^Saurians` | `도마뱀족` | `도마뱀들` |
| `wesnoth-help-ko.po:6594` | `race^Merfolk` | `인어족` | `인어들` |
| `wesnoth-help-ko.po:6646` | `race^Nagas` | `나가족` | `나가들` |

The matching glossary rows were updated for the same contextual keys. No
ordinary narrative sentence containing the conceptual word `종족` was changed.

## Verification

- `msgfmt --check --check-format`: passed for `wesnoth-help-ko.po`
- `git diff --check`: passed for the PO file
- PO layout tests: 30 passed
- Glossary tests: existing unrelated failures remain; the previous
  `race+female^Saurian` mismatch was resolved by updating the PO entry.

## Remaining Scope

Other PO files still contain older `족` forms for plural race labels. They are
not changed in this cycle and should be reviewed one file at a time under the
same rule.
