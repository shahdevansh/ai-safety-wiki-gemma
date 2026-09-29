# Ask evidence

Execution: **local**. Recorded: 2026-09-29T07:21:18.595077+00:00.

Model: `gemma4:e2b-it-qat`; digest `07ea59a474013479c8b6b802bef095c40e964a1d776ba02f264c0e30e1aede0c`. Wall time: 16.674 s.

## Input

According to the notes, what is the AI's only goal in an assistance game, and what uncertainty must it resolve?

## Actual displayed result

According to the retrieved meeting notes:

AI’s only goal is to promote human interests [Pd36e317f50b9] [P0796ce4b536c]

It is uncertain what those interests are and must infer them [Pd36e317f50b9] [P0796ce4b536c]

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

### [P6641881a8987] vault/raw/alignment-fundamentals-notes.md:L1-L34

```text

### AI Safety Course: Group Image Exercise

- Three groups presented AI futures via generated images
- Group 1 (Outgroup): framed AI development as “camps”
  - Camp 1: slow development
  - Camp 2: race ahead (current reality)
  - Camp 3: pause + global coordination
  - Ideal future: global agreement on AI governance or ban
- Group 2: projected AI capabilities to 2045
  - \~90% of cognitive tasks, some physical via robotics
  - Also considered humanity becoming extraterrestrial
- One group: “equitable AI” prompt
  - Personal assistant for 8B+ people
  - Enables professional, personal, and creative fulfillment
  - Image depicted human-AI hybrid wielding AI for self-determined futures
  - AI freeing humans from repetitive tasks for creative work
- Facilitator noted all three were unusually original
  - Most common outputs: Dubai-with-parks, drones, guy playing guitar

### Breakout: Technical Challenges in AI Safety

- Format: pairs, each person presents then swaps; reconvene to share learnings

### Alignment: Core Challenges

- Defining alignment is itself unsolved
  - Aligning to individual risks enabling harmful behavior
  - Aligning to “general human values” produces Western/English-skewed outputs
  - No consensus on what those values even are
- Reward modeling is a fundamental bottleneck
  - SGD and numerical optimization assume a single optimum
  - Fails to capture cultural and individual diversity
  - Pluralistic alignment explored as a direction (modeling multiple values simultaneously) but not yet effective

```

### [P9e2cc541c9bc] vault/raw/alignment-lecture-notes.md:L38-L56

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

Full model request, raw response, metrics, and validation fields: [ask-1-assistance-objective.json](ask-1-assistance-objective.json).
