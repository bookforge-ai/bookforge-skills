# Copyright and Legal Framework

BookForge is a non-commercial, open-source project that distills non-fiction books into agent skills. This document explains our legal posture, how we honor the rights of authors and publishers, and what to do if you are a rights holder who wants content removed.

If you are an author or rights holder looking for the removal path, see [TAKEDOWN.md](TAKEDOWN.md). One email is enough.

---

## Our posture

BookForge is non-commercial and fully open source. The skills library, the pipeline, and the landing page are free. There is no paid tier, no hosted service, no ads, no premium content, and no enterprise licensing. Skills are licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). The pipeline code is licensed under MIT.

Every skill includes mandatory attribution to the source book and its authors. Any author or rights holder can request removal of their book's skills with one email, honored within 48 hours, no lawyers required. We maintain a compliance log of every takedown and opt-out as an auditable good-faith record.

This posture is a commitment, not a marketing statement. If you are a rights holder, this document tells you what we do and how to reach us.

---

## Why we believe this is legal

BookForge's legal theory rests on a simple distinction that has been part of US copyright law for more than a century: **copyright protects expression, not ideas.**

**Primary legal basis: idea/expression dichotomy — 17 USC §102(b).**

Section 102(b) of the US Copyright Act states that copyright protection does not extend to "any idea, procedure, process, system, method of operation, concept, principle, or discovery, regardless of the form in which it is described, explained, illustrated, or embodied in such work." Methods, procedures, and systems are outside the scope of copyright protection.

BookForge extracts *methods*. A skill distilled from Chris Voss's *Never Split the Difference* encodes the calibrated-questions framework — a technique a negotiator can apply. It does not reproduce Voss's prose, his anecdotes, or his specific wording. The framework is a method, which §102(b) explicitly excludes from copyright protection. The way Voss *writes about* the framework is expression, which is protected. We use the first and do not reproduce the second.

This distinction is load-bearing for everything that follows. Skills are built around workflows, decision frameworks, and acceptance criteria — the excluded categories under §102(b). Books contain both methods and expression; we take only the methods.

**Secondary basis: fair use — 17 USC §107.**

Even for content that might be considered expression rather than method, the use BookForge makes of book content is likely protected by fair use. The four factors:

- **Purpose and character.** Skills are a highly transformative use. They convert book prose into executable agent instructions, changing both the form and the function of the original work. BookForge is non-commercial and educational, which strengthens this factor further.
- **Nature of the copyrighted work.** Published, factual, expository non-fiction receives thinner copyright protection than fictional or unpublished works. Every book in the library is in this category.
- **Amount and substantiality.** Skills take the framework, not the "heart of the work." We do not reproduce distinctive examples, case studies, or extended passages. Our pipeline enforces this with build-time checks (see the next section).
- **Effect on the potential market.** Skills are complements to the source books, not substitutes. A skill helps a reader apply a framework; it does not replace reading the book. If anything, we expect skills to drive book sales for curious users.

Fair use is a defense, not a guarantee, and we do not claim otherwise. We rely on it as a backup to §102(b), not as the primary theory.

We do not claim that BookForge is "definitely legal" or that any specific skill is immune from challenge. We claim that our practice is grounded in specific statutory and case-law principles, honored operationally, and subject to review at any author's request. That is the commitment.

---

## How we honor this in practice

A legal theory is only credible if it is reflected in how the work actually gets done. The following practices are enforced operationally, not just claimed on paper.

**Mandatory attribution.** Every skill in this repository has a `source-books:` entry in its frontmatter naming the book title, author(s), and ISBN. Attribution is enforced by our validator — a skill cannot ship without it. When you read a skill, you always know which book it came from and who wrote that book.

**No verbatim quoting.** Skills must paraphrase, never reproduce. Our pipeline includes a build-time check that greps for long n-gram overlap (eight or more consecutive words) between the draft skill and the source book text. Skills that exceed the threshold fail the build. This turns our "no verbatim reproduction" claim into a verifiable property, not an aspiration.

