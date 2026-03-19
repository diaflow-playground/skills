# Diaflow Built-in Tools Reference

All 25 built-in tools available in the Diaflow flow builder. Each tool is a node you can add to any flow.

---

## 1. Branch

Conditional decision point that routes data down different paths based on conditions.

**When to use:** When your flow needs to take different actions depending on data values (if/else logic).

**Key Parameters:**
- Only continue if: Select which condition branch to evaluate
- Condition: One of 21 condition types
- Form: The value or field to evaluate

**Condition Types (21 total):**
- Text: contains, matches, starts with, ends with, does not contain, does not match, does not start with, does not end with
- File format: checks file extension/type
- Numeric: equals, greater than, less than
- Temporal: equal to, after, before
- Boolean: true/false evaluation
- Existence: is empty, is not empty, exists, does not exist

---

## 2. Merge (Multiple Data Source to JSON)

Combines data from multiple upstream sources into a single unified JSON object.

**When to use:** When you need to consolidate outputs from several nodes into one JSON payload before passing to the next step.

**Key Parameters:**
- Input sources: Connect multiple node outputs as inputs
- Output: Single merged JSON object

---

## 3. Split Data (JSON Formatter)

Formats output data into well-structured JSON format.

**When to use:** When you need to restructure or reformat JSON data between nodes for cleaner downstream consumption.

**Key Parameters:**
- Input data: The JSON data to format
- Output: Well-structured JSON

---

## 4. Get Current Date and Time

Retrieves the current date, time, or day in configurable formats and timezones.

**Node ID pattern:** `date-time-{n}`

**When to use:** When your flow needs the current date/time for scheduling, logging, comparisons, or display.

**Key Parameters:**
| Parameter | Options |
|-----------|---------|
| Retrieval data | Day, Date, Time |
| Day format | Name (Monday-Sunday) or numeric (1-7) |
| Date format | MM/DD/YYYY, DD/MM/YYYY, YYYY/DD/MM, YYYY/MM/DD |
| Time format | 24-hour or 12-hour |
| Timezone | GMT -12 to GMT +12 |

---

## 5. Web Scraper

Collects and extracts information from any given URL.

**Node ID pattern:** `scraper-{n}`

**When to use:** When you need to extract content from a web page for processing in your flow.

**Key Parameters:**
- URL: The web page to scrape
- Content output format: HTML, Markdown, or Plaintext

**Advanced Configurations:**
- Caching: Enable/disable result caching
- Caching time: Duration to cache results

---

## 6. Document to Plain Text

Converts document files into plain text format.

**Node ID pattern:** `dtt-{n}`

**When to use:** When you need to extract readable text from PDF or other document formats for AI processing.

**Key Parameters:**
- Data: The document file to convert (PDF, etc.)

**Advanced Configurations:**
- Caching: Enable/disable result caching

---

## 7. Spreadsheet Analyzer

Runs SQL queries on CSV data for analysis and extraction.

**Node ID pattern:** `tbl-analyzer-{n}`

**When to use:** When you need to query, filter, aggregate, or analyze tabular/CSV data within a flow.

**Key Parameters:**
- Data: The CSV file or data source
- Action: The operation to perform
- SQL Generate Method: AI-assisted or Manual
- Input: Query description (for AI) or raw SQL (for Manual)

**Advanced Configurations:**
- Caching: Enable/disable result caching

---

## 8. Spreadsheet Creator

Converts structured JSON data into downloadable spreadsheet files.

**When to use:** When you need to generate a CSV, XLSX, or XLS file from JSON data.

**Key Parameters:**
- Input Data: Structured JSON to convert
- Format: CSV, XLSX, or XLS

---

## 9. Convert JSON to Chart Data

Transforms JSON data into visual chart representations.

**Node ID pattern:** `json-chart-{n}`

**When to use:** When you need to visualize data as charts in the flow output.

**Key Parameters:**
- Input: JSON data to chart
- Chart type: One of 13 types

**Supported Chart Types (13):**
Auto detect, Line, Multi-line, Bar, Stacked bar, Grouped bar, Column, Stacked column, Grouped column, Area, Stacked area, Pie, Donut

