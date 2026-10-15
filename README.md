# dfa-simulation

A small toolkit for simulating **Deterministic Finite Automata (DFAs)** in pure Python. It traces how a DFA processes a word step by step, explores which strings a DFA accepts up to a given length, and collects usage statistics about states and transitions.

No imports, no external libraries.

## Features

| Function | What it does |
|---|---|
| `simulate_DFA(dfa, word)` | Runs the DFA on a word and returns `True` if it is accepted |
| `computation_history(dfa, word)` | Returns every configuration the DFA passes through while reading the word |
| `language_exploration(dfa, n)` | Tests every string of length `0` to `n` and marks each one `ACCEPT` or `REJECT` |
| `language_report(dfa, n)` | Counts state visits, transition uses and accepted/rejected strings over all strings of length `0` to `n` |

## Defining a DFA

A DFA is a plain Python dictionary. This one accepts strings with an **even number of `a`'s**:

```python
dfa = {
    "states": ["q0", "q1"],
    "alphabet": ["a", "b"],
    "start_state": "q0",
    "accepting_states": ["q0"],
    "transitions": {
        "q0": {"a": "q1", "b": "q0"},
        "q1": {"a": "q0", "b": "q1"},
    }
}
```

Any alphabet and any number of states are supported.

## Usage

### Computation history

Each configuration has the form `<consumed>-<state>-<remaining>`:

```python
>>> computation_history(dfa, "bab")
['-q0-bab', 'b-q0-ab', 'ba-q1-b', 'bab-q1-']
```

The first entry is the starting configuration, before any symbol is read. The last one shows the state after the whole word has been read.

### Language exploration

```python
>>> language_exploration(dfa, 2)
{'': 'ACCEPT', 'a': 'REJECT', 'b': 'ACCEPT',
 'aa': 'ACCEPT', 'ab': 'REJECT', 'ba': 'REJECT', 'bb': 'ACCEPT'}
```

Strings are ordered by length, then by alphabet order. The empty string `''` stands for ε.

### Language report

```python
>>> language_report(dfa, 3)
{'q0_visit_count': 32, 'q1_visit_count': 17,
 'q0_a_q1_transition_count': 12, 'q0_b_q0_transition_count': 12,
 'q1_a_q0_transition_count': 5, 'q1_b_q1_transition_count': 5,
 'total_accepted': 8, 'total_rejected': 7}
```

- **`<state>_visit_count`:** how many times each state was entered. The start state counts as visited once at the beginning of every run.
- **`<from>_<symbol>_<to>_transition_count`:** how many times each transition was used.
- **`total_accepted` / `total_rejected`:** how many of the tested strings ended in an accepting state and how many did not.

## How it works

- **String generation:** `all_strings(alphabet, n)` builds all strings level by level. It starts from the empty string and, at each step, appends every alphabet symbol to each string of the previous length. This produces strings of length `0` to `n` without recursion or `itertools`.
- **Simulation:** the DFA starts in `start_state` and follows `transitions[state][symbol]` for each character. A word is accepted if the final state is in `accepting_states`.
- **History and statistics:** the same walk through the transitions is reused. Each step either records a configuration string or updates the counters.

## Example DFAs

The assignment came with three DFAs that are useful for testing:

| DFA | Language over `{a, b}` | States |
|---|---|---|
| DFA 1 | Even number of `a`'s | 2 |
| DFA 2 | Strings ending with `ab` | 3 |
| DFA 3 | At most one `a` | 3 |

## Project structure

```
.
├── dfa-simulation.py   # DFA simulation, history, exploration and report functions
└── README.md
```

## Background

Developed as Homework 4 (DFA Simulation, Computation History, and Language Exploration) for an introductory programming course. Solutions were limited to basic Python with no imported modules.
