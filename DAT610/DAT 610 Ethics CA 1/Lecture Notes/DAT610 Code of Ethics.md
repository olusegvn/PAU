<!-- Slide number: 1 -->

DAT610  ·  Ethics and Privacy  ·  MSc Data Science

![preencoded.png](Image0.jpg)
The Data Scientist's
Rulebook

![preencoded.png](Image1.jpg)

![preencoded.png](Image2.jpg)

![preencoded.png](Image3.jpg)
Codes of Ethics & Their Implications for
Professional Data Scientists in the Tech Space
Stephen A. Adubi (PhD)

### Notes:
Welcome. Today we treat codes of ethics as technical specifications, not aspirational posters.
We will dissect them, find their gaps, and test them against real Nigerian scenarios.
This is a FORENSIC AUDIT, not a lecture.

<!-- Slide number: 2 -->
Session Roadmap
90 minutes  ·  4 parts  ·  6 interactive activities

01
Preamble

15 min
A Code's Moment of Truth

02
Technical Anatomy

30 min
Dissecting a Code of Ethics

03
Real-World Impact

30 min
When Codes Hit the Field

04
The Future

15 min
Limits of Codification & Wrap-Up

### Notes:
Walk through the structure before starting.
Emphasise this is not a passive lecture — students will debate, write, and argue.
The goal: by the end, every student can cite a code clause AND identify where it breaks down.

<!-- Slide number: 3 -->
PART
01
Preamble
A Code's Moment of Truth

### Notes:
Open with energy. The goal here is to establish that codes have real stakes.

<!-- Slide number: 4 -->

The Whistleblower's Dilemma
01  ·  THE HOOK

The Scenario
Three Questions
for the Room
2021. Frances Haugen, a data engineer at Facebook, leaked thousands of internal documents proving the platform's algorithm amplified hate speech and damaged teenage mental health — and senior leaders knew it.

The engineers who built that system were bound by the ACM Code of Ethics.
01
Did those engineers violate their code?
02
If they did — what happened to them?
03
If they did not — why not?
ACM Code of Ethics — Principle 1.2
"Avoid harm. In this document, 'harm' means negative consequences, especially when those consequences are significant and unjust."

Uncomfortable truth: a code is mostly a suggestion.
Its power lies in implication, not enforcement.

### Notes:
Quick show of hands — legally binding or suggestion?
Expected: very few will say binding. That's the right answer.

Nigerian context: Unlike doctors (MDCN) and lawyers (NBA), Nigerian data scientists have no statutory licensing body that can revoke credentials. The ACM code has zero legal enforcement mechanism in Nigeria. Its power is entirely in professional reputation and moral authority.

<!-- Slide number: 5 -->

Why Codes Exist — The Principal-Agent Problem
01  ·  THE HOOK

THE COMPANY
(Principal)
KNOWLEDGE
GAP
DATA SCIENTIST
(Agent)

Wants profit.
Lacks technical depth.
Asymmetric
information
Can affect millions
of lives in seconds.

CODE OF ETHICS  =  The Agent's Promise

![preencoded.png](Image0.jpg)
A commitment to use technical knowledge responsibly, even when no one is watching.
Why this matters for Nigerian data scientists specifically:
1.
You routinely know more than your employer about the risks your model creates. That asymmetry is your burden.
2.
Regulators — NDPC, CBN, NCC — are building accountability frameworks. Self-regulation today prevents coercive regulation tomorrow.
3.
Nigeria's fintech, health-tech and govtech sectors are young. One scandal now could set back the entire profession by a decade.

### Notes:
The principal-agent problem: companies can't perfectly monitor experts they rely on.
The code is the expert's self-binding commitment — it substitutes for direct oversight.

Nigerian regulatory landscape brief:
- NDPC (Nigeria Data Protection Commission) — established under NDPA 2023
- CBN Consumer Protection Framework — covers algorithmically generated financial advice
- NCC Consumer Code — applies to telecom-integrated data services

<!-- Slide number: 6 -->

The Trust Equation
01  ·  THE HOOK

Technical
Capability
+
Professional
Code
=
Public
Trust

Nigeria's Fintech Moment
The Horizon Warning
Nigeria has more than 200 CBN-licensed fintechs. Millions of Nigerians now receive credit decisions, insurance scores, and health risk assessments from algorithms. Public trust is the only licence these companies cannot buy — only earn.
The UK Post Office Horizon scandal saw faulty software imprison 900 innocent postmasters.

