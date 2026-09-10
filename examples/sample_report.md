# Compileq Compliance Scan Report

_Compileq — proprietary compliance triage software by Psylinks Security Private Limited (https://psylinkssecurity.com)_

_Generated 2026-09-10 · 5 files scanned · 21 rules evaluated · target markets: EU, US-CA, US_

> This is an automated triage scan, not a legal audit. Confidence scores indicate how reliable each finding is — treat anything under 0.5 as a lead to investigate, not a fact.

## Readiness by category

**Overall readiness: 71.8/100**

| Regulation | Readiness |
|---|---|
| GDPR | 31.8/100 |
| WCAG | 54.5/100 |
| PCI-DSS | 56.0/100 |
| COPPA | 58.4/100 |
| LGPD | 66.4/100 |
| PIPEDA | 79.0/100 |
| CCPA | 100.0/100 |
| EU_AI_Act | 100.0/100 |
| HIPAA | 100.0/100 |

## Findings (highest risk first)

### [83.2/100] Tracking script loads before consent
- **Regulation:** GDPR — Art. 6/7 - Lawful basis & conditions for consent
- **Location:** `global_privacy_gaps.js:2`
- **Snippet:** `gtag('config', 'UA-XXXXX-Y');`
- **Confidence:** 0.6
- **Estimated fine exposure:** $3,000–$12,000,000 (triage estimate, confidence-scaled from a $5,000–$20,000,000 statutory range)
- **Why it matched:** A tracking/analytics/ad script (Google Analytics, Meta Pixel, etc.) appears to load unconditionally rather than after a consent decision.

- **Suggested fix:** Gate the script load behind an explicit consent check (e.g. only call gtag/fbq/init after the user accepts a cookie/consent banner). Log the consent decision with a timestamp.


### [83.2/100] Tracking script loads before consent
- **Regulation:** GDPR — Art. 6/7 - Lawful basis & conditions for consent
- **Location:** `good_tracker.js:3`
- **Snippet:** `gtag('config', 'UA-XXXXX-Y');`
- **Confidence:** 0.3
- **Estimated fine exposure:** $1,500–$6,000,000 (triage estimate, confidence-scaled from a $5,000–$20,000,000 statutory range)
- **Why it matched:** A tracking/analytics/ad script (Google Analytics, Meta Pixel, etc.) appears to load unconditionally rather than after a consent decision.

- **Suggested fix:** Gate the script load behind an explicit consent check (e.g. only call gtag/fbq/init after the user accepts a cookie/consent banner). Log the consent decision with a timestamp.


### [83.2/100] Tracking script loads before consent
- **Regulation:** GDPR — Art. 6/7 - Lawful basis & conditions for consent
- **Location:** `bad_signup_form.html:5`
- **Snippet:** `gtag('config', 'UA-XXXXX-Y');`
- **Confidence:** 0.6
- **Estimated fine exposure:** $3,000–$12,000,000 (triage estimate, confidence-scaled from a $5,000–$20,000,000 statutory range)
- **Why it matched:** A tracking/analytics/ad script (Google Analytics, Meta Pixel, etc.) appears to load unconditionally rather than after a consent decision.

- **Suggested fix:** Gate the script load behind an explicit consent check (e.g. only call gtag/fbq/init after the user accepts a cookie/consent banner). Log the consent decision with a timestamp.


### [78.0/100] No data deletion / DSAR endpoint found
- **Regulation:** GDPR — Art. 17 - Right to erasure
- **Location:** `global_signup.py:1`
- **Snippet:** `def create_user(request):`
- **Confidence:** 0.4
- **Estimated fine exposure:** $4,000–$8,000,000 (triage estimate, confidence-scaled from a $10,000–$20,000,000 statutory range)
- **Why it matched:** No route or handler matching common "delete my data" / "export my data" patterns was found in the API layer.

- **Suggested fix:** Add an authenticated endpoint that deletes or anonymizes a user's personal data on request, and a corresponding data-export endpoint. Document the process in your privacy policy.


### [78.0/100] No data deletion / DSAR endpoint found
- **Regulation:** GDPR — Art. 17 - Right to erasure
- **Location:** `payment_handler.py:8`
- **Snippet:** `def create_user(request):`
- **Confidence:** 0.4
- **Estimated fine exposure:** $4,000–$8,000,000 (triage estimate, confidence-scaled from a $10,000–$20,000,000 statutory range)
- **Why it matched:** No route or handler matching common "delete my data" / "export my data" patterns was found in the API layer.

- **Suggested fix:** Add an authenticated endpoint that deletes or anonymizes a user's personal data on request, and a corresponding data-export endpoint. Document the process in your privacy policy.


### [52.8/100] Form input without associated label
- **Regulation:** WCAG — WCAG 1.3.1 / 3.3.2 - Info and Relationships / Labels or Instructions
- **Location:** `bad_signup_form.html:11`
- **Snippet:** `<input type="email" placeholder="Email">`
- **Confidence:** 0.5
- **Estimated fine exposure:** $0–$37,500 (triage estimate, confidence-scaled from a $0–$75,000 statutory range)
- **Why it matched:** An <input> element was found with no nearby <label> and no aria-label/aria-labelledby attribute.

- **Suggested fix:** Associate every input with a visible <label for="id"> or an aria-label/aria-labelledby attribute.


### [52.0/100] Plaintext storage of personal data field
- **Regulation:** GDPR — Art. 32 - Security of processing
- **Location:** `global_signup.py:3`
- **Snippet:** `date_of_birth = request.form["date_of_birth"]`
- **Confidence:** 0.35
- **Estimated fine exposure:** $3,500–$7,000,000 (triage estimate, confidence-scaled from a $10,000–$20,000,000 statutory range)
- **Why it matched:** A field name suggesting sensitive personal data (email, ssn, dob, passport, national_id) is written to storage/logs without an encryption or hashing call nearby.

- **Suggested fix:** Encrypt sensitive fields at rest (application-level or column-level encryption) and ensure they are never written to plaintext logs.


### [52.0/100] Plaintext storage of personal data field
- **Regulation:** GDPR — Art. 32 - Security of processing
- **Location:** `global_signup.py:4`
- **Snippet:** `db.save(email=email, date_of_birth=date_of_birth)`
- **Confidence:** 0.35
- **Estimated fine exposure:** $3,500–$7,000,000 (triage estimate, confidence-scaled from a $10,000–$20,000,000 statutory range)
- **Why it matched:** A field name suggesting sensitive personal data (email, ssn, dob, passport, national_id) is written to storage/logs without an encryption or hashing call nearby.

- **Suggested fix:** Encrypt sensitive fields at rest (application-level or column-level encryption) and ensure they are never written to plaintext logs.


### [52.0/100] Plaintext storage of personal data field
- **Regulation:** GDPR — Art. 32 - Security of processing
- **Location:** `payment_handler.py:10`
- **Snippet:** `ssn = request.form["ssn"]`
- **Confidence:** 0.35
- **Estimated fine exposure:** $3,500–$7,000,000 (triage estimate, confidence-scaled from a $10,000–$20,000,000 statutory range)
- **Why it matched:** A field name suggesting sensitive personal data (email, ssn, dob, passport, national_id) is written to storage/logs without an encryption or hashing call nearby.

- **Suggested fix:** Encrypt sensitive fields at rest (application-level or column-level encryption) and ensure they are never written to plaintext logs.


### [52.0/100] Plaintext storage of personal data field
- **Regulation:** GDPR — Art. 32 - Security of processing
- **Location:** `payment_handler.py:11`
- **Snippet:** `db.save(email=email, ssn=ssn)`
- **Confidence:** 0.35
- **Estimated fine exposure:** $3,500–$7,000,000 (triage estimate, confidence-scaled from a $10,000–$20,000,000 statutory range)
- **Why it matched:** A field name suggesting sensitive personal data (email, ssn, dob, passport, national_id) is written to storage/logs without an encryption or hashing call nearby.

- **Suggested fix:** Encrypt sensitive fields at rest (application-level or column-level encryption) and ensure they are never written to plaintext logs.


### [44.0/100] Card number pattern near a database/log write
- **Regulation:** PCI-DSS — PCI-DSS Req. 3 - Protect stored cardholder data
- **Location:** `payment_handler.py:2`
- **Snippet:** `card_number = request.form["card"]`
- **Confidence:** 0.4
- **Estimated fine exposure:** $2,000–$40,000 (triage estimate, confidence-scaled from a $5,000–$100,000 statutory range)
- **Why it matched:** A variable/field named like a card number (card_number, cc_number, pan, credit_card) appears near a database save or logging call. Cards should generally never touch your own storage — use a tokenized processor (Stripe, Braintree, etc.).

- **Suggested fix:** Never store or log raw PANs. Use a PCI-compliant tokenized payment processor and only ever handle the returned token / last-4 digits.


### [44.0/100] Card number pattern near a database/log write
- **Regulation:** PCI-DSS — PCI-DSS Req. 3 - Protect stored cardholder data
- **Location:** `payment_handler.py:4`
- **Snippet:** `db.save(card_number=card_number)`
- **Confidence:** 0.4
- **Estimated fine exposure:** $2,000–$40,000 (triage estimate, confidence-scaled from a $5,000–$100,000 statutory range)
- **Why it matched:** A variable/field named like a card number (card_number, cc_number, pan, credit_card) appears near a database save or logging call. Cards should generally never touch your own storage — use a tokenized processor (Stripe, Braintree, etc.).

- **Suggested fix:** Never store or log raw PANs. Use a PCI-compliant tokenized payment processor and only ever handle the returned token / last-4 digits.


### [44.0/100] Card data potentially written to application logs
- **Regulation:** PCI-DSS — PCI-DSS Req. 3.4 / 10 - Logging
- **Location:** `payment_handler.py:3`
- **Snippet:** `print(f"Processing card {card_number}")`
- **Confidence:** 0.5
- **Estimated fine exposure:** $2,500–$50,000 (triage estimate, confidence-scaled from a $5,000–$100,000 statutory range)
- **Why it matched:** A logging call (console.log, logger.info, print) appears on the same or adjacent line as a card-shaped variable.

- **Suggested fix:** Strip or mask card fields before logging. Never log CVV/CVC under any circumstance (it cannot be stored at all per PCI-DSS).


### [44.0/100] Image without alt text
- **Regulation:** WCAG — WCAG 1.1.1 - Non-text Content (Level A)
- **Location:** `bad_signup_form.html:9`
- **Snippet:** `<img src="/logo.png">`
- **Confidence:** 0.8
- **Estimated fine exposure:** $0–$60,000 (triage estimate, confidence-scaled from a $0–$75,000 statutory range)
- **Why it matched:** An <img> tag was found without an alt attribute.
- **Suggested fix:** Add a descriptive alt attribute (alt="") for decorative images, or a meaningful description for informative ones.


### [41.6/100] Age gate / birthdate collection without parental consent flow
- **Regulation:** COPPA — COPPA 16 CFR Part 312 - Parental consent requirement
- **Location:** `global_privacy_gaps.js:6`
- **Snippet:** `var dateOfBirth = request.body.dateOfBirth;`
- **Confidence:** 0.3
- **Estimated fine exposure:** $15,523–$15,523 (triage estimate, confidence-scaled from a $51,744–$51,744 statutory range)
- **Why it matched:** Code collects a date-of-birth or age field (common pattern for under-13 detection) with no nearby parental-consent handling, despite the product plausibly targeting or being accessible to children.

- **Suggested fix:** If the service is directed at or knowingly collects data from children under 13, implement verifiable parental consent before collecting personal information, per the FTC's COPPA Rule.


### [41.6/100] Age gate / birthdate collection without parental consent flow
- **Regulation:** COPPA — COPPA 16 CFR Part 312 - Parental consent requirement
- **Location:** `global_privacy_gaps.js:7`
- **Snippet:** `db.save({ dateOfBirth: dateOfBirth });`
- **Confidence:** 0.3
- **Estimated fine exposure:** $15,523–$15,523 (triage estimate, confidence-scaled from a $51,744–$51,744 statutory range)
- **Why it matched:** Code collects a date-of-birth or age field (common pattern for under-13 detection) with no nearby parental-consent handling, despite the product plausibly targeting or being accessible to children.

- **Suggested fix:** If the service is directed at or knowingly collects data from children under 13, implement verifiable parental consent before collecting personal information, per the FTC's COPPA Rule.


### [41.6/100] Age gate / birthdate collection without parental consent flow
- **Regulation:** COPPA — COPPA 16 CFR Part 312 - Parental consent requirement
- **Location:** `global_signup.py:3`
- **Snippet:** `date_of_birth = request.form["date_of_birth"]`
- **Confidence:** 0.3
- **Estimated fine exposure:** $15,523–$15,523 (triage estimate, confidence-scaled from a $51,744–$51,744 statutory range)
- **Why it matched:** Code collects a date-of-birth or age field (common pattern for under-13 detection) with no nearby parental-consent handling, despite the product plausibly targeting or being accessible to children.

- **Suggested fix:** If the service is directed at or knowingly collects data from children under 13, implement verifiable parental consent before collecting personal information, per the FTC's COPPA Rule.


### [41.6/100] Age gate / birthdate collection without parental consent flow
- **Regulation:** COPPA — COPPA 16 CFR Part 312 - Parental consent requirement
- **Location:** `global_signup.py:4`
- **Snippet:** `db.save(email=email, date_of_birth=date_of_birth)`
- **Confidence:** 0.3
- **Estimated fine exposure:** $15,523–$15,523 (triage estimate, confidence-scaled from a $51,744–$51,744 statutory range)
- **Why it matched:** Code collects a date-of-birth or age field (common pattern for under-13 detection) with no nearby parental-consent handling, despite the product plausibly targeting or being accessible to children.

- **Suggested fix:** If the service is directed at or knowingly collects data from children under 13, implement verifiable parental consent before collecting personal information, per the FTC's COPPA Rule.


### [39.6/100] Click handler on non-interactive element without keyboard support
- **Regulation:** WCAG — WCAG 2.1.1 - Keyboard (Level A)
- **Location:** `bad_signup_form.html:12`
- **Snippet:** `<div onclick="submitForm()">Submit</div>`
- **Confidence:** 0.55
- **Estimated fine exposure:** $0–$41,250 (triage estimate, confidence-scaled from a $0–$75,000 statutory range)
- **Why it matched:** An onClick/onclick handler was found on a <div> or <span> with no tabIndex or keyboard event handler nearby.

- **Suggested fix:** Use a native <button> instead, or add tabIndex="0", role="button", and an onKeyDown handler for Enter/Space.


### [33.6/100] Tracking script loads before consent (LGPD basis)
- **Regulation:** LGPD — LGPD Art. 7 - Requirements for processing personal data
- **Location:** `global_privacy_gaps.js:2`
- **Snippet:** `gtag('config', 'UA-XXXXX-Y');`
- **Confidence:** 0.5
- **Estimated fine exposure:** $800–$4,800,000 (triage estimate, confidence-scaled from a $1,600–$9,600,000 statutory range)
- **Why it matched:** A tracking/analytics/ad script loads unconditionally rather than after a consent or other lawful-basis decision, similar to the GDPR consent requirement but under Brazil's LGPD.

- **Suggested fix:** Establish and document one of LGPD's ten lawful bases (Art. 7) before processing, and gate non-essential tracking behind a consent decision where consent is the chosen basis.


### [33.6/100] Tracking script loads before consent (LGPD basis)
- **Regulation:** LGPD — LGPD Art. 7 - Requirements for processing personal data
- **Location:** `good_tracker.js:3`
- **Snippet:** `gtag('config', 'UA-XXXXX-Y');`
- **Confidence:** 0.25
- **Estimated fine exposure:** $400–$2,400,000 (triage estimate, confidence-scaled from a $1,600–$9,600,000 statutory range)
- **Why it matched:** A tracking/analytics/ad script loads unconditionally rather than after a consent or other lawful-basis decision, similar to the GDPR consent requirement but under Brazil's LGPD.

- **Suggested fix:** Establish and document one of LGPD's ten lawful bases (Art. 7) before processing, and gate non-essential tracking behind a consent decision where consent is the chosen basis.


### [33.6/100] Tracking script loads before consent (LGPD basis)
- **Regulation:** LGPD — LGPD Art. 7 - Requirements for processing personal data
- **Location:** `bad_signup_form.html:5`
- **Snippet:** `gtag('config', 'UA-XXXXX-Y');`
- **Confidence:** 0.5
- **Estimated fine exposure:** $800–$4,800,000 (triage estimate, confidence-scaled from a $1,600–$9,600,000 statutory range)
- **Why it matched:** A tracking/analytics/ad script loads unconditionally rather than after a consent or other lawful-basis decision, similar to the GDPR consent requirement but under Brazil's LGPD.

- **Suggested fix:** Establish and document one of LGPD's ten lawful bases (Art. 7) before processing, and gate non-essential tracking behind a consent decision where consent is the chosen basis.


### [33.6/100] No data deletion / data subject rights endpoint found
- **Regulation:** LGPD — LGPD Art. 18 - Rights of the data subject
- **Location:** `global_signup.py:1`
- **Snippet:** `def create_user(request):`
- **Confidence:** 0.4
- **Estimated fine exposure:** $640–$3,840,000 (triage estimate, confidence-scaled from a $1,600–$9,600,000 statutory range)
- **Why it matched:** No route or handler matching common "delete my data" / "access my data" patterns was found, despite user signup/registration code existing.

- **Suggested fix:** Provide a mechanism for data subjects (titulares) to confirm processing, access, correct, anonymize, or delete their data per Art. 18, and respond within statutory timelines.


### [33.6/100] No data deletion / data subject rights endpoint found
- **Regulation:** LGPD — LGPD Art. 18 - Rights of the data subject
- **Location:** `payment_handler.py:8`
- **Snippet:** `def create_user(request):`
- **Confidence:** 0.4
- **Estimated fine exposure:** $640–$3,840,000 (triage estimate, confidence-scaled from a $1,600–$9,600,000 statutory range)
- **Why it matched:** No route or handler matching common "delete my data" / "access my data" patterns was found, despite user signup/registration code existing.

- **Suggested fix:** Provide a mechanism for data subjects (titulares) to confirm processing, access, correct, anonymize, or delete their data per Art. 18, and respond within statutory timelines.


### [25.2/100] Personal data collected without identified purpose nearby
- **Regulation:** PIPEDA — PIPEDA Principle 4.2 - Identifying Purposes
- **Location:** `global_signup.py:1`
- **Snippet:** `def create_user(request):`
- **Confidence:** 0.3
- **Estimated fine exposure:** $0–$30,000 (triage estimate, confidence-scaled from a $0–$100,000 statutory range)
- **Why it matched:** A signup/registration handler collects personal data fields with no nearby reference to a stated purpose or privacy-policy link, which PIPEDA's Fair Information Principles require be identified at or before collection.

- **Suggested fix:** State the purpose for collecting each category of personal information at or before collection (e.g. in the form UI or an accompanying privacy notice), per PIPEDA Principle 4.2.


### [25.2/100] Personal data collected without identified purpose nearby
- **Regulation:** PIPEDA — PIPEDA Principle 4.2 - Identifying Purposes
- **Location:** `payment_handler.py:8`
- **Snippet:** `def create_user(request):`
- **Confidence:** 0.3
- **Estimated fine exposure:** $0–$30,000 (triage estimate, confidence-scaled from a $0–$100,000 statutory range)
- **Why it matched:** A signup/registration handler collects personal data fields with no nearby reference to a stated purpose or privacy-policy link, which PIPEDA's Fair Information Principles require be identified at or before collection.

- **Suggested fix:** State the purpose for collecting each category of personal information at or before collection (e.g. in the form UI or an accompanying privacy notice), per PIPEDA Principle 4.2.


### [16.8/100] No data deletion / withdrawal-of-consent endpoint found
- **Regulation:** PIPEDA — PIPEDA Principle 4.3.8 - Withdrawing consent
- **Location:** `global_signup.py:1`
- **Snippet:** `def create_user(request):`
- **Confidence:** 0.3
- **Estimated fine exposure:** $0–$30,000 (triage estimate, confidence-scaled from a $0–$100,000 statutory range)
- **Why it matched:** No route or handler matching common "delete my data" / "withdraw consent" patterns was found in the API layer.

- **Suggested fix:** Provide a way for individuals to withdraw consent and have their data deleted or anonymized, subject to legal/contractual restrictions, per PIPEDA Principle 4.3.8.


### [16.8/100] No data deletion / withdrawal-of-consent endpoint found
- **Regulation:** PIPEDA — PIPEDA Principle 4.3.8 - Withdrawing consent
- **Location:** `payment_handler.py:8`
- **Snippet:** `def create_user(request):`
- **Confidence:** 0.3
- **Estimated fine exposure:** $0–$30,000 (triage estimate, confidence-scaled from a $0–$100,000 statutory range)
- **Why it matched:** No route or handler matching common "delete my data" / "withdraw consent" patterns was found in the API layer.

- **Suggested fix:** Provide a way for individuals to withdraw consent and have their data deleted or anonymized, subject to legal/contractual restrictions, per PIPEDA Principle 4.3.8.


---

_Report generated by **Compileq**, built by **Psylinks Security Private Limited** (https://psylinkssecurity.com). Proprietary software — not for redistribution._