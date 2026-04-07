# Mixed Strategy Calculation Reference

Full algebraic and graphical methods for computing Nash equilibrium mixing proportions.

---

## The Indifference Principle

The key insight: in a mixed strategy Nash equilibrium, each player's mixing proportions are chosen to make their **opponent** indifferent between their pure strategies. If your opponent strictly preferred one strategy over another against your mix, they would abandon mixing and play that pure strategy — and you should have responded differently. So equilibrium requires opponent indifference.

**Consequence:** Your equilibrium mix is determined by your opponent's payoffs. If your own payoffs change, your equilibrium mix is unaffected — only your opponent's mix changes.

---

## 2x2 Algebraic Method

**Setup:** Row player mixes strategy A (probability p) and strategy B (probability 1−p).

**Step 1:** Write the column player's expected payoff for each of their strategies as a function of p.

If column player's payoffs are (a, b) when column plays Left against row's A and B respectively, and (c, d) when column plays Right:
- Expected payoff from Left: a·p + b·(1−p)
- Expected payoff from Right: c·p + d·(1−p)

**Step 2:** Set the two expressions equal and solve for p.

a·p + b·(1−p) = c·p + d·(1−p)

**Step 3:** Verify p is between 0 and 1. If not, a pure strategy equilibrium exists (one strategy dominates).

**Step 4:** Repeat with column player's proportion y to find row player's equilibrium mix.

---

## Worked Example: Penalty Kick

Payoff table (kicker success percentages; goalie minimizes):

|  | Goalie: Left | Goalie: Right |
|---|---|---|
| **Kicker: Left** | 58 | 95 |
| **Kicker: Right** | 93 | 70 |

**Finding kicker's mix (p = proportion Left):**

Set goalie's worst-case equal. Goalie prefers to minimize kicker's success. When kicker uses proportion p of Left:
- If goalie plays Left: 58p + 93(1−p) = 93 − 35p
- If goalie plays Right: 95p + 70(1−p) = 70 + 25p

Set equal: 93 − 35p = 70 + 25p → 23 = 60p → **p = 23/60 ≈ 0.383**

Kicker: Left 38.3%, Right 61.7%. Equilibrium success rate: 93 − 35(0.383) = 79.6%

**Finding goalie's mix (y = proportion Left):**

When goalie uses proportion y of Left:
- If kicker plays Left: 58y + 95(1−y) = 95 − 37y
- If kicker plays Right: 93y + 70(1−y) = 70 + 23y

Set equal: 95 − 37y = 70 + 23y → 25 = 60y → **y = 25/60 ≈ 0.417**

Goalie: Left 41.7%, Right 58.3%. Kicker's success rate: 70 + 23(0.417) = 79.6%

**Von Neumann's minimax theorem:** The kicker's maximum of minima (79.6%) equals the goalie's minimum of maxima (79.6%). This equality is guaranteed for zero-sum games — compute the best mix for one player and you know the equilibrium value for both.

---

## 3x3 System of Equations

For three strategies per player, let row player mix with p (strategy 1), q (strategy 2), (1−p−q) (strategy 3).

**Step 1:** Write column player's expected payoff for each of their three strategies as a function of p and q.

**Step 2:** Set all three equal. This gives two independent equations (the third is implied by the first two plus the constraint p + q + (1−p−q) = 1).

**Step 3:** Solve the system for p and q. Check that p > 0, q > 0, (1−p−q) > 0.

**Example: Janken step game** (win with Paper = +5 steps, Scissors = +2, Rock = +1; losses are negatives):

Row player's payoff from each of column's strategies, expressed in terms of Takashi's p (Paper) and q (Scissors):

- Yuichi's Rock payoff: −5p + 1q + 0(1−p−q) = −5p + q
- Yuichi's Paper payoff: 0p − 2q + 5(1−p−q) = −5p − 7q + 5
- Yuichi's Scissors payoff: 2p + 0q − 1(1−p−q) = 3p + q − 1

Set Rock = Paper: −5p + q = −5p − 7q + 5 → 8q = 5 → q = 5/8

Set Rock = Scissors: −5p + q = 3p + q − 1 → −8p = −1 → p = 1/8

Therefore: p(Paper) = 1/8, p(Scissors) = 5/8, p(Rock) = 2/8

---

## Graphical Method (Minimax V-Shape)

For a 2x2 zero-sum game, plot the row player's success rate against their mixing proportion p (horizontal axis, 0 to 1).

**Two lines:** One showing success against column's Left pure strategy, one showing success against column's Right pure strategy.

- Line for column's Left: starts at payoff(row Right vs col Left) when p=0, ends at payoff(row Left vs col Left) when p=1. This line may rise or fall depending on payoff values.
- Line for column's Right: starts at payoff(row Right vs col Right) when p=0, ends at payoff(row Left vs col Right) when p=1.

**The goalie (column player) will always play the pure strategy that minimizes the kicker's success** — they choose the lower of the two lines at each p.

**The resulting envelope** (lower of the two lines at each p) forms an inverted-V. The kicker maximizes their guaranteed success by choosing p at the apex — where the two lines cross.

**The intersection point p = 0.383** gives success rate 79.6%.

**For the goalie's mix:** Draw the same plot from the goalie's perspective (y on horizontal axis). Two lines show kicker's success against goalie's Left vs. Right mixtures. The kicker always picks the higher line. The goalie minimizes by choosing y at the bottom of the V (where lines cross). This is y = 0.417, same success rate 79.6%.

---

## When Pure Strategy Equilibria Exist in Zero-Sum Games

Not all zero-sum games require mixing. If one strategy dominates all others for the row player, play it; the game is solved. More generally, if the row player's maximin (best of worst cases) equals the column player's minimax (worst of best cases) in pure strategies, a pure strategy equilibrium exists.

Example: If kicker success when going Left is 38 (vs goalie Left) and 65 (vs goalie Right), but Right gives 93 and 70 respectively — Right dominates Left for the kicker. No mixing needed; the kicker should always go Right.

The mixing method will confirm this: solving the indifference equation gives p < 0 or p > 1, indicating the pure strategy is optimal.