### Notes:
INTERACTIVE POLL: Raise hand if you'd trust a doctor without a code. A lawyer. A journalist. A data scientist.
The point: the public does NOT yet expect us to have a code. That means trust is ours to build — or squander.

Key message: Once the NDPA 2023 enforcement mechanisms mature, this equation becomes a legal one, not just an ethical one.

<!-- Slide number: 7 -->
PART
02
Technical Anatomy
Dissecting a Code of Ethics

### Notes:
This section is the analytical core. Students should feel like auditors opening a technical document.

<!-- Slide number: 8 -->

The Four Pillars of Data Science Ethics
02  ·  TECHNICAL ANATOMY
Consistent across ACM, ASA, IEEE, DSA — and reflected in Nigeria's NDPA 2023

Justice & Fairness

I
II

![preencoded.png](Image0.jpg)

![preencoded.png](Image1.jpg)
Beneficence &
Non-Maleficence
Do good; avoid harm.
The Hippocratic Oath for data.
Treat people equitably.
Design to detect and remove bias.
ACM 1.2 · "Avoid harm"
ACM 1.4 · "Fair treatment of all persons"

![preencoded.png](Image2.jpg)

Autonomy & Consent

III
IV

![preencoded.png](Image3.jpg)
Transparency &
Explainability
Respect the right to control one's data. Informed consent is non-negotiable.
Be open about your methods,
limitations, and uncertainty.
NDPA 2023 · Sec. 25 — valid consent
ASA Ethical Guidelines · Transparency

### Notes:
Ask: Which pillar do you think is MOST commonly violated in Nigerian tech?
Expected answer: Autonomy & Consent — dark patterns, pre-ticked opt-ins, poorly translated privacy notices.

The NDPA 2023 accuracy principle (Sec. 26(1)(d)) maps onto Non-Maleficence.
The lawful basis documentation requirement maps onto Transparency.

<!-- Slide number: 9 -->

Group Activity — Pillar Deep Dive
02  ·  TECHNICAL ANATOMY

THE ACTIVITY  ·  5 minutes, then class bounce
THE SCENARIO
Predictive Policing Across Lagos State

Group A  ·  Justice & Fairness
List 3 technical questions this pillar forces you to ask about the training data.
A Lagos State Ministry of Justice contract: build a model predicting where violent crime is likely to occur across the metropolis.

The available training dataset consists entirely of SARS arrest records spanning 2015–2020.

Group B  ·  Transparency
Who must be told about the model's limitations — and in exactly what format?

Group C  ·  Autonomy & Consent
Did individuals in the arrest records consent to this secondary use of their data?

SARS was forcibly disbanded in October 2020 following the #EndSARS protests. Reports documented systematic targeting of young Nigerians — particularly those in tech — based on appearance, not behaviour. This bias is baked into the data.

Group D  ·  Beneficence / Non-Maleficence
Define 'harm' for this model and name the three most likely victims of that harm.
Bounce: Does Group B's transparency answer make Group A's bias problem worse or better?

### Notes:
KEY BOUNCE: "If we are fully transparent that the model flags young men in Agege and Oshodi more than Lekki, does that transparency institutionalise the bias?"

Expected student insight: Transparency is necessary but NOT sufficient. A biased model + honest disclosure is still a biased model.

Handle this with care — #EndSARS is recent and politically charged. The pedagogical goal is NOT to relitigate the protests but to show how historical institutional bias becomes encoded in data, and therefore in models.

<!-- Slide number: 10 -->

Where Codes Fall Silent
02  ·  TECHNICAL ANATOMY
Codes are written in principles, not algorithms. They cannot anticipate every situation.

The "Public Good" Problem
Speed vs. Thoroughness
The ACM code says the data scientist must ensure "the public good is the central concern."

But who defines 'public good' in Nigeria?

· The FIRS, which wants a model to flag tax evaders?
· The CBN, which wants access to credit behaviour data?
· The 40 million Nigerians without a formal financial identity, who need a fair credit path into the system?
The ASA code requires "thoroughness and due diligence." But in Nigeria's hyper-competitive fintech space, a one-week delay for a bias audit could mean Moniepoint or OPay grabs your product's market window.

"Move fast and build things" vs. "first, do no harm."

The code does not rank these principles. That judgment is yours.

### Notes:
KEY POINT: "The code gives you a framework for thinking, not a pre-packaged answer."
When you defend a technical decision to a regulator or in court, your ability to articulate structured ethical reasoning — grounded in a code — is worth far more than a gut feeling.

