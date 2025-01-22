# Markdown to Google Docs Converter

A Python script that converts markdown meeting notes into properly formatted Google Documents while preserving hierarchical structure and special formatting elements.

## Features

- **Automatic Document Creation**: Generates Google Docs with single command
- **Heading Preservation**:
  - H1 → Heading 1 style
  - H2 → Heading 2 style 
  - H3 → Heading 3 style
- **Advanced Formatting**:
  - Nested bullet points with indentation
  - Interactive checkboxes (visual representation)
  - Colored @mentions with bold styling
  - Distinct footer formatting
- **Google Workspace Integration**: Secure OAuth2 authentication

## ⚙️ Setup Instructions

### 1. Prerequisites
- Google Colab account
- Google Cloud Project with:
  - Docs API enabled
  - OAuth consent screen configured
  - Desktop app credentials downloaded as `client_secret.json`

### 2. Installation
```bash
# Clone repository
git clone https://github.com/yourusername/markdown-to-google-docs.git
cd markdown-to-google-docs

# Install dependencies
pip install -r requirements.txt
```

### 3. Usage

