# Stakeholder Domain Concerns

Detailed concern categories for each of the 8 stakeholder domains used in business viability testing. For each domain: who typically holds authority, what they care about, specific concern signals to look for, and the right questions to ask in a preview session.

Source: INSPIRED, Ch. 56 (Testing Business Viability, pp.277-281)

---

## 1. Marketing

**Who holds authority:** Head of Marketing, VP Marketing, Product Marketing lead

**What marketing cares about:**
- Enabling sales through effective positioning and messaging
- Protecting and enhancing the company's brand and reputation
- Market competitiveness and differentiation
- Go-to-market channel effectiveness

**Specific concern signals:**
- Solution falls outside the company's established brand promise (the range of things customers expect from this company)
- Solution requires a different go-to-market channel than what currently exists (e.g., direct sales product sold through PLG/self-serve, or vice versa)
- Solution messaging conflicts with current product positioning or market segment strategy
- Solution could undermine differentiation by commoditizing a premium feature
- Solution requires marketing campaigns the company does not have budget or capability for

**Questions to ask in the preview session:**
- "Does this fit within the brand promise our customers expect from us?"
- "Would this require changes to our current go-to-market motion?"
- "Does this conflict with any current marketing programs or positioning commitments?"
- "Is there anything here that would be difficult to message or that could confuse existing customers?"

---

## 2. Sales

**Who holds authority:** VP Sales, Sales leadership, Head of Sales Engineering

**What sales cares about:**
- Channel capability — the sales force can only sell what it is equipped to sell
- Price point alignment — high-touch direct sales requires high-value price points to justify the cost of sale
- Skill and knowledge requirements — new product types may require sales skills the team does not have

**Specific concern signals:**
- Solution requires sales to explain a new paradigm or technology category the sales force is not trained on
- Solution is priced at a point incompatible with the existing sales model (e.g., low-ACV product requiring high-touch enterprise sales)
- Solution competes with or cannibalizes existing deals or product lines the sales force is currently selling
- Solution requires different buyer relationships (e.g., selling to engineering rather than business executives)
- Solution changes deal structure (e.g., introducing usage-based pricing when the sales team sells annual contracts)

**Questions to ask in the preview session:**
- "Can your sales force sell this with the skills and relationships they currently have?"
- "Is the price point compatible with your sales motion?"
- "Does this create any conflict with deals you are currently working?"
- "What would you need to train your team to sell this effectively?"

---

## 3. Customer Success

**Who holds authority:** Head of Customer Success, VP Customer Success

**What customer success cares about:**
- Alignment between product complexity and the company's service model (high-touch vs. low-touch)
- Support burden — new features create new categories of customer questions and failure modes
- Onboarding scalability — can customers be successfully onboarded at current staffing levels?

**Specific concern signals:**
- Solution introduces a complex workflow that will generate high support volume
- Solution requires configuration or setup that customers cannot do without hand-holding
- Solution changes the onboarding model (e.g., self-serve product with a complex enterprise feature that requires human setup)
- Solution affects SLA commitments to existing customers
- New user segment (e.g., free-tier users) will need support at a volume the team cannot sustain

**Questions to ask in the preview session:**
- "Would this change the volume or nature of support requests you receive?"
- "Can customers be successfully onboarded without additional staffing?"
- "Is this consistent with our high-touch / low-touch service model?"
- "Are there any aspects of this that would be hard for customers to self-serve?"

**Note:** In companies with a high-touch service model, customer success teams are exceptionally helpful for product insights and prototype testing — they have deep knowledge of customer failure patterns.

---

## 4. Finance

**Who holds authority:** CFO, Head of Finance, Business Analytics

**What finance cares about:**
- Unit economics — can the company afford to build, sell, and operate the product at scale?
- Pricing model viability — does the pricing generate sufficient gross margin?
- Provisioning costs — infrastructure, licensing, or operational costs per unit
- Reporting and compliance — does the solution affect financial reporting, investor relations, or financial controls?

**Specific concern signals:**
- Solution relies on a third-party service (e.g., LLM API, data provider) with uncertain or high per-unit costs
- Solution pricing does not generate sufficient margin to cover provisioning and support costs
- Solution introduces a new pricing model (usage-based, freemium, consumption) that requires finance modeling
- Solution creates a new product line that changes revenue recognition accounting
- Investor relations concern — solution affects metrics investors track or creates financial disclosure requirements

**Questions to ask in the preview session:**
- "Can we model the unit economics together? What assumptions should we use for provisioning costs?"
- "At what scale does this become profitable, and is that realistic?"
- "Are there any financial reporting or compliance implications I should be aware of?"
- "Is the pricing model compatible with how we recognize revenue?"

---