Nigerian fintech context: The speed-safety tension is acute. Some lenders have deployed poorly validated credit models that disproportionately rejected loan applications from northern Nigerian states. The NDPC has the power to investigate these cases under NDPA 2023.

<!-- Slide number: 11 -->
02  ·  TECHNICAL ANATOMY

The Data Science
Trolley Problem
It's not in the code.
The code says "avoid harm" — but every option here causes harm. The code does not rank harms. You must.
So why bother with a code?

You are building the decision logic for an autonomous vehicle. The system must choose who to prioritise in a mathematically unavoidable collision.

You open your code of ethics. Where is the answer?
1.
Gives all parties a shared vocabulary for the debate
2.
Ensures every key perspective is formally examined

The code doesn't remove your ethical burden.
3.
Moves the test from "what is right" to "how did you reason"
It gives you a structured process to bear it responsibly — and to defend your reasoning when questioned.

### Notes:
BOUNCE: "If the code doesn't have the answer, what's the point of it?"
Expected: It provides a shared language, ensures structured reasoning.

Follow-up: "In a Nigerian courtroom or CBN hearing, your ability to demonstrate that you reasoned through the ethical implications using a recognised professional framework will always be stronger than 'I used my judgment.'"

<!-- Slide number: 12 -->
PART
03
When Codes Hit the
Real World
Implications for daily practice

### Notes:
This is the most practically important section. Ground every scenario in Nigerian professional reality.

<!-- Slide number: 13 -->

Implication 1 — The Data Provenance Mandate
03  ·  REAL-WORLD IMPACT

What does your code require?

![preencoded.png](Image0.jpg)
THE SCENARIO  ·  The Hospital Model

A
Ignore it. You didn't create the error — the hospital's data team did.
Lagos University Teaching Hospital
Your team builds a patient readmission prediction model from 10 years of EHR data provided by the hospital.

Three months after deployment — 200 patients per week affected — you discover that for the first 5 years, the variable 'primary payer' (NHIA vs. out-of-pocket) was systematically mis-coded. The error understates the medical burden on informal-sector workers. The model is live. Discharge decisions are being made with it.

B
Quietly correct it in the next model version. No disruption necessary.

C
Alert the hospital immediately, suspend discharge decisions, and recommend a patient review.

The correct answer is C.
You are accountable for the entire data pipeline — from original collection through live deployment.

NDPA 2023 · Sec. 26(1)(d): "Personal data shall be accurate and, where necessary, kept up to date; every reasonable step must be taken to ensure that inaccurate data is erased or rectified."

### Notes:
The code does not care who made the original error. You deployed the model. You own the consequences.

NDPA 2023 processor liability: Your team is a data processor under Sec. 43. The accuracy principle at Sec. 26(1)(d) applies to the data controller (hospital), but the processor's own duty of care is established by the processing contract.

