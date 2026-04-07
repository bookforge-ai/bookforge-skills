# Risk Sequencing Patterns Reference

## The Core Principle

When you need multiple risky actions to all succeed, and you can choose the order of attempts, **attempt the riskier action first** — while fallback options remain available.

This is a direct corollary of backward induction: reason from the end-state you need to reach, and structure the sequence so that failure of the hardest step leaves the maximum number of options open.

---

## The Orange Bowl Case (Source: Ch. 2, pp. 71-73)

**Situation:** Nebraska needs net +3 extra points across two touchdowns to win the championship.
- Option A: Two-point conversion (~50% success, needed twice for a certain win, or once for a tie)
- Option B: One-point kick (~95% success, "safe")
- Osborne's order: B first (safe kick after TD1), then A (two-pointer after TD2 — now forced)

**Why Osborne's order was wrong:**

The only scenario where order matters is when exactly one attempt fails. Consider each case:
- Both succeed: order is irrelevant. Win regardless.
- A fails, B succeeds: if B→A order, A is the last attempt. No fallback. Lose. If A→B order, A fails but B after TD2 still gives a tie (championship by record).
- B fails, A succeeds: under B→A, this means the kick after TD1 failed (very rare), but two-pointer after TD2 succeeds. Net result: 31-30, Nebraska wins. Under A→B, same outcome.
- Both fail: order is irrelevant. Lose regardless.

**The asymmetry:** The only scenario where order changes the outcome is "A fails, B succeeds." Under B→A (Osborne's plan), this means: one-point kick succeeds after TD1 → two-pointer attempted after TD2 → fails → lose. Under A→B (correct): two-pointer attempted after TD1 → fails → score TD2 → one-point kick → tied game → championship by record.

**Backward induction logic:** Work backward from "what do I need after the second touchdown?" If the two-pointer failed on the first TD, you need a two-point attempt after the second TD too — but then failure means game over with no remaining fallback. If the two-pointer succeeded on the first TD, the one-point kick after the second TD is pure insurance.

---

## Generalized Risk-Sequencing Rule

**Setup:** You need both action A (probability p_A of success) and action B (probability p_B of success) to achieve your goal, where p_A < p_B (A is riskier). You can attempt them in either order. Failure of one does not make the other impossible.

**Compare outcomes where exactly one attempt fails (the only scenario where order matters):**

| Scenario | Order A→B outcome | Order B→A outcome |
|---|---|---|
| A fails, B succeeds | Partial goal achieved (B succeeded; fallback) | Forced to attempt A after using up B |
| B fails, A succeeds | Partial goal achieved (A succeeded; fallback) | Same as A→B |

In Order A→B: if A fails first, B is still available and may recover a fallback position.
In Order B→A: if B succeeds but A fails, no fallback remains.

**Recommendation:** Always attempt the lower-probability (harder, riskier) action first when a fallback exists.

---

## Domain Applications

### Sports / Competition

**Tennis serves:** First serve = aggressive (high risk, high reward). Second serve = safe (lower risk). If you hit the easy serve first and miss the aggressive one, you double-fault. The correct sequencing is hardest first (aggressive serve), safe second. Tennis players do this instinctively; the game-theoretic logic is exactly the risk-sequencing principle.

**Golf approach shots:** If playing for a par save requires a risky chip followed by an easy putt, attempt the risky chip while you still have the putt as backup.

---

### Business / Product Development

**New product launch:** A team must both (A) secure a manufacturing partner (uncertain, hard negotiation) and (B) sign a marketing agency (easier, multiple options available). Correct order: negotiate manufacturing first. If it fails, the marketing spend has not been committed. If manufacturing is locked in first, marketing negotiations happen with all options open.

**Investment due diligence:** A startup needs both (A) regulatory approval (uncertain, slow) and (B) investor commitment (easier to get conditionally). Correct order: pursue regulatory approval while investor commitment is conditional. Lock in regulatory approval, then firm up the investment. Investor commitments typically allow conditional withdrawal; regulatory rejections do not refund marketing spend.

---

### Negotiation

**Multi-issue negotiation:** You need to resolve both a harder concession (salary, equity, price) and an easier one (start date, title, payment terms). Attempt the harder concession first. If it fails, the easier concession has not been spent as a goodwill gesture. If the harder concession succeeds, the easier one strengthens the deal.

**Warning:** The counterparty may prefer the reverse order — they want you to spend your easy concessions early so that the hard ask comes after you are invested in the deal. Recognize this tactic and sequence your concessions to preserve your fallback.

---

### Career Decisions

**Switching fields:** Moving from finance to technology requires both (A) building a technical portfolio (uncertain, 6-month effort) and (B) updating a network and personal brand (lower risk, ongoing). Correct order: invest in the portfolio first while still employed in finance (fallback intact). Do not announce the pivot publicly (B) before the portfolio demonstrates readiness (A). If A stalls, the fallback position in finance is still accessible.

---

## When the Principle Does Not Apply

Risk sequencing only matters when:

1. Both actions are needed (not just preferred)
2. The order is flexible (some sequences are forced by logistics)
3. Failure of one action does not eliminate the option to attempt the other
4. A fallback outcome exists if the harder action fails first

If there is no fallback (all-or-nothing), order is irrelevant. If the actions are independent in payoff, backward induction may reveal a different priority. Always draw the tree first.

---

## Quick Decision Check

Ask these questions before sequencing:

1. Which action has the lower probability of success? → Attempt this one first.
2. If the harder action fails, what fallback remains? → The answer defines your "tie" or partial win.
3. If the easier action is used first and the harder fails, is the fallback still accessible? → If no: you are locked in; Osborne's mistake.
4. What is the difference in outcome between "harder fails, easier succeeds" under each ordering? → Quantify the benefit of correct sequencing.
