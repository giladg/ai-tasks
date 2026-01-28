# OAuth Verification Checklist

Use this checklist to prepare your app for Google OAuth verification.

## Before You Start

- [ ] App is deployed and publicly accessible at https://ai-tasks.app
- [ ] All features are working correctly in production
- [ ] You have a Google Cloud project with Gmail and Calendar APIs enabled

## 1. Deploy Legal Pages

- [ ] Deploy updated frontend with Privacy Policy and Terms pages
  ```bash
  cd /opt/ai-tasks
  git pull origin main
  cd frontend
  npm run build
  sudo cp -r dist/* /var/www/ai-tasks/
  ```

- [ ] Verify pages are accessible:
  - [ ] https://ai-tasks.app/privacy
  - [ ] https://ai-tasks.app/terms

- [ ] Review and customize the legal documents:
  - [ ] Replace `[YOUR SUPPORT EMAIL]` with actual support email
  - [ ] Replace `[YOUR BUSINESS ADDRESS]` with actual address (if applicable)
  - [ ] Replace `[YOUR SERVER LOCATION]` with actual server location
  - [ ] Review all content for accuracy

## 2. Domain Verification

- [ ] Go to https://search.google.com/search-console
- [ ] Click "Add Property"
- [ ] Enter domain: ai-tasks.app
- [ ] Choose verification method:
  - **DNS TXT Record** (recommended):
    - [ ] Add TXT record to your domain DNS
    - [ ] Wait for DNS propagation (up to 48 hours)
    - [ ] Click "Verify" in Search Console
  - **HTML File Upload**:
    - [ ] Download verification file
    - [ ] Upload to `/var/www/ai-tasks/` on your server
    - [ ] Verify file is accessible
    - [ ] Click "Verify" in Search Console
- [ ] Confirm domain is verified (green checkmark)

## 3. Configure OAuth Consent Screen

Go to https://console.cloud.google.com/apis/credentials/consent

### App Information

- [ ] **App name**: AI Task Manager (or your preferred name)
- [ ] **User support email**: your-email@gmail.com
- [ ] **App logo**: Upload 120x120px logo
  - Create a simple logo or use a placeholder
  - Must be square (120x120 pixels)
  - PNG or JPG format
- [ ] **App domain**:
  - Application home page: https://ai-tasks.app
  - Application privacy policy link: https://ai-tasks.app/privacy
  - Application terms of service link: https://ai-tasks.app/terms

### Authorized Domains

- [ ] Add: ai-tasks.app
  - Note: Must be verified in Search Console first
  - Do NOT include https:// or www

### Scopes

- [ ] Review scopes:
  - openid (Basic)
  - .../auth/userinfo.email (Basic)
  - .../auth/userinfo.profile (Basic)
  - .../auth/gmail.readonly (RESTRICTED - needs verification)
  - .../auth/calendar.readonly (RESTRICTED - needs verification)

- [ ] Click "Add or Remove Scopes"
- [ ] Ensure all required scopes are added
- [ ] Save

### Test Users (While in Testing Mode)

- [ ] Add your email as test user
- [ ] Add any beta testers (up to 100 users)
- [ ] Save

### Publishing Status

- [ ] Keep in "Testing" mode until verification is complete
- [ ] Do NOT publish yet

## 4. Create Verification Materials

### Screen Recording Video

