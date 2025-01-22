import re
from typing import List, Dict
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.colab import auth
from oauth2client.client import GoogleCredentials

class GoogleDocsConverter:
    """Converts markdown content to formatted Google Docs"""
    
    def __init__(self):
        self.service = None
        self.requests: List[Dict] = []
        self.current_index = 1

    def authenticate(self) -> bool:
        """Initialize Google Docs API connection"""
        try:
            auth.authenticate_user()
            creds = GoogleCredentials.get_application_default()
            self.service = build('docs', 'v1', credentials=creds)
            return True
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            return False

    def create_document(self, title: str) -> str:
        """Create new Google Doc"""
        try:
            doc = self.service.documents().create(body={'title': title}).execute()
            return doc.get('documentId')
        except HttpError as e:
            print(f"Document creation error: {str(e)}")
            return None

    def _process_header(self, line: str) -> None:
        """Format markdown headers"""
        level = min(len(re.match(r'^#+', line).group()), 3)
        text = line.lstrip('#').strip()
        
        self.requests.extend([
            {
                'insertText': {
                    'location': {'index': self.current_index},
                    'text': f"{text}\n"
                }
            },
            {
                'updateParagraphStyle': {
                    'range': {
                        'startIndex': self.current_index,
                        'endIndex': self.current_index + len(text)
                    },
                    'paragraphStyle': {
                        'namedStyleType': f'HEADING_{level}'
                    },
                    'fields': 'namedStyleType'
                }
            }
        ])
        self.current_index += len(text) + 1

    def _process_list_item(self, line: str) -> None:
        """Handle bullet points and checkboxes"""
        indent_level = (len(line) - len(line.lstrip())) // 2
        text = line.strip().lstrip('*- ').strip()

        # Text insertion
        self.requests.append({
            'insertText': {
                'location': {'index': self.current_index},
                'text': f"{text}\n"
            }
        })

        # Bullet formatting
        self.requests.append({
            'createParagraphBullets': {
                'range': {
                    'startIndex': self.current_index,
                    'endIndex': self.current_index + len(text)
                },
                'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE'
            }
        })

        # Indentation
        if indent_level > 0:
            self.requests.append({
                'updateParagraphStyle': {
                    'range': {
                        'startIndex': self.current_index,
                        'endIndex': self.current_index + len(text)
                    },
                    'paragraphStyle': {
                        'indentStart': {
                            'magnitude': 36 * indent_level,
                            'unit': 'PT'
                        }
                    },
                    'fields': 'indentStart'
                }
            })

        # Checkboxes
        if re.match(r'\[[ x]\]', text):
            self.requests.append({
                'updateTextStyle': {
                    'range': {
                        'startIndex': self.current_index,
                        'endIndex': self.current_index + len(text)
                    },
                    'textStyle': {
                        'backgroundColor': {
                            'color': {
                                'rgbColor': {
                                    'red': 0.9,
                                    'green': 0.9,
                                    'blue': 0.9
                                }
                            }
                        }
                    },
                    'fields': 'backgroundColor'
                }
            })

        # Mentions
        for match in re.finditer(r'@(\w+)', text):
            start, end = match.span()
            self.requests.append({
                'updateTextStyle': {
                    'range': {
                        'startIndex': self.current_index + start,
                        'endIndex': self.current_index + end
                    },
                    'textStyle': {
                        'foregroundColor': {
                            'color': {
                                'rgbColor': {
                                    'red': 0.2,
                                    'green': 0.4,
                                    'blue': 0.8
                                }
                            }
                        },
                        'bold': True
                    },
                    'fields': 'foregroundColor,bold'
                }
            })

        self.current_index += len(text) + 1

    def convert_content(self, markdown_text: str, doc_id: str) -> bool:
        """Main conversion controller"""
        try:
            lines = markdown_text.split('\n')
            for line in lines:
                if line.startswith('#'):
                    self._process_header(line)
                elif line.strip().startswith(('*', '-')):
                    self._process_list_item(line)
                elif line.strip():
                    self._process_paragraph(line.strip())

            self.service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': self.requests}
            ).execute()
            return True
            
        except Exception as e:
            print(f"Conversion error: {str(e)}")
            return False
