# Diaflow Productivity Tools Reference

Complete reference for Tables, Drive, Vectors, and Pages productivity features.

---

## Tables

Create and manage structured database tables within your Diaflow workspace.

### Creating Tables
- **Blank template:** Start with an empty table
- **CSV import:** Upload a CSV file to populate the table
- **Sample data:** Use pre-built sample data as a starting point

### Column Types

| Type | Description |
|------|-------------|
| Single line text | Short text field |
| Long text | Multi-line text field |
| Checkbox | Boolean true/false |
| Multiple select | Choose multiple options from a list |
| Single select | Choose one option from a list |
| Date | Date value |
| Duration | Time duration |
| Number | Numeric value |
| Currency | Monetary value |
| Rating | Star rating |
| Created time | Auto-populated creation timestamp |
| Last modified time | Auto-populated modification timestamp |

### Table Operations
- **Filtering:** Select a field and apply an operator to filter rows
- **Sorting:** Sort by any column in ascending or descending order
- **Field visibility:** Toggle columns visible or hidden in the view

### Table Actions
- View record count
- Refresh data
- Download as CSV
- Share table to workspace members

### Tables Assistant
Chat with the Diaflow Tables Assistant to query and retrieve information from your tables using natural language.

---

## Drive

Centralized file storage accessible by all flows in the workspace.

### Views
- **Grid view:** Thumbnail-based file display
- **List view:** Detailed list with metadata

### File Management
- **Create Folder:** Organize files into folders
- **Upload:** Add files to Drive
- **Sort by:** Name, Size, Date, Folder first

### File Actions
| Action | Description |
|--------|-------------|
| Copy ID | Copy the file's unique identifier |
| Rename | Change the file name |
| Add to Vector | Vectorize the file for AI semantic search |
| Move | Relocate to a different folder |
| Download | Download the file locally |
| Delete | Remove the file permanently |
| Open selection | Enter multi-select mode |
| Select all | Select all visible files |
| Clear selection | Deselect all files |

---

## Vectors

Store vectorized data for AI semantic search and knowledge base capabilities.

### Overview
Vector databases store files as numerical embeddings that enable semantic (meaning-based) search. Diaflow provides a central vector store accessible by AI Chat, Flow nodes, and Pages.

### Organization
- **Root:** Contains all uploaded files regardless of group
- **Groups:** Organized collections of related files
- Two views: Files view and Groups view

### Supported Upload Types

| Type | Details |
|------|---------|
| Documents | PDF, DOCX, TXT, MD, CSV, XLSX, XLS, JSON |
| Articles | Rich text content created directly in Diaflow |
| URLs | Static web page content (must include http:// or https://) |
| Sitemaps | Crawl entire website sitemaps for bulk URL ingestion |

### Size Limits
- Text documents: Maximum 300,000 words
- Tabular files: Maximum 2,000 rows
- File upload: Maximum 50MB per file

### Chunking Settings
Configured at upload time and cannot be changed after upload.

| Setting | Options | Default |
|---------|---------|---------|
| Method | Word, Letter, Sentence, Passage | - |
| Chunk Size | 0-4500 | 200 |
| Chunk Overlap | 0-4500 | 3 |

**Tip:** Use larger chunk sizes (400-500) for technical documentation. Use smaller chunk sizes (100-200) for conversational content.

### Processing Status
- **Processing:** File is being vectorized (typically 1-5 minutes)
- **Completed:** File is ready for search
- **Rejected:** File could not be processed

### Search
Perform semantic search across:
- All files (root level)
- Specific groups
- Individual files

### File Type Actions

| File Type | Available Actions |
|-----------|------------------|
| Documents | View Data, Download, Access, Add/Remove Group, Delete |
| Articles | Edit Article, View Data, Add/Remove Group, Delete |
| URLs | View Data, Reindex, Visit Link, Add/Remove Group, Delete |

### Bulk Operations
- Remove from Group (bulk)
- Reindex URLs (bulk)
- Delete (permanent, removes from all groups)

### Integration with AI Features
- **AI Chat Knowledge Base:** Select vector sources in Chat Config for knowledge-grounded conversations
- **Diaflow Vector Node:** Search or Add data to vectors within flows
- **Page Generation:** Generate documents using vector knowledge

### Frequently Asked Questions
- **Duplicate file names:** Uploading a file with the same name automatically overwrites the old data
- **Editing files:** No direct editing; delete and re-upload instead
- **Processing time:** Typically 1-5 minutes depending on file size
- **Chunking changes:** Chunking settings cannot be changed after upload; delete and re-upload with new settings
- **Workspace isolation:** Vectors are isolated per workspace; they are not shared across workspaces
- **Maintenance:** Published chatbots use cached vector data during system maintenance

---

## Pages (Diaflow Pages)

Document management system for creating, appending, and retrieving content within workflows.

### Actions

| Action | Description | Key Parameters |
|--------|-------------|---------------|
| Add to existing document | Append content to an existing Page | Page (select existing), Content (from node outputs) |
| Add to new document | Create a new Page with content | Title (document title), Content (from node outputs) |
| Retrieve data from document | Read content from an existing Page | Page (select existing) |

### Usage in Flows
Pages nodes accept content from upstream node outputs using @ references. This allows flows to dynamically create reports, append logs, or read stored documents as part of automated workflows.