**No distinctive-example capture.** Books often illustrate methods with memorable examples — Voss's Haiti kidnapping story, Cialdini's Joe-the-car-salesman anecdote, the specific case studies in *Building Secure and Reliable Systems*. We take the method (calibrated questions, reciprocity, typed-builder patterns) without reproducing the story. Human review in our packaging stage catches cases where a draft skill gets too close to a distinctive example.

**Value-contribution testing.** Every skill is tested against a no-skill baseline by an independent evaluator. A skill only ships if it measurably changes agent behavior in a transformative way. A skill that just repeats the book would not clear this bar — the whole test is designed to reward genuine transformation.

**Sourcing provenance.** Every book processed by BookForge is legitimately acquired. We maintain internal records of source, acquisition date, and receipt location for each book in the library. We do not work from pirate sources.

**Good-faith compliance log.** Every takedown honored, every opt-out respected, and every author contacted is recorded privately. This log exists so our response history is auditable by anyone who asks, including future counsel.

None of these practices are trust-me claims. Each one is enforced either by a build-time check, a validator, a review stage, or a written record you can ask to see.

---

## If you are an author or rights holder

**You can opt out at any time, with one email.** We honor author opt-out requests within 48 hours of verification. No lawyers required, no statute citations needed, no argument. Send an email to the address in [TAKEDOWN.md](TAKEDOWN.md#contact) with the book title and your relationship to the work, and we will remove the content.

**You can also file a formal DMCA notice** if you prefer a paper trail. The full §512(c)(3) procedure is documented in [TAKEDOWN.md](TAKEDOWN.md#dmca-notice-17-usc-512c3).

**You are welcome to participate instead of opt out.** BookForge offers an author-verified badge program for authors who review their book's skills and confirm accuracy. Participating authors receive prominent credit and a verified badge on their skill set. Details in [TAKEDOWN.md](TAKEDOWN.md#author-verified-badge-program-for-authors-who-want-to-participate).

**We do not retaliate.** Exercising your rights as an author is not something we fight. We will not file penalty counter-claims against you for requesting removal of your own work.

---

## Trademark disclaimer

Book titles, author names, publisher names, and related marks are the trademarks and property of their respective owners. BookForge is not affiliated with, endorsed by, or sponsored by any of the authors, publishers, or rights holders whose books are featured in this library, unless explicitly stated through the author-verified badge program.

When BookForge references a book or author in marketing or documentation, it is for the purpose of identifying the source of extracted methods and honoring the required attribution. No claim of endorsement or affiliation is implied or intended.

---

## Jurisdictions outside the United States

BookForge is maintained from outside the United States by a non-US founder and distributes through GitHub (a US-hosted service). The legal analysis in this document is grounded in US copyright law, which is the governing law for content hosted on GitHub.

Readers in jurisdictions with stronger moral rights — particularly the European Union — should be aware that EU moral rights are inalienable and separate from the fair-use analysis above. If you are an author in an EU jurisdiction who objects to the use of your work on moral-rights grounds, please contact us at the email address in TAKEDOWN.md. We honor moral-rights objections through the same opt-out process as any other author request.

---

## Limits of this document

This document is informational and is not legal advice. It explains the posture and practice of a non-commercial open-source project. It is not a warranty that any specific use of BookForge skills is legal in any specific jurisdiction.

If you are considering using BookForge skills in a commercial context, or if you have a specific legal question about a specific skill or book, consult an attorney in your jurisdiction.

---

## Contact

- **For takedown and opt-out requests:** see [TAKEDOWN.md](TAKEDOWN.md)
- **For legal questions:** email the address listed in [TAKEDOWN.md contact section](TAKEDOWN.md#contact)
- **For general questions:** open an issue on this repository

---

## Related documents

- [TAKEDOWN.md](TAKEDOWN.md) — DMCA agent designation, opt-out path, counter-notice procedure
- [LICENSE](LICENSE) — CC BY-SA 4.0 license for BookForge skills
- [README.md](README.md) — project overview and library
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to contribute new skills

---

*Last updated: 2026-04-10. This document reflects BookForge's committed legal posture as of that date. It will be updated if the posture changes, if new books are added, or if an author or rights holder contacts us with a correction.*
