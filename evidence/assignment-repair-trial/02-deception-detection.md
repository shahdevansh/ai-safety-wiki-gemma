# Ask evidence

Execution: **local**. Recorded: 2026-09-29T07:33:41.653971+00:00.

Model: `gemma4:e2b-it-qat`; digest `07ea59a474013479c8b6b802bef095c40e964a1d776ba02f264c0e30e1aede0c`. Wall time: 13.532 s.

## Input

In the fundamentals session, what two things were compared to look for deception in reasoning models?

## Actual displayed result

Insufficient evidence: citation validation failed; inspect the saved raw Gemma response.

## Retrieved original passages

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

### [P19588883e584] vault/raw/risk-defenses-notes.md:L29-L51

```text
    - Coordination between education, companies, government needed
  2. Universal Basic Income implementation
  3. Human-as-bottleneck model where AI abundance increases human leverage
- Cultural erosion risks:
  - AI content overwhelming human-generated content
  - Mandatory labeling of AI-generated content as intervention
- Democratic hollowing identified as biggest threat
  - Could lead to civil war scenarios
  - AI exacerbating existing political polarization
  - No clear solutions identified

### Power Concentration \&amp; Governance Solutions

- Model ensembling as risk mitigation
  - Use multiple AI models (Anthropic, OpenAI, Grok) for government decisions
  - Compare answers to identify potential manipulation or bias
  - Diversification approach similar to financial risk management
- AI Constitution concept explored:
  - Challenge of writing legislation for fluid AI capabilities
  - Question of allowing AI to bypass constitution in emergencies
  - Enforcement mechanisms unclear
  - Separation of powers principle: AI-assisted but human-accountable institutions checking each other
- Broader team involvement in model training to prevent concentration

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

Full model request, raw response, metrics, and validation fields: [02-deception-detection.json](02-deception-detection.json).

## Fixed expectation

According to the session notes, compare the thinking trace with explicit model output; do not claim this is a proven reliable deception detector.

Expected source: vault/raw/alignment-fundamentals-notes.md

Expected passage: Tracking discrepancies between thinking trace and explicit model output