## 5. Legal

**Who holds authority:** General Counsel, Legal team, Compliance team

**What legal cares about:**
- Privacy — data collection, storage, and transmission practices that create regulatory exposure
- Regulatory compliance — industry-specific regulations (GDPR, HIPAA, CCPA, SOC 2, PCI-DSS, etc.)
- Intellectual property — use of third-party IP, open source license compliance, patent exposure
- Competitive constraints — existing agreements that limit competitive positioning or market entry
- Contractual obligations — commitments to enterprise customers in existing contracts

**Specific concern signals:**
- Solution collects or processes personal data in new ways
- Solution transmits user data to third parties (APIs, analytics, LLMs)
- Solution enters a regulated industry segment (healthcare, finance, government)
- Solution uses open source components with restrictive licenses
- Solution could be construed as competing with a strategic partner protected by agreement

**Questions to ask in the preview session:**
- "Are there any privacy concerns with how this solution handles user data?"
- "Does this create any regulatory compliance requirements I should understand?"
- "Are there any IP constraints with the technology or content we are proposing to use?"
- "Are there existing customer contracts that this could violate?"
- "What specific language, screens, or data flows should I make sure are reviewed before we build?"

**Practical note:** Legal needs to see the actual proposed screens, wording, and data flows — not a description. Presentations are too abstract for legal review.

---

## 6. Business Development

**Who holds authority:** VP Business Development, Head of Partnerships, Strategic Alliances lead

**What business development cares about:**
- Existing partner agreements — contracts with commitments and constraints that the company must honor
- Partner alignment — whether the solution affects value delivered to or through key partners
- Competitive boundaries — whether the solution violates exclusivity or non-compete provisions in partner agreements

**Specific concern signals:**
- Solution integrates with or competes against a product covered by an existing partnership agreement
- Solution changes the data or value exchanged with a key distribution partner
- Solution enters a market segment covered by a partner exclusivity arrangement
- Solution changes API terms or access in ways that affect existing integration partners

**Questions to ask in the preview session:**
- "Are there any existing partner agreements that constrain what we can build here?"
- "Does this affect any of our key partner relationships?"
- "Are there commitments in existing contracts that we need to honor in the design?"

---

## 7. Security

**Who holds authority:** Chief Information Security Officer, Head of Security Engineering, Security Lead

**What security cares about:**
- Data protection — what new data the solution handles and how it is secured
- Access control — new permission boundaries or authentication requirements
- Attack surface — whether the solution introduces new vulnerability exposure
- Compliance with security standards — SOC 2, ISO 27001, penetration testing requirements

**Specific concern signals:**
- Solution stores or transmits sensitive user or enterprise data
- Solution introduces new API endpoints or integrations with external services
- Solution changes user authentication or authorization model
- Solution handles payment data, health data, or government-regulated data categories
- Solution is customer-facing infrastructure with new exposure to external attack

**Questions to ask in the preview session:**
- "What data will this solution handle, and does that create any security concerns?"
- "Does this change our authentication or access control model in any way?"
- "Are there security review requirements that we need to schedule before launch?"
- "Is there anything here that would require a penetration test or security audit?"

**Note:** Security is often considered part of the engineering organization rather than an independent stakeholder, but the issues are significant enough to warrant explicit, early engagement for any solution touching sensitive data or external exposure.

---

## 8. Executive (CEO/COO/GM)

**Who holds authority:** Chief Executive Officer, Chief Operating Officer, General Manager of the business unit

**What executives care about:**
- Overall business risk — whether the solution could harm the company's revenue, reputation, employees, or customers
- Strategic alignment — whether the solution fits the company's direction and priorities
- Trust in the product manager — whether the PM understands the business well enough to be trusted with this decision
- Cross-functional coordination — whether all relevant constraints have been identified and managed

**Specific concern signals:**
- PM has not engaged all relevant stakeholder domains before seeking executive sign-off
- Solution represents a significant strategic departure that has not been discussed at the leadership level
- Executive has unresolved concerns that subordinates have not been able to resolve
- Executive is unaware of the discovery approach and needs context on why they are being shown a prototype rather than a finished product

**Questions to ask in the preview session:**
- "Are there business risks in this direction that I should be thinking about?"
- "Does this align with where you want to take the company in this area?"
- "Are there constraints I may have missed in my stakeholder conversations?"
- "Are you comfortable with the approach we are taking, given what you have seen?"

**Critical note:** Executives assess product managers quickly. An executive will rapidly determine whether the PM has done the homework — understands the users, the market, the technology, and the business. If the PM demonstrates this competence, the executive gives latitude. If not, the executive attempts to control the product. The preview session is as much a credibility moment as a constraint-gathering exercise.
