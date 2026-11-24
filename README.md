# Testing a small AI assistant

Deakin Data Science Club workshop, 25 November 2026 (Melbourne).

A small Python example for students who know C#. It demonstrates how to define
and test a decision boundary around an assistant using fictional campus events.

## Run the demo

Requires Python 3.9 or newer. No packages or API key are needed.

```sh
python3 demo.py
python3 demo.py --buggy
python3 demo.py --json
python3 exercises.py
```

On Windows, use `py -3` instead of `python3` if needed.

The fixed version passes **8/8** example cases. The intentionally broken version
passes **6/8**, failing ambiguity and advanced-event-first cases. Its exit code 1
is expected. The three additional exercises pass.

## What to look for

- Validate source completeness and detect conflicting records.
- Match both the requested topic and level.
- Ask for clarification when more than one event fits.
- Distinguish a successful empty result from a failed source.
- Save the input, expected outcome and observed outcome.

## C# to Python

Python's `for event in records:` visits the items like C#'s `foreach`.
Python uses indentation for blocks, `def` for functions and `and` for conjunction.
A dictionary stores named fields; a list holds the event records.

## Teaching scope

This is deterministic selection code, not a live LLM or an LLM benchmark.
It does not book events, call external services or parse natural-language dates.
Request fields and dictionary-shaped records are assumed. Topic matching ignores
case; level matching is exact. All source records are validated before selection.

The `--buggy` mode deliberately ignores the level constraint and chooses the
first match even when the request is ambiguous.

## Files

- `demo.py`: selector and eight-case demonstration
- `exercises.py`: three extra cases with answers
- `expected-output.txt`: fallback output for workshop use

## Reading

- [Python control flow](https://docs.python.org/3/tutorial/controlflow.html)
- [Python data structures](https://docs.python.org/3/tutorial/datastructures.html)
- [C# iteration statements](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/iteration-statements)

Manupriya Gupta · [LinkedIn](https://www.linkedin.com/in/manupriya-gupta/)
