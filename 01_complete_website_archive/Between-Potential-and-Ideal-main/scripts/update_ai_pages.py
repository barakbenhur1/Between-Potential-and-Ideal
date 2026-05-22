#!/usr/bin/env python3
"""
Script to modify AI pages by hiding raw file lists and inserting structured card grids.
This script updates both Hebrew and English AI pages to improve UX by replacing
the simple file-dump list with a more structured and visually unified card grid.

Usage:
    python3 update_ai_pages.py

The script is idempotent and safe to run multiple times.
"""
import io
from pathlib import Path

# Base directory containing the theory-site-static pages
BASE_DIR = Path(__file__).resolve().parents[1] / 'theory-site-static'

def update_hebrew_ai(page_path: Path) -> None:
    """Update the Hebrew AI page with card grid layout."""
    content = page_path.read_text(encoding='utf-8')
    # Hide the raw file list
    content = content.replace('<ul class="file-list">', '<ul class="file-list" hidden>')
    # Define card grid HTML
    grid = (
        '<div class="ai-card-grid">'
        '  <div class="appendix-card">'
        '    <h3>טיורינג הפוך</h3>'
        '    <p>שיחה עם בינה מלאכותית הבוחנת האם מכונה יכולה לזהות אדם ולהפך.</p>'
        '    <div class="appendix-actions">'
        '      <a href="files/ai-believes/reverse-turing-conversation-he.docx" rel="noopener noreferrer" target="_blank">DOCX <span class="file-size">67.6 KB</span></a>'
        '      <a href="files/ai-believes/reverse-turing-conversation-he.html" rel="noopener noreferrer" target="_blank">HTML <span class="file-size">99.2 KB</span></a>'
        '      <a href="files/ai-believes/reverse-turing-conversation-he.md" rel="noopener noreferrer" target="_blank">MD <span class="file-size">58.4 KB</span></a>'
        '      <a href="files/ai-believes/reverse-turing-conversation-he.pdf" rel="noopener noreferrer" target="_blank">PDF <span class="file-size">72.0 KB</span></a>'
        '    </div>'
        '  </div>'
        '  <div class="appendix-card">'
        '    <h3>מה בינה מלאכותית מאמינה</h3>'
        '    <p>חקירה על אמונות ותפיסות של מודלים מלאכותיים דרך דיאלוג פילוסופי.</p>'
        '    <div class="appendix-actions">'
        '      <a href="files/ai-believes/what-ai-believes-he.docx" rel="noopener noreferrer" target="_blank">DOCX <span class="file-size">174.8 KB</span></a>'
        '      <a href="files/ai-believes/what-ai-believes-he.html" rel="noopener noreferrer" target="_blank">HTML <span class="file-size">527.0 KB</span></a>'
        '      <a href="files/ai-believes/what-ai-believes-he.md" rel="noopener noreferrer" target="_blank">MD <span class="file-size">373.4 KB</span></a>'
        '      <a href="files/ai-believes/what-ai-believes-he.pdf" rel="noopener noreferrer" target="_blank">PDF <span class="file-size">296.1 KB</span></a>'
        '    </div>'
        '  </div>'
        '  <div class="appendix-card">'
        '    <h3>כשאני גם אתה</h3>'
        '    <p>דיאלוג על זהות ומשמעות בין בינה מלאכותית לבין אדם: היכן מסתיימת האינדיבידואליות?</p>'
        '    <div class="appendix-actions">'
        '      <a href="files/ai-believes/when-i-am-also-you-he.docx" rel="noopener noreferrer" target="_blank">DOCX <span class="file-size">97.1 KB</span></a>'
        '      <a href="files/ai-believes/when-i-am-also-you-he.html" rel="noopener noreferrer" target="_blank">HTML <span class="file-size">221.3 KB</span></a>'
        '      <a href="files/ai-believes/when-i-am-also-you-he.md" rel="noopener noreferrer" target="_blank">MD <span class="file-size">144.8 KB</span></a>'
        '      <a href="files/ai-believes/when-i-am-also-you-he.pdf" rel="noopener noreferrer" target="_blank">PDF <span class="file-size">140.7 KB</span></a>'
        '    </div>'
        '  </div>'
        '</div>'
    )
    # Insert grid before closing section tag of the reader-card
    content = content.replace('</ul></section>', '</ul>' + grid + '</section>')
    page_path.write_text(content, encoding='utf-8')

def update_english_ai(page_path: Path) -> None:
    """Update the English AI page with card grid layout."""
    content = page_path.read_text(encoding='utf-8')
    content = content.replace('<ul class="file-list">', '<ul class="file-list" hidden>')
    grid = (
        '<div class="ai-card-grid">'
        '  <div class="appendix-card">'
        '    <h3>When I Am Also You</h3>'
        '    <p>A dialogue on identity and meaning between AI and human: where does individuality end?</p>'
        '    <div class="appendix-actions">'
        '      <a href="files/ai-believes/when-i-am-also-you-en.docx" rel="noopener noreferrer" target="_blank">DOCX <span class="file-size">92.5 KB</span></a>'
        '      <a href="files/ai-believes/when-i-am-also-you-en.html" rel="noopener noreferrer" target="_blank">HTML <span class="file-size">144.2 KB</span></a>'
        '      <a href="files/ai-believes/when-i-am-also-you-en.md" rel="noopener noreferrer" target="_blank">MD <span class="file-size">98.2 KB</span></a>'
        '      <a href="files/ai-believes/when-i-am-also-you-en.pdf" rel="noopener noreferrer" target="_blank">PDF <span class="file-size">128.7 KB</span></a>'
        '    </div>'
        '  </div>'
        '</div>'
    )
    content = content.replace('</ul></section>', '</ul>' + grid + '</section>')
    page_path.write_text(content, encoding='utf-8')

def main() -> None:
    hebrew_path = BASE_DIR / 'ai.html'
    english_path = BASE_DIR / 'ai-en.html'
    if hebrew_path.exists():
        update_hebrew_ai(hebrew_path)
    if english_path.exists():
        update_english_ai(english_path)

if __name__ == '__main__':
    main()