**Advanced Configurations:**
- Caching: Enable/disable result caching

---

## 10. PDF to Image

Converts PDF document pages into image format (JPEG or PNG).

**Node ID pattern:** `pdf-img-{n}`

**When to use:** When you need to convert PDF pages to images for vision AI analysis or display.

**Key Parameters:**
- Input: PDF file
- Pages per image: Number of PDF pages per output image (2 to n)

**Advanced Configurations:**
- Caching: Enable/disable result caching

---

## 11. Get Weather Information

Retrieves current, forecast, or historical weather data for a location.

**Node ID pattern:** `weather-{n}`

**When to use:** When your flow needs weather data for decisions, reports, or notifications.

**Key Parameters:**
| Parameter | Options |
|-----------|---------|
| Type | Current, Forecast, History |
| Input method | City name, Lat/Long, US Zipcode, IP address |
| Value | The location value based on input method |
| Day | 1-14 (for Forecast type only) |
| Start date | For History type (minimum 2010-01-01) |
| End date | For History type (maximum 30-day span from start) |

---

## 12. HTTP Request (API)

Connects with external APIs by sending HTTP requests.

**When to use:** When you need to call any external REST API, webhook, or web service.

**Key Parameters:**
- Method: GET, POST, PUT, PATCH, DELETE
- URL: The API endpoint
- Header: Key:Value pairs for request headers
- Parameters: URL query parameters
- Payload: Request body data

**Advanced Configurations - Failure Handling:**
| Option | Details |
|--------|---------|
| Stop flow | Halt execution on failure |
| Skip | Continue flow, ignore the error |
| Retry | Retry on failure: max 1-3 attempts, delay 1-5 seconds between retries |

---

## 13. Get GEO Location

Determines geographic location from an address or automatically detects it.

**Node ID pattern:** `geo-{n}`

**When to use:** When you need latitude/longitude coordinates or city names for location-based logic.

**Key Parameters:**
- Method: Auto-detect or Manual
- Value: Address or location input (for Manual method)
- Data to retrieve: Lat/Long or City name

---

## 14. SMTP

Sends automated emails via SMTP protocol.

**Node ID pattern:** `smtp-{n}`

**When to use:** When your flow needs to send email notifications, reports, or alerts.

**Key Parameters:**
- Credentials: SMTP server credentials
- To: Recipient email address(es)
- Cc: Carbon copy recipients
- Object: Email subject line
- Message: Email body content (supports rich text formatting)
- Attachments: Files to attach

---

## 15. Loop

For-each mechanism that processes array items sequentially.

**When to use:** When you need to iterate over a list/array and perform the same operation on each item.

**Important Limits:**
- Maximum 100 runs per session
- Branching nodes are NOT supported within loops

**Loop Over Items Node Parameters:**
- Input JSON: The array to iterate over
- Batch size: Number of items per iteration (default: 1)
- On Error: Skip the item or Stop the entire loop

**Loop Output Node Parameters:**
- Data to store: The result from each iteration to collect

---

## 16. Delay

Pauses workflow execution for a specified duration or until a specific time.

**When to use:** When you need to wait between steps (e.g., rate limiting, scheduling, timed sequences).

**Option A - Delay For (fixed duration):**
- Seconds: 5-60
- Minutes: 1-60
- Hours: 1-24

**Option B - Delay Until (specific time):**
- Date and time: Specific date/time to resume execution

---

## 17. File Converter

Converts files between different formats.

**When to use:** When you need to transform a file from one format to another within your flow.

**Key Parameters:**
- Original file: The file to convert
- Original format: Source file format
- Target format: Desired output format

**Supported Conversion Table:**

| Source Format | Target Formats |
|---------------|---------------|
| .txt | .docx, .pdf, .html, .md |
| .json | .xlsx, .md, .xml, .base64 |
| .html | .docx, .pdf, .txt, .xlsx, .csv, .jpg, .png, .json, .md, .xml, .base64 |
| .md | .docx, .pdf, .html |
| .csv | .pdf, .xlsx, .jpg, .png, .json, .html, .xml, .base64 |
| .jpeg/.jpg | .pdf |
| .png | .pdf |
| .pdf | .docx, .pptx, .txt, .xlsx, .jpg, .png, .webp, .html |
| .xlsx | .pdf, .csv, .jpg, .png, .json, .html, .xml, .base64 |
| .docx | .pdf, .txt, .jpg, .png, .html |

