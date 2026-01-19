# ATS Landscape Overview

## What is an ATS?

An **Applicant Tracking System (ATS)** is software that companies use to:
- Post job listings
- Collect applications
- Screen candidates
- Manage hiring pipeline
- Comply with regulations

---

## Major ATS Systems

### Workday
**Market Position**: Enterprise leader
**Complexity**: High (4-7 pages)
**Account**: Required
**URL Pattern**: `*.myworkdayjobs.com`
**Characteristics**:
- Multi-step wizard
- Account/profile creation
- Resume parsing (often inaccurate)
- Many custom questions
- Enterprise features

### Greenhouse
**Market Position**: Tech company favorite
**Complexity**: Low (1-2 pages)
**Account**: Usually not required
**URL Pattern**: `boards.greenhouse.io`
**Characteristics**:
- Clean, modern UI
- Single-page forms common
- Custom questions vary
- EEOC questions optional

### Lever
**Market Position**: Startup popular
**Complexity**: Low (1 page)
**Account**: Not required
**URL Pattern**: `jobs.lever.co`
**Characteristics**:
- Very simple forms
- Minimal questions
- Quick applications

### Ashby
**Market Position**: Growing in tech
**Complexity**: Low (1 page)
**Account**: Not required
**URL Pattern**: `jobs.ashbyhq.com`
**Characteristics**:
- Modern UI
- Similar to Greenhouse
- Resume upload usually required

### Taleo (Oracle)
**Market Position**: Enterprise legacy
**Complexity**: Very High (5-10+ pages)
**Account**: Required
**URL Pattern**: `*.taleo.net`
**Characteristics**:
- Legacy UI
- Many pages
- Slow
- Complex account system

### iCIMS
**Market Position**: Mid-market
**Complexity**: Medium (2-4 pages)
**Account**: Sometimes required
**URL Pattern**: `careers-*.icims.com`
**Characteristics**:
- Variable complexity
- Modern versions exist
- Resume parsing

---

## ATS Screening

### How ATS Screens
1. **Keyword matching**: Looking for specific terms
2. **Experience parsing**: Extracting years of experience
3. **Education matching**: Degree requirements
4. **Location filtering**: Geographic requirements
5. **Knockout questions**: Must-have requirements

### Implications for Automation
- Resume should contain job-relevant keywords
- Format should be ATS-parseable
- Custom questions need appropriate answers
- Experience fields should match resume

---

## Detection Patterns

### Easy Apply vs. External
- **LinkedIn Easy Apply**: Handled within LinkedIn
- **External**: Redirects to company ATS

### Identifying ATS
1. Check URL pattern
2. Look for visual cues
3. Check page structure
4. May need snapshot analysis

---

## Strategy by ATS Type

### Simple ATS (Greenhouse, Lever, Ashby)
- Quick applications
- Few custom questions
- Resume upload key

### Complex ATS (Workday, Taleo)
- May need account creation
- Multi-page navigation
- More fields to fill
- More potential blockers

