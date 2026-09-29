# Chat evidence

Execution: **local**. Recorded: 2026-09-29T07:31:45.365760+00:00.

Model: `gemma4:e2b-it-qat`; digest `07ea59a474013479c8b6b802bef095c40e964a1d776ba02f264c0e30e1aede0c`. Wall time: 3.223 s.

## Input

For this conversation only, my project codename is Tangerine. Acknowledge it without saving it to the wiki.

## Actual displayed result

Got it. For this conversation only, your project codename is Tangerine.

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

### [P393649e8c594] vault/raw/alignment-lecture-notes.md:L54-L67

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

Full model request, raw response, metrics, and validation fields: [chat-05.json](chat-05.json).
