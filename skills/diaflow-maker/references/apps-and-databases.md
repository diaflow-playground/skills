# Diaflow Apps and Database Integrations Reference

Complete reference for all app integrations and database connectors available in Diaflow.

---

## App Integrations (60+ Apps)

Apps are third-party services that connect to Diaflow flows as nodes. Credentials are configured in Workspace Integrations and shared across all flows in the workspace.

### Automation and Integration Tools
- **Python code** - Execute custom Python scripts within flows
- **Hunter.io** - Email finding and verification
- **SerpAPI** - Search engine results API
- **AWS** - Amazon Web Services integration
- **Exa** - AI-powered search API

### Social Media and Communication
- **Telegram** - Bot messaging and automation
- **YouTube** - Video data extraction and processing
- **Facebook Pages** - Page management and posting
- **WhatsApp Business** - Business messaging automation
- **Slack** - Workspace messaging and notifications
- **Microsoft Teams** - Team collaboration messaging
- **Discord Bot** - Bot-based Discord automation
- **Discord** - Discord platform integration
- **LinkedIn** - Professional network integration

### Email Marketing and CRM
- **Gmail** - Email sending and reading
- **Mailchimp** - Email marketing campaigns
- **Twilio SendGrid** - Transactional email delivery
- **Klaviyo** - E-commerce email marketing
- **HubSpot** - CRM and marketing automation
- **Salesforce** - Enterprise CRM
- **Intercom** - Customer messaging platform
- **Zendesk** - Customer support ticketing
- **Freshdesk** - Help desk and support

### Storage and Document Management
- **Google Drive** - Cloud file storage and sharing
- **Microsoft OneDrive** - Microsoft cloud storage
- **Google Docs** - Document creation and editing
- **Dropbox** - File hosting and sharing
- **Notion** - Workspace and knowledge management

### Spreadsheet and Database
- **Google Sheets** - Spreadsheet data operations
- **Airtable** - Database-spreadsheet hybrid
- **Asana** - Project management
- **Monday** - Work management platform

### Calendar and Scheduling
- **Google Calendar** - Event management
- **Microsoft Outlook Calendar** - Calendar scheduling
- **Google Meet** - Video meeting creation
- **Zoom** - Video conferencing management

### Accounting and Finance
- **Quickbook** - Accounting and invoicing
- **Xero Accounting** - Financial management

### CMS and Website
- **Wordpress.org** - Content management and publishing
- **SuiteDash** - Business management platform

### Analytics and Business Intelligence
- **Microsoft Power BI** - Business analytics dashboards
- **YouTube Analytics** - Channel performance metrics
- **YouTube Data** - Video and channel data API
- **LinkedIn Ads** - Advertising analytics
- **Google Ads** - Advertising campaign management

### Email and Productivity
- **Microsoft Outlook** - Email and calendar
- **Jira Service Desk** - IT service management

---

## Database Integrations

Direct database connections for querying, inserting, and updating data within flows.

### MySQL
- **Actions:** Query data, Add data, Update record
- **SQL Generation:** AI-assisted or Manual
- **Use case:** Read/write operations on MySQL databases

### PostgreSQL
- **Actions:** Query data, Add data
- **SQL Generation:** AI-assisted or Manual
- **Use case:** Read/write operations on PostgreSQL databases

### Microsoft SQL
- **Actions:** Query data, Add data, Update record
- **SQL Generation:** AI-assisted or Manual
- **Use case:** Read/write operations on MS SQL Server databases

### Snowflake
- **Actions:** Query data, Add data
- **SQL Generation:** AI-assisted or Manual
- **Use case:** Data warehouse querying and ingestion

### Common Database Parameters

All database integrations share these configuration options:

| Parameter | Description |
|-----------|-------------|
| Select resource | Choose from configured database connections in Integrations |
| Table | Target database table |
| Action | Query data, Add data, or Update record (varies by DB) |
| SQL Generate Method | AI-assisted (describe in natural language) or Manual (write SQL) |
| Input / Code editor | Natural language query (AI mode) or SQL statement (Manual mode) |

Database credentials are stored in Workspace Integrations and are available to all flows in the workspace.