- [ ] Record a video showing:
  1. Landing page (https://ai-tasks.app)
  2. Click "Get Started" or "Sign In with Google"
  3. Google OAuth consent screen appears
  4. Select Gmail and Calendar scopes
  5. Grant permissions
  6. Redirect to dashboard
  7. Show tasks extracted from Gmail/Calendar
  8. Show how to revoke access (Google Account Permissions)
  9. Show how to delete account/data (if implemented)

- [ ] Video requirements:
  - Length: Under 5 minutes
  - Format: MP4, MOV, or AVI
  - Resolution: At least 720p
  - Audio: Optional but recommended (explain what you're doing)
  - No background music
  - Clear demonstration of OAuth flow

- [ ] Upload video to YouTube:
  - [ ] Set visibility to "Unlisted" (not Private)
  - [ ] Title: "AI Task Manager OAuth Flow"
  - [ ] Copy URL for verification form

### Scope Justifications

Write justifications (max 1000 characters each):

- [ ] **gmail.readonly justification**:
  ```
  We request gmail.readonly to automatically extract actionable tasks from the user's
  email messages. Our AI analyzes email subject lines, body content, and sender information
  to identify tasks such as meeting requests, action items, deadlines, and follow-ups.
  This scope is essential because:

  1. Core Functionality: Task extraction from Gmail is the primary purpose of our application
  2. User Experience: Without this scope, users would need to manually enter all tasks
  3. Automation: We sync daily to catch new tasks automatically
  4. Read-Only: We only read emails, never modify or delete them
  5. Transient Processing: Email content is processed in real-time and not stored

  Users can see which emails generated which tasks in the dashboard. Users can revoke
  access at any time through Google Account Permissions.
  ```

- [ ] **calendar.readonly justification**:
  ```
  We request calendar.readonly to automatically extract tasks from the user's Google
  Calendar events. Our AI analyzes event titles, descriptions, locations, and times to
  identify actionable tasks and deadlines. This scope is essential because:

  1. Core Functionality: Task extraction from Calendar is a primary feature
  2. Context: Calendar events often contain task information (e.g., "Prepare presentation
     for Monday meeting")
  3. Due Dates: Event dates help prioritize tasks automatically
  4. Read-Only: We only read calendar events, never modify or delete them
  5. Transient Processing: Calendar data is processed in real-time and not stored

  Users can see which calendar events generated which tasks. Users can revoke access at
  any time through Google Account Permissions.
  ```

## 5. Submit for Verification

- [ ] In Google Cloud Console, go to OAuth consent screen
- [ ] Click "Prepare for Verification" or "Submit for Verification"
- [ ] Fill out verification form:
  - [ ] Paste YouTube video URL
  - [ ] Paste scope justifications
  - [ ] Confirm all information is accurate
  - [ ] Provide additional context if requested
- [ ] Submit

## 6. During Review Process

- [ ] Monitor the email associated with your Google Cloud account
- [ ] Respond promptly to any requests from Google verification team (usually within 48 hours)
- [ ] Common requests:
  - Additional video clarification
  - More detailed scope justifications
  - Proof of domain ownership
  - Security documentation
- [ ] Expected timeline: 4-8 weeks for restricted scopes

## 7. If Security Assessment is Required

Some apps may need CASA (Cloud Application Security Assessment):

- [ ] Check if required (Google will notify you)
- [ ] Choose an approved assessor from: https://cloud.google.com/security/casa
- [ ] Schedule assessment (may take 2-4 weeks)
- [ ] Provide assessor with:
  - Application architecture documentation
  - Security practices documentation
  - Access to test environment
- [ ] Submit Letter of Assessment to Google
- [ ] Note: This adds significant time and cost to verification

## 8. Alternative: Annual Security Self-Assessment

For apps with fewer users:

- [ ] Complete self-assessment questionnaire
- [ ] Document security practices:
  - Data encryption (at rest and in transit)
  - Access controls
  - Incident response procedures
  - Data retention policies
- [ ] Submit documentation to Google

## 9. After Approval

- [ ] Change publishing status from "Testing" to "In Production"
- [ ] Remove test user limitations
- [ ] Update OAuth consent screen if needed
- [ ] Monitor for any compliance issues
- [ ] Maintain verification by:
  - Keeping legal documents updated
  - Responding to policy changes
  - Renewing annually (if required)

## 10. If Rejected

- [ ] Read rejection reasons carefully
- [ ] Address each issue mentioned
- [ ] Common fixes:
  - Update privacy policy with more details
  - Improve scope justifications
  - Re-record video with better clarity
  - Verify domain ownership
  - Remove unnecessary scopes
- [ ] Resubmit after fixes
- [ ] Be patient - may take multiple rounds

## Temporary Solutions (While Waiting for Verification)

### Option 1: Testing Mode with Test Users

- [ ] Keep app in "Testing" mode
- [ ] Add users individually as test users (limit: 100)
- [ ] Test users won't see "unverified app" warning
- [ ] Good for: Small user base, beta testing

### Option 2: Accept "Unverified App" Warning

- [ ] Users will see warning screen
- [ ] Users must click "Advanced" then "Go to AI Task Manager (unsafe)"
- [ ] Good for: Tech-savvy users who understand the warning
- [ ] Not recommended for general public

## Important Notes

- **Timeline**: Plan for 2-3 months total (domain verification + OAuth review + potential assessment)
- **Cost**: Free for OAuth verification, but CASA assessment costs $15,000-$75,000
- **Maintenance**: Verification may need renewal annually
- **Scope Creep**: Only request scopes you actively use; removing scopes later is easy, adding requires re-verification
- **User Data**: Follow Google's Limited Use policy strictly
- **Communication**: Keep email address monitored; Google may request info any time

## Resources

- OAuth Consent Screen: https://console.cloud.google.com/apis/credentials/consent
- Domain Verification: https://search.google.com/search-console
- Verification Guide: https://support.google.com/cloud/answer/9110914
- User Data Policy: https://developers.google.com/terms/api-services-user-data-policy
- CASA Program: https://cloud.google.com/security/casa

## Contact

If you encounter issues:
- Google Cloud Support: https://support.google.com/cloud
- Community: https://stackoverflow.com/questions/tagged/google-oauth