---

## 18. File Creator

Generates new files with specified content.

**When to use:** When you need to create a downloadable file from text or data within your flow.

**Key Parameters:**
- File Type: .docx, .pdf, .txt, .xlsx, .csv, .json, .html, .md
- File Name: Name without extension
- Content: Direct text entry or dynamic reference using @ notation

---

## 19. QR Code Generator

Converts URLs into QR code images.

**When to use:** When you need to generate a QR code for a link or URL.

**Key Parameters:**
| Parameter | Options |
|-----------|---------|
| Input URL | The URL to encode |
| Size | 128px, 256px, 512px, 1024px |
| Background color | Hex color code |
| Foreground color | Hex color code |
| Format | PNG or SVG |
| Output | Image file or Link URL |

---

## 20. Run Another Flow

Calls a sub-flow synchronously within the current flow.

**When to use:** When you want to reuse an existing flow as a modular component inside another flow.

**Key Parameters:**
- Select a flow: Choose the sub-flow to execute
- Field Input: Data to pass to the sub-flow
- On Error: Stop workflow or Skip

**Important Restrictions:**
- Only available for App type flows
- Sub-flows CANNOT use: Branch, Loop, Delay, or Run Another Flow nodes
- Parent and sub-flow execution are linked in history

---

## 21. Filter

Binary decision gate that either passes or blocks data based on conditions.

**When to use:** When you need a simple pass/fail gate (NOT branching). If the condition fails, the flow halts at the Filter node without an error.

**Key Differences from Branch:**
- Filter is a singular gate (pass or fail), not a branching mechanism
- If the condition is false, the flow simply stops at this node (no error thrown)
- Branch creates multiple paths; Filter only allows or blocks

**Key Parameters:**
- Rules: Condition rules using AND/OR groups
- Same 21+ condition types as Branch
- Preview tab: Test your filter conditions before running

---

## 22. Image Generation

Generates images from text prompts using AI models.

**When to use:** When your flow needs to create images from text descriptions.

**Key Parameters:**
- Model: Gemini 2.5 Flash Image or BytePlus Seedream 4.5
- Prompt: Text description of the desired image
- Image source: Optional reference image (.jpg or .png)
- Aspect ratio: 1:1, 4:3, 3:4, 16:9, 9:16, 21:9
- Number of images: 1 (Gemini) or 1-4 (BytePlus)

**Output:** Image URL(s)

---

## 23. Video Generation

Generates videos from text prompts and optional reference images using AI models.

**When to use:** When your flow needs to create short video clips from text descriptions.

**Key Parameters:**
- Model: BytePlus Seedance 1.0 Pro or BytePlus Seedance 1.5 Pro
- Prompt: Text description of the desired video
- Image source: Optional reference image
- Resolution: 720p to 1080p
- Aspect ratio: Various options
- Duration: 5 seconds or 12 seconds
- Audio: Available with 1.5 Pro model only
- Enhancement: Video quality enhancement option
- Compression: Video compression settings

**Important:** Video URLs expire in 24 hours. Download or process them promptly.

---

## 24. Diaflow Vision (Built-in Resource)

Analyzes images based on text prompts using AI vision capabilities.

**When to use:** When you need AI to analyze, describe, or extract information from images.

**Key Parameters:**
- Prompt: Instructions for image analysis
- Image Source: .jpg or .png file (PDFs require prior conversion)
- Max Token: Maximum response length

**Advanced Configurations:**
- Caching: Enable/disable result caching

---

## 25. Diaflow Pages (Built-in Resource)

Manages documents within workflows for content creation and retrieval.

**When to use:** When you need to create, append to, or read from Diaflow Pages documents.

**Key Parameters:**
- Action: Add to existing document, Add to new document, or Retrieve data from document
- Page: Select existing page (for "Add to existing" action)
- Title: Document title (for "Add to new document" action)
- Content: Content to add (from node outputs via @ references)
