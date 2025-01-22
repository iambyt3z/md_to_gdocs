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

### 2. Usage

  - Step 1: Open a Google Colab project.
  - Step 2: Downlaod `md_to_gdocs.ipynb` from git repository.
  - Step 3: Open `md_to_gdocs.ipynb` in your colab project.
  - Step 4: Add your markdown text in `markdown_text` variable in the `cell 3`.
  - Step 5: Run the all of the cells.
  - Step 6: Complete authentication pop-up by google.
  - Step 7: After the complete script is run, the link to the file will be returned below, which can used to visit the google doc document.


