"""Adds the phrase from a "New phrase" issue (its body comes in the ISSUE_BODY environment variable).

Prints the result for the issue comment. Exits 0 when the phrase was added, 1 when it was refused.
"""
import os
import sys

import phrases_lib


def fields(body):
    """An issue form's body is '### Label' followed by the answer, one block per field."""
    result, current, lines = {}, None, []
    for line in body.splitlines():
        if line.startswith("### "):
            if current:
                result[current] = "\n".join(lines).strip()
            current, lines = line[4:].strip(), []
        else:
            lines.append(line)
    if current:
        result[current] = "\n".join(lines).strip()
    return result


def main():
    f = fields(os.environ.get("ISSUE_BODY", ""))
    key, text = f.get("Category", ""), f.get("Phrase", "")
    data = phrases_lib.load()
    error = phrases_lib.add(data, key, text, "manual")
    if error:
        print(f"Not added: {error}.")
        return 1
    phrases_lib.save(data)
    print(f'Added "{phrases_lib.clean(text)}" to {phrases_lib.category(data, key)["id"]}. '
          "The TV picks it up within 30 minutes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
