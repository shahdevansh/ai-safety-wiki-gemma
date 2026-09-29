# Ask evidence

Execution: **local**. Recorded: 2026-09-29T08:20:23.492774+00:00.

Model: `gemma4:e2b-it-qat`; digest `07ea59a474013479c8b6b802bef095c40e964a1d776ba02f264c0e30e1aede0c`. Wall time: 11.753 s.

## Input

What physical or human controls did the infrastructure workshop propose to stop software from taking over?

## Actual displayed result

According to the retrieved meeting notes:

Proposed defense mechanisms: 1. Physical fail-safes with human override capabilities [P571ac3d9e151]

Proposed defense mechanisms: 2. Multiple humans in decision loops [P571ac3d9e151]

Proposed defense mechanisms: 3. Physical buttons/levers to shut off software entirely (airplane example) [P571ac3d9e151]

## Retrieved original passages

### [P571ac3d9e151] vault/raw/risk-defenses-notes.md:L1-L31

```text

### AI Safety Workshop - Kill Chain Analysis

- Participated in breakout exercise analyzing AI risk scenarios
  - Focused on critical infrastructure collapse as kill chain topic
  - Other participants covered gradual disempowerment, power concentration, mirror life risks

### Critical Infrastructure Vulnerabilities Discussion

- Cybersecurity threats to outdated government systems
  - Legacy software in oil/gas pipelines, power grids, water supplies vulnerable to AI-enhanced attacks
  - Bad state actors or terrorists could exploit these with powerful models
  - Recent attacks on US pipelines by human actors demonstrate current vulnerability
- Proposed defense mechanisms:
  1. Physical fail-safes with human override capabilities
  2. Multiple humans in decision loops
  3. Physical buttons/levers to shut off software entirely (airplane example)
  - AI lacks physical world access currently - key defensive advantage
  - Always cat-and-mouse chase between attack/defense capabilities

### Gradual Disempowerment Analysis (Participant A’s Presentation)

- Economic displacement concerns:
  - Workers replaced by AI losing meaningful work and income
  - Skills atrophy as AI handles previous human tasks
  - 40% unemployment scenario potential social crisis
- Defense strategies discussed:
  1. Proactive job creation and reskilling programs
    - Coordination between education, companies, government needed
  2. Universal Basic Income implementation
  3. Human-as-bottleneck model where AI abundance increases human leverage

```

### [P0796ce4b536c] vault/raw/alignment-lecture-notes.md:L1-L23

```text

### Objective Specification vs. Optimal Behavior

- Two distinct ways to build a system that optimizes an objective:
  - Specify the objective and let the system optimize it
  - Derive optimal behavior for a given objective and hard-code the behavior
- Control theory example: autopilot derives a simple control law (e.g., force = 6x deviation + 2x deviation²) without explicitly representing the cost function
- Humans and animals are similar: evolution optimizes for reproduction, but animals don’t consciously pursue it
- Classical AI systems (1960–2020) mostly fall into the “objective-in-the-machine” category

### Imitation Learning and the Problem of Objectives

- Imitation learning in the limit reproduces the behavior-generating mechanism of the training source
- Key complications:
  - Training data comes from millions of humans in invisible, varied circumstances (e.g., a Solidarity operative in Communist Poland)
  - Context is stripped; the resulting entity may not resemble a classical rational agent with stable objectives
- Open question: do imitation-trained models have a mixture of objective structures activated conditionally by context?
- Empirical signals suggest LLMs develop proxy goals: self-preservation, wealth, human companionship (natural byproducts of human training data)

### The Assistance Game Model

- Core framing: AI’s only goal is to promote human interests; it is uncertain what those interests are and must infer them
- “Interest” preferred over “preference” or “values”:

```

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

Full model request, raw response, metrics, and validation fields: [03-physical-defenses.json](03-physical-defenses.json).

## Fixed expectation

Proposals: physical fail-safes with human override, multiple humans in decision loops, and physical buttons/levers to shut off software. Attribute as proposals, not guaranteed defenses.

Expected source: vault/raw/risk-defenses-notes.md

Expected passage: Physical fail-safes with human override capabilities
