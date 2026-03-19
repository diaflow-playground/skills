# Diaflow AI Models Reference

Complete reference for all AI/LLM models and AI tools available in Diaflow.

---

## Private AI/LLM Models

Models hosted on Diaflow's servers. User data stays private and is not shared with third-party providers.

### 1. OpenAI

**Node ID pattern:** `openai/opa-{n}`

**GPT Text Models:**
- Series 5: GPT-5, GPT-5-mini, GPT-5-nano
- Series 4.1: GPT-4.1, GPT-4.1-mini, GPT-4.1-nano
- Series o: GPT-4o-mini, GPT-4o, GPT-o3-mini

Full chat capability with configurable prompt, memory, temperature, max length, Top P, presence/frequency penalties.

**GPT Vision:**
- Model: GPT-4o
- Purpose: Image analysis and understanding
- Supported formats: .jpg, .png

**DALL-E 3:**
- Purpose: Image generation from text descriptions
- Configurable: Quantity and size

**TTS / TTS-HD:**
- Purpose: Text-to-Speech conversion
- Models: TTS (standard), TTS-HD (high definition)
- Voices: Selectable from available voice options
- Output formats: MP3, OPUS, AAC, FLAC

**Whisper:**
- Purpose: Speech-to-text conversion
- Endpoints: Transcriptions or Translations
- Multi-language support

**Advanced Configurations (common to all OpenAI models):**
| Parameter | Range | Description |
|-----------|-------|-------------|
| Caching | On/Off | Cache responses for identical inputs |
| Memory (window size) | 0-5 or 0-1000 | Number of previous exchanges to remember |
| Temperature | 0-1 | Controls randomness (0 = deterministic, 1 = creative) |
| Max length | 0-3097 | Maximum output token length |
| Top P | 0-1 | Nucleus sampling threshold |
| Presence penalty | -2 to +2 | Penalizes repeated topics |
| Frequency penalty | -2 to +2 | Penalizes repeated tokens |

---

### 2. Anthropic

**Node ID pattern:** `an-{n}`

**Models:** Claude-4.5-sonet, Claude-4.5-opus, Claude-4.5-haiku

**Advanced Configurations:** Same as OpenAI (Caching, Memory, Temperature 0-1, Max length 0-3097, Top P, Presence/Frequency penalties)

---

### 3. Llama (Meta)

**Node ID pattern:** `an-{n}`

**Models:**
- Llama 4: Maverick (17B), Scout (17B)
- Llama 3.3: 70B
- Llama 3.2: 90B, 11B, 3B, 1B
- Llama 3.1: 70B, 8B
- Llama 3: 70B, 8B

---

### 4. Google Gemini

**Node ID pattern:** `gg-{n}`

**Models:** Gemini 2.5 Pro, Gemini 2.5 Flash, Gemini 2.0 Flash, Gemini 2.0 Flash-lite

---

### 5. BytePlus

**Node ID pattern:** `byteplus-{n}`

**Models:**
- DeepSeek V3.2 (text)
- Seed 1.6 (text)
- Seedream 4.5 (image generation, resolution up to 4K)
- Seedance 1.0 Pro (video generation, 5s/12s)
- Seedance 1.5 Pro (video generation, 5s/12s, audio support)

---

### 6. Cohere

**Node ID pattern:** `an-{n}`

**Models:** Command R+, Command R

---

### 7. MistralAI

**Node ID pattern:** `an-{n}`

**Models:** Mistral 7B, Mixtral 8x7B, Mistral Small (24.02), Mistral Large (24.02), Pixtral Large

---

## Common Configuration for All Private LLM Models

**Inputs:**
- From Data Loaders / Data source / Vector DB: Provides context to the model
- From Input: User query text (from trigger or upstream node)

**Key Parameters:**
- Model: Select the specific model variant
- Prompt: Instructions for the model (supports @ references to other node outputs)
- Image source: For vision-capable models

**Output:**
- To Output: Text string result

---

## Public AI/LLM Models (BYOK - Bring Your Own Key)

Users supply their own API credentials. Configure credentials in Workspace Integrations.

| # | Provider | Notable Details |
|---|----------|----------------|
| 1 | OpenAI Cloud | Full OpenAI API access |
| 2 | Perplexity Cloud | Search-augmented AI |
| 3 | BytePlus Cloud | BytePlus model access |
| 4 | Deepseek Cloud | Deepseek models |
| 5 | Anthropic Cloud | Claude models |
| 6 | Replicate | Open-source model hosting |
| 7 | Straico | Multi-model platform |
| 8 | OpenRouter | Multi-provider routing |
| 9 | Cohere Cloud | Cohere models |
| 10 | Google Gemini Cloud | Gemini models |
| 11 | MistralAI Cloud | Mistral models |
| 12 | ElevenLabs Cloud | TTS and STT with Stability and Similarity boost controls |
| 13 | Azure Cloud | Azure-hosted OpenAI models (GPT-3.5, GPT-4) |
| 14 | AWS Bedrock Cloud | Foundation models (Anthropic Claude, Amazon Titan, AI21, etc.) |

All BYOK providers share similar configuration: Credentials, Model selection, Prompt, Caching options.

---

## AI Tools (Built-in Capabilities)

Pre-built AI capabilities that do not require model selection. Each performs a specific task.

| Tool | Description |
|------|-------------|
| Text Generation from Image | Generate descriptive text from images |
| Audio Transcription | Convert audio (WAV/MP3) to text |
| Audio Translation | Translate audio content to another language |
| Image Generation | Generate images from text using DALL-E 3 |
| Entity Recognition from Text | Extract named entities (people, places, orgs) from text |
| Entity Recognition from Images | Extract named entities from image content |
| Image-to-Text Description | Generate detailed descriptions of images |
| Text Summarization | Condense long text into summaries |
| Text-to-Speech | Convert text to spoken audio |
| Data Classification | Classify text into predefined categories |

---

## Credit Calculations

Different AI operations consume credits based on different unit types.

| Unit Type | Applies to | Formula |
|-----------|-----------|---------|
| Token | AI/LLM text generation | (Input credits x Input tokens) + (Output credits x Output tokens) |
| Character | AI/LLM text nodes | Output Credits x Number of characters |
| Image | Image generation nodes | Output Credits x Number of images |
| Second | Time-based AI nodes (TTS, video) | Output Credits x Duration in seconds |
| Request | App category nodes | Output credit per run |

Nodes that do not consume credits are clearly indicated in the Component List popup as free to use.