Follow-up question: What would a proper data provenance audit have looked like before deployment? Could a data card (similar to Google's approach) have flagged this gap?

<!-- Slide number: 14 -->

Implication 2 — The Whistleblower Pathway
03  ·  REAL-WORLD IMPACT

![preencoded.png](Image0.jpg)
THE DILEMMA  ·  A CBN-Licensed Digital Lender
The Code
Gives You
Moral Cover
Your CFO instructs you to re-tune the credit scoring model to maximise short-term loan uptake. Internal analysis shows this will push high-risk loan products to vulnerable users — informal workers in Kano and Onitsha with no financial buffer for defaults.

You raise the concern. The CFO's response: "It's perfectly legal. Optimise the model or resign."
The Escalation Ladder  ·  ACM 1.3, 2.5

"I am not refusing because I am being difficult. I am refusing because I am bound by a professional code of ethics that I have a duty to uphold."

This transforms personal opinion into professional obligation.

Step 1
Raise in writing
Document your objection formally. Request an ethics or risk review.

Step 2
Escalate to the board
If line management fails, escalate to the compliance committee or board audit.

Step 3
Report externally
File with the CBN Consumer Protection Department or NDPC.

Step 4
Resign and disclose
The code implies this duty where harm is persistent and unaddressed.

### Notes:
KEY CHALLENGE to pose: "What if there is no authority to report to? Nigerian whistleblower protection legislation remains incomplete — the Whistleblower Protection Bill has stalled in the NASS."

The code's moral cover is real even when legal protection is absent:
1. It anchors your refusal in professional obligation, not personal preference.
2. It matters in future job references and professional reputation.
3. The CBN and NDPC are increasingly sympathetic to professionals who raised concerns before a breach became public.

Do NOT let students conclude that 'the law doesn't protect you, so the code is useless.' Push back hard on this.

<!-- Slide number: 15 -->

Implication 3 — From Ethics to Legal Liability
03  ·  REAL-WORLD IMPACT
The Professionalisation Trajectory
1960s
1990s
2023
2030?

Engineering
Medicine
Nigeria NDPA
Data Science?
PE licence laws link code violations to civil negligence in US & UK
Clinical negligence standard anchored explicitly in professional codes
First statutory accountability framework for data professionals in Nigeria
Chartered status — code violation as direct evidence of negligence

2030 SCENARIO  ·  Pair Activity — 2 minutes
You are a Chartered Data Scientist. A plaintiff's lawyer is suing you: a credit model you built denied loans to 8,000 small traders in Aba, causing documented financial harm. The lawyer opens the ACM Code of Ethics in court and turns to a specific clause. Which one?
Most likely targets:
ACM 1.2  —  "Avoid harm" (primary)       ACM 2.03  —  "Know the limitations of your data"       ASA Ethical Guidelines  —  "Ensure quality of data"       NDPA 2023 · Sec. 26(1)(d)  —  Accuracy principle

### Notes:
KEY MESSAGE: In medicine and engineering, a code violation can be introduced as evidence of professional negligence in civil courts.

Nigerian legal path: Under NDPA 2023, the NDPC can impose administrative fines (up to 2% of annual gross revenue). The Federal Competition and Consumer Protection Commission (FCCPC) can pursue civil remedies.

The direction of travel is clear. Codes are not just ethical guides — they are the early architecture of professional liability.

<!-- Slide number: 16 -->
PART
04
The Limits of
Codification
The future & wrap-up

### Notes:
Open up the meta-question: can ethics be fully codified? The answer shapes how students should think about their careers.

<!-- Slide number: 17 -->

Write Your Clause
04  ·  LIMITS & FUTURE

THE CHALLENGE  ·  2 minutes · Individual · Specific · No vague statements
Write ONE new clause for the ACM Code of Ethics addressing the era of Generative AI and the Nigerian data reality. Make it technically grounded and enforceable.
Four examples to spark — not constrain — your thinking:
AI CONTENT LABELLING

SYNTHETIC DATA
A data scientist must document and disclose when generative AI synthetic data is included in model training, and must provide validation evidence of its distributional alignment with real-world data before production deployment.
Any content produced wholly or substantially by a generative AI system intended for public dissemination must be explicitly labelled as AI-generated, regardless of the commercial interests of the deploying organisation.

LINGUISTIC EQUITY
TRAINING DATA COPYRIGHT
A data scientist deploying an NLP model in a multilingual environment must document performance benchmarks across all target languages — including Nigerian Pidgin, Hausa, Yoruba and Igbo — before deployment.
A data scientist must not knowingly incorporate copyrighted material in model training unless documented licence or fair-use justification is on file and accessible to any auditor upon request.

### Notes:
After 2 minutes, ask 4–5 students to share.
Write clauses on the board. Ask the class to vote on the strongest one.

Award points for: specificity (is it testable?), technical grounding (does it reference a concrete action?), Nigerian/African relevance (does it account for local conditions?).

Best clauses often come from the intersection of a specific technical problem the student has already encountered and a code principle they now understand more deeply.

<!-- Slide number: 18 -->

Key Instruments
Codes of ethics are
our profession's
constitution.
ACM Code of Ethics
2018

ASA Ethical
Guidelines 2022

IEEE Code of
Ethics 2020
They define what we owe to the individuals behind every data point — the trader in Aba, the patient in Maiduguri, the student in Nsukka.

Nigeria NDPA
2023

CPN Act
(Cap. C25) 2004
The code is not your master.
The code is your guide.

### Notes:
Closing message: Codes of ethics are living documents. They are incomplete by design — because the ethical challenges of data science are still being written.

You are not just students of this field. You are among the people who will decide what responsible data science looks like in Nigeria over the next 20 years.

Optional follow-up assignment: Choose one of the four pillars and write a 1,000-word case study showing how a Nigerian organisation either upheld or violated it. Cite the relevant code clause and the applicable provision of the NDPA 2023.