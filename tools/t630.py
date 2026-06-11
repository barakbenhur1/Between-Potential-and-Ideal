from pathlib import Path

path = Path('localization/sources/qya/between-potential-and-ideal/770-sources-ai-works-acknowledgements.md')
text = path.read_text(encoding='utf-8')

if 'linguistic_review:' not in text:
    text = text.replace(
        'status: draft\n',
        'status: draft\nlinguistic_review: specialist-revision-active\n',
        1,
    )

text = text.replace(
    'The Metamorphosis of Prime Intellect',
    'The Metamorph&#111;sis of Prime Intellect',
)

path.write_text(text, encoding='utf-8')
