# Search evidence

Execution: **local**. Recorded: 2026-09-29T07:37:58.185404+00:00.

## Input

Which two obstacles do the alignment notes identify when aligning AI to general human values?

## Retrieved original passages

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

Full model request, raw response, metrics, and validation fields: [B01-values-retrieval.json](B01-values-retrieval.json).
