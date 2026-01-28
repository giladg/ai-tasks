# Google OAuth App Verification Guide

This guide covers the steps needed to verify your app with Google OAuth and remove the "unverified app" warning.

## Overview

Since your app uses Gmail and Calendar APIs (restricted/sensitive scopes), you'll need to complete Google's OAuth verification process. This involves:

1. Creating required legal documents (Privacy Policy, Terms of Service)
2. Configuring OAuth consent screen properly
3. Verifying domain ownership
4. Submitting app for verification
5. Potentially undergoing security assessment

## Timeline

- **Standard verification**: 3-6 weeks
- **Sensitive/Restricted scopes** (Gmail, Calendar): Can take 4-8 weeks and may require security assessment

## Required Documents

### 1. Privacy Policy

Must include:
- What data you collect (Gmail emails, Calendar events)
- How you use the data (task extraction)
- How you store the data (encrypted tokens, task database)
- How long you retain data
- How users can delete their data
- Third-party services used (Google APIs, Gemini AI)
- Contact information

**Location**: Must be publicly accessible at a URL on your verified domain
**Suggested URL**: https://ai-tasks.app/privacy

### 2. Terms of Service

Must include:
- Service description
- User responsibilities
- Acceptable use policy
- Limitation of liability
- Account termination conditions
- Contact information

**Location**: Must be publicly accessible
**Suggested URL**: https://ai-tasks.app/terms

### 3. App Homepage

A public page describing your app.

**Location**: https://ai-tasks.app
**Should include**:
- What the app does
- How it works
- Screenshot/demo
- Link to sign up

## OAuth Consent Screen Configuration

In Google Cloud Console (https://console.cloud.google.com):

### 1. App Information

- **App name**: AI Task Manager
- **App logo**: Upload a logo (120x120px PNG/JPG)
- **User support email**: Your support email
- **App homepage**: https://ai-tasks.app
- **App privacy policy**: https://ai-tasks.app/privacy
- **App terms of service**: https://ai-tasks.app/terms

### 2. Authorized Domains

Add your verified domain:
- ai-tasks.app

### 3. Scopes

Currently using:
- `openid`
- `https://www.googleapis.com/auth/userinfo.email`
- `https://www.googleapis.com/auth/userinfo.profile`
- `https://www.googleapis.com/auth/gmail.readonly` (RESTRICTED)
- `https://www.googleapis.com/auth/calendar.readonly` (RESTRICTED)

You'll need to justify why each restricted scope is necessary.

### 4. Test Users

Before verification, add test users who can bypass the "unverified" warning:
- Add your email and any beta testers

## Domain Verification

1. Go to Google Search Console: https://search.google.com/search-console
2. Add property: ai-tasks.app
3. Verify ownership via DNS TXT record or HTML file upload
4. Return to OAuth consent screen and add verified domain

## Verification Submission Requirements

### For Restricted Scopes (Gmail, Calendar):

1. **Scope Justification Video**
   - Record a screen recording (< 5 minutes)
   - Show OAuth flow from start to finish
   - Demonstrate how you use each scope
   - Show where/how data is displayed to users
   - Show how users can delete their data
   - Upload to YouTube (unlisted)

2. **Written Justification**
   - Explain why you need gmail.readonly
   - Explain why you need calendar.readonly
   - Describe what happens without these scopes
   - Maximum 1000 characters per scope

3. **Security Assessment** (may be required)
   - Letter of Assessment from approved assessor
   - Or complete CASA (Cloud Application Security Assessment)
   - Required for apps with > 100,000 users or handling sensitive data

## Submission Process

1. In Google Cloud Console → OAuth consent screen
2. Click "Prepare for verification"
3. Fill out all required information
4. Provide links to privacy policy, terms, homepage
5. Upload scope justification video
6. Write scope justifications
7. Submit for review

## During Review

- Google may request additional information
- Respond promptly to verification team emails
- Average review time: 4-6 weeks for restricted scopes
- May require multiple rounds of feedback

## After Verification

Once approved:
- "Unverified app" warning will be removed
- All users can authorize without warnings
- Your app will show as "Verified by Google"
- No more test user limitations

## Development Mode

**While waiting for verification**, you can:
- Keep app in "Testing" mode
- Add up to 100 test users
- Test users won't see unverified warning
- Request users to accept "unverified app" warning if urgent

## Common Rejection Reasons

1. **Incomplete privacy policy** - Must cover all data collection
2. **Poor scope justification** - Be specific about necessity
3. **Domain not verified** - Complete domain verification first
4. **Video quality issues** - Make sure video clearly shows OAuth flow
5. **Scope creep** - Only request scopes you actually use
6. **Non-functional URLs** - All links must work and be on verified domain

## Checklist Before Submission

- [ ] Domain verified in Google Search Console
- [ ] Privacy policy published at verified domain
- [ ] Terms of service published at verified domain
- [ ] App homepage is public and descriptive
- [ ] OAuth consent screen fully configured
- [ ] App logo uploaded (120x120px)
- [ ] All URLs use verified domain
- [ ] Screen recording video created and uploaded to YouTube
- [ ] Scope justifications written (< 1000 chars each)
- [ ] Test users added for beta testing
- [ ] Support email configured and monitored
- [ ] App functioning correctly in production

## Useful Links

- OAuth Consent Screen: https://console.cloud.google.com/apis/credentials/consent
- Domain Verification: https://search.google.com/search-console
- API Scopes: https://developers.google.com/identity/protocols/oauth2/scopes
- Verification Process: https://support.google.com/cloud/answer/9110914
- CASA Program: https://cloud.google.com/security/casa

## Contact

If you have questions during the verification process:
- Google OAuth Support: https://support.google.com/cloud/
- Response time: Usually 1-3 business days
