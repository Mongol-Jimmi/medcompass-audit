# MedCompass Audit

A static sales site and fictional sample for a narrow Canadian MD school-list audit.

**Offer:** a cited, profile-specific screen of 12 Canadian medical schools for Ontario applicants. Founding pilot price: CAD $79.

## Why this exists

Canadian schools calculate GPA, use MCAT scores, and define residency pools differently. The audit turns one applicant profile into a ranked planning screen with explicit caveats and official source links. It is a decision aid—not an admission prediction or essay service.

## Local check

```bash
python3 -m unittest discover -s tests -v
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Privacy

The public site has no analytics, cookies, form endpoint, or applicant data. The sample applicant is fictional. Initial requests use email and explicitly tell visitors not to send sensitive documents before intake is confirmed.

## Independence

MedCompass is not affiliated with OMSAS, OUAC, AFMC, a university, or an admissions committee. Official program pages control.
