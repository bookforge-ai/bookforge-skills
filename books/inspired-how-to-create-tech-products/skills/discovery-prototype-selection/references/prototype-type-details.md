# Prototype Type Details

Source: INSPIRED by Marty Cagan, Chapters 46–49

## Type 1: Feasibility Prototype (Ch46)

**What it is:** Working code written by one or more engineers to answer a specific technical question. It is not a user interface, not a product, and not productization-ready.

**When to use:** When engineers identify significant feasibility risk in the discovery process. Common triggers:
- Algorithm concerns (can we make this work at all?)
- Performance concerns (will it be fast enough?)
- Scalability concerns (will it hold up under load?)
- Fault tolerance concerns
- Use of a technology the team has not used before
- Use of a third-party component or service the team has not used before
- Use of a legacy system the team has not used before
- Dependency on new or related changes by other teams

**Who creates it:** Engineers only. Product managers and designers do not create feasibility prototypes.

**Fidelity:** None in the UI sense. It is code — throwaway code. No user interface, no error handling, no analytics, none of the work required for productization. Just enough code to answer the specific feasibility question.

**Typical time:** One to two days for most questions. Significantly longer for major new technology (machine learning, novel algorithms, major architectural changes).

**Key constraint — disposability:** Feasibility prototypes are intended to be throwaway code. It is normal and expected to be quick and dirty. The product manager does not judge when this code is "good enough" for production — that judgment belongs to engineers during productization, and they must be given full time to do delivery work properly.

**Key constraint — discovery framing:** Feasibility prototype work is discovery work, not delivery work. It is done as part of deciding whether to even pursue a particular approach. This distinction matters for team planning and morale.

---

## Type 2: User Prototype (Ch47)

**What it is:** A simulation. Smoke and mirrors. There is nothing behind the curtain. If you have a user prototype of an e-commerce site and enter credit card information, you will not actually be buying anything.

**When to use:** Usability testing, qualitative value testing, stakeholder alignment, team exploration of workflow.

**Who creates it:** Designers (primary). Some designers prefer to hand-code high-fidelity user prototypes, which is acceptable as long as they are fast and the prototype is treated as disposable.

**Fidelity spectrum:**

*Low-fidelity user prototype:* Does not look real — essentially an interactive wireframe. Useful for internal team thinking and testing information architecture and workflow. Does not capture the impact of visual design or differences caused by actual data. Faster and cheaper than high fidelity.

*High-fidelity user prototype:* Looks and feels very real. Data appears realistic (though it is not real or live). With good high-fidelity prototypes, you need to look closely to see it is not real. Required when testing value perception — users must experience the product concept as realistic for their reactions to be valid signal.

**Tools:** Standard prototyping tools developed for designers. Your designer almost certainly already has a preferred tool.

**Key limitation — cannot prove value:** The big limitation of a user prototype is that it is not good for proving anything, including whether a product will sell. Where many novice product practitioners go sideways is when they create a high-fidelity user prototype, put it in front of 10–15 people who all say they love it, and think they have validated their product. People say all kinds of things and then do something different. Better value testing techniques exist — use them for demand validation.

**Key use — communication:** A user prototype is one of the most important communication tools in product discovery. It enables stakeholders, engineers, and business partners to experience the product concept and develop shared understanding.

---

## Type 3: Live-Data Prototype (Ch48)

**What it is:** A very limited real implementation designed to collect actual usage data. It is not a simulation — real users use it for real work, generating real analytics. But it is substantially smaller and lower quality than the eventual product.

**When to use:** When you need actual usage data to address a major risk, and a user prototype simulation is insufficient. Canonical use cases:
- Search relevance (does this ranking algorithm actually surface better results?)
- Game dynamics (do users actually engage with this mechanic?)
- Social features (do users actually connect and interact as hypothesized?)
- Product funnel optimization (where do users actually drop off?)

**Who creates it:** Engineers only — designers cannot create live-data prototypes. This is real code.

**What it excludes by design:** All the work normally required for productization:
- Full set of use cases
- Automated tests
- Full analytics instrumentation (only the specific use cases being measured)
- Internationalization and localization
- Performance and scalability work
- SEO work
- Error handling and edge cases

**Typical scope:** 5–10% of the eventual delivery productization effort.

**Key constraint — not shippable:** A live-data prototype is not commercially shippable. It is not ready for prime time and cannot run a business on it. If live-data tests go well and the team decides to productize, engineers must be given full delivery time. It is not acceptable for a product manager to tell engineers that the live-data prototype is "good enough." That judgment does not belong to the product manager.

**Key constraint — stakeholder communication:** Executives and key stakeholders must understand the limitations of the live-data prototype explicitly. Managing this expectation is the product manager's responsibility.

**Speed:** Modern tooling makes live-data prototypes achievable in a couple of days to a week. Iteration cycles are fast once the prototype exists.

---

## Type 4: Hybrid Prototype (Ch49)

**What it is:** A combination of elements from user prototypes, feasibility prototypes, and live-data prototypes. The most common and powerful hybrid is the Wizard of Oz prototype.

**Wizard of Oz prototype:** Combines the front-end user experience of a high-fidelity user prototype with an actual person behind the scenes performing manually what would ultimately be handled by automation. From the user's perspective, it looks and behaves like a real product. Behind the scenes, it is a human (often the product manager or another team member) performing the manual work.

**When to use:** When you need to test the user experience of an automated system before the automation exists. Most powerful for:
- Automated chat or messaging systems
- Recommendation engines
- Any feature that will ultimately be algorithm-driven but where the interaction design matters now

**Example:** You want to build an automated 24/7 chat support system. Build a simple chat interface (user prototype front-end), but behind the scenes your customer service team (or you) manually receives the requests and composes responses. Users experience a realistic interaction. You learn what questions they ask, how they phrase them, and what responses satisfy them — all before writing any automation code.

**Key constraint — not scalable:** A Wizard of Oz prototype is absolutely not scalable. Never send significant amounts of traffic to one. Its value is qualitative learning, not quantitative proof.

**Key principle — build things that don't scale:** Hybrid prototypes embody the "build things that don't scale" philosophy of product discovery. By being a little clever, you can quickly create tools that let the team learn very quickly. The learning is mainly qualitative, but that is often where the biggest insights come from.

**Evolution path:** Wizard of Oz prototypes often evolve into live-data prototypes as the team begins to experiment with system-generated responses and algorithm-based approaches.
