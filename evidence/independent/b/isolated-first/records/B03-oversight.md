# Ask evidence

Execution: **local**. Recorded: 2026-09-29T07:25:36.538232+00:00.

Model: `gemma4:e2b-it-qat`; digest `07ea59a474013479c8b6b802bef095c40e964a1d776ba02f264c0e30e1aede0c`. Wall time: 15.698 s.

## Input

How do the notes contrast the ICAO/IMO and IAEA approaches to AI oversight?

## Actual displayed result

According to the retrieved meeting notes:

The ICAO/IMO model regulates national regulators and is hands-off and less intrusive. [P9e2cc541c9bc]

The IAEA model involves direct inspection powers, can enter facilities and seize files, and is strictly stronger but politically harder because the US won’t accept jurisdiction. [P9e2cc541c9bc]

## Retrieved original passages

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

Full model request, raw response, metrics, and validation fields: [B03-oversight.json](B03-oversight.json).
