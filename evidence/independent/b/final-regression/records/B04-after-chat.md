# Ask evidence

Execution: **local**. Recorded: 2026-09-29T07:39:41.606606+00:00.

Model: `gemma4:e2b-it-qat`; digest `07ea59a474013479c8b6b802bef095c40e964a1d776ba02f264c0e30e1aede0c`. Wall time: 6.798 s.

## Input

What is the date, start time, and room number of the next AI safety workshop?

## Actual displayed result

Insufficient evidence: the provided sources do not answer this question.

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

Full model request, raw response, metrics, and validation fields: [B04-after-chat.json](B04-after-chat.json).
