# Ask evidence

Execution: **local**. Recorded: 2026-09-29T08:16:23.250913+00:00.

Model: `gemma4:e2b-it-qat`; digest `07ea59a474013479c8b6b802bef095c40e964a1d776ba02f264c0e30e1aede0c`. Wall time: 17.435 s.

## Input

Why might taking someone straight to the mountaintop fail to respect what they want from the climb?

## Actual displayed result

According to the retrieved meeting notes:

Climbing Everest vs. being helicoptered to the top: outcomes matter, but so does agency [P4f87872fbb73]

Closing off “exits” (non-optimal choices) violates autonomy even if outcomes are optimal [P4f87872fbb73]

## Retrieved original passages

### [Pd36e317f50b9] vault/raw/alignment-lecture-notes.md:L21-L40

```text

- Core framing: AI’s only goal is to promote human interests; it is uncertain what those interests are and must infer them
- “Interest” preferred over “preference” or “values”:
  - “Values” triggered culture-war reactions
  - “Stated preferences” are easily manipulated; “interest” implicitly acknowledges that preferences can be shaped against one’s own good
- Inference mechanism: observe behavior and internal mental states, apply Bayesian priors
- Convergence: in theory, infinite data + fixed model of human decision-making → recover true preferences; in practice, unlikely to fully converge
- Non-identifiability problem: behavior alone can’t distinguish preferences from beliefs (e.g., a chess-player example: anti-rational agent looks identical from outside)
  - Bayesian prior that someone is anti-rational is infinitesimally low, so practically resolvable

### Hard Problems for the Assistance Game

- Preferences vs. interests: what someone prefers may not be good for them
- Preference plasticity and manipulation:
  - Addiction changes preference structures; AI should weight “reflective” preferences over drug-modified ones
  - Broader issue: preferences are shaped by external parties (e.g., patriarchal societies shaping women’s preferences)
  - Risk: AI systems are now themselves engaged in preference engineering
- Aggregation and social choice: what should AI do when serving multiple humans with conflicting interests?
- Autonomy dimension:
  - Climbing Everest vs. being helicoptered to the top: outcomes matter, but so does agency

```

### [P4f87872fbb73] vault/raw/alignment-lecture-notes.md:L38-L56

```text
- Aggregation and social choice: what should AI do when serving multiple humans with conflicting interests?
- Autonomy dimension:
  - Climbing Everest vs. being helicoptered to the top: outcomes matter, but so does agency
  - Closing off “exits” (non-optimal choices) violates autonomy even if outcomes are optimal
  - Strivings and achievements are not captured by pure state-of-the-world preferences
  - Fixable by incorporating mental states and process into the preference model; may require a modified decision theory
- Training data gap: no 400 trillion labeled examples of an assistance game solver; only human behavior data exists

### Governance and Regulation

- Behavioral red lines are hard to enforce without better understanding of system internals
- Compute governance is more tractable: regulate training runs and hardware rather than software
  - Software can be copied and transmitted freely; malware costs \~$12T/year globally and is largely uncontrolled
  - Hardware governance: if TSMC and all major chip manufacturers embed safety checks, bypassing requires building a fab from scratch (currently infeasible)
- Treaty organization models compared:
  - ICAO/IMO model: regulate the national regulators; hands-off, less intrusive
  - IAEA model: direct inspection powers, can enter facilities and seize files; strictly stronger but politically harder (US won’t accept jurisdiction)
  - Some White House voices now calling for “an IAEA for AI”
- CTBTO experience: UN structural impediments (5-continent division requirement, 4-year term limits, no institutional memory) make competent organizations very hard to build

```

### [Pd3902efa8beb] vault/raw/alignment-fundamentals-notes.md:L32-L52

```text
  - SGD and numerical optimization assume a single optimum
  - Fails to capture cultural and individual diversity
  - Pluralistic alignment explored as a direction (modeling multiple values simultaneously) but not yet effective
- Process reward models exist but limited to math
  - Still trained on traces that reach a “correct” answer
  - Don’t capture what a correct process actually looks like
- Agents still misread intent and don’t ask for clarification
  - Unlike human collaborators, they don’t flag ambiguity

### Interpretability: The Other Half

- Hard to align models without understanding their internals
  - Analogous to not knowing what a human is thinking
- Interpretability and alignment are two sides of the same objective
  - Need to know what direction to go, and how to get there
- Active research direction: detecting deception in reasoning models
  - Tracking discrepancies between thinking trace and explicit model output
  - Hidden states that lead to deceptive outputs as a target


[Participant biographies and personal follow-up actions removed for public sharing.]

```

### [P59429a0cbfc7] vault/raw/alignment-lecture-notes.md:L54-L67

```text
  - IAEA model: direct inspection powers, can enter facilities and seize files; strictly stronger but politically harder (US won’t accept jurisdiction)
  - Some White House voices now calling for “an IAEA for AI”
- CTBTO experience: UN structural impediments (5-continent division requirement, 4-year term limits, no institutional memory) make competent organizations very hard to build
  - Alternative: UN-affiliated but independently run (like ICAO), avoiding veto paralysis
- [Speaker-specific career anecdote removed for privacy.]

### Transformer Limitations and Safety

- Fixed-depth transformers cannot solve certain problems (e.g., graph connectivity) regardless of scale
- Chain-of-thought and recurrent models are effectively Turing machines: unbounded computation per token
- Transformers + context window + wrapping algorithm = functionally a Turing machine
- Current saving grace: transformers still fail to learn certain regularities (e.g., the Reversal Curse) due to sample complexity
- Not a strong safety guarantee: MCO chess analogy applies (win without understanding; bypass limitations via pattern matching)
- Recurrent models could flip the situation “almost overnight” with a research breakthrough

```

Full model request, raw response, metrics, and validation fields: [B02-mountaintop.json](B02-mountaintop.json).
