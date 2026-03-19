# Diaflow Workspace and Settings Reference

Complete reference for workspace management, teams, billing, settings, API keys, integrations, and community features.

---

## Workspace

A workspace is the centralized environment for all your Diaflow resources. One workspace is automatically provisioned when you create your account.

### Shared Resources
All team members in a workspace share access to:
- Files (Drive)
- Database tables
- Vectors
- Third-party API configurations
- Credentials and integrations

### Key Constraints
- No simultaneous editing of the same flow by multiple users
- Only one workspace can be active at a time
- Switch workspaces via Settings > Change option

---

## Teams

Manage team members and their access levels within a workspace.

### Inviting Members
- Invite by email with an assigned role
- Roles: Owner, Admin, Member, Viewer

### Member Management
- Edit member name, email, or role
- Delete members from the workspace
- View last login information

---

## Billing and Subscription

### Overview
- Monitor credit usage and plan details
- Manage payment methods
- View invoices

### Credits
- Credits reset monthly with your plan
- Purchasable credit packages: 4,000 to 1,200,000 credits
- Purchased credits start burning when monthly plan credits reach zero

### Plan Changes
| Action | When It Takes Effect |
|--------|---------------------|
| Upgrade | Immediately |
| Downgrade | After current plan expires |
| Cancel | Downgrades to Basic plan, no refunds |

---

## Settings

### Personal Settings
- **Account information:** View and update name, email, avatar
- **Password:** Change password (validate current, enter new)
- **Delete account:** Permanently delete account and all workspace data

### Workspace Settings
- **Workspace name:** Display name for the workspace
- **Logo:** Workspace logo image
- **Favicon:** Browser tab icon
- **Slug OR Custom Domain:** Choose one (mutually exclusive, must be globally unique)

### Custom Domain Setup
Only available to workspace Owners. Available with Pro and Business plans.

**Setup Steps:**
1. Select your custom domain
2. Add TXT record to verify domain ownership
3. Configure CNAME or ANAME DNS record
4. Run domain check (verification may take up to 30 minutes)

### Language Settings
Supported languages:
- English (default)
- German
- French
- Spanish
- Japanese
- Vietnamese

Note: Some dynamic fields and system content remain in English regardless of language setting.

---

## API Keys

Manage API keys used for webhook automation nodes.

### Actions
- Create new API keys
- View existing keys
- Delete keys

### Key Information Displayed
| Field | Description |
|-------|-------------|
| Name | Descriptive name for the key |
| Key | The API key value |
| Created date | When the key was created |
| Last usage | Most recent use timestamp |
| Total usage | Cumulative usage count |

---

## Integrations

Store third-party API credentials at the workspace level for use across all flows.

### Management
- Add new integrations from the available list
- Search integrations by name
- Enter credentials specific to each integration (API keys, OAuth tokens, etc.)
- Credentials are available to all flows in the workspace

---

## Community

Global marketplace for discovering and sharing pre-built flow templates. All submissions are reviewed by the Diaflow Admin Team.

### Community Profile
Create via Account > My community profile.

| Field | Details |
|-------|---------|
| Avatar | Profile image |
| Name | Display name |
| Username | Permanent (cannot be changed after creation) |
| Description | Profile bio |
| Email | Contact email |
| Phone | Contact phone |
| Social links | External profile links |

Must agree to Community guidelines before publishing.

### Creating and Publishing Templates

**Steps:**
1. Create from Community Profile page or from the Workflow Builder
2. Configure: Name (max 60 characters), Categories, Description
3. Submit for review

**Review Status Flow:**
Waiting for review > In Review > Public (Approved) or Need change (Rejected)

### Managing Published Templates

**Visibility Options:**
| Visibility | Description |
|------------|-------------|
| Public | Visible to all community users |
| Private | Only visible to the creator |
| Unlisted | Accessible via direct link only |

**Important:** Any changes to a published template require re-approval through the review process.

### Finding and Using Templates
- Search by name, keywords, or creator
- Browse by category (Apps, Chat, Automation)
- Clone template to your workspace with one click
