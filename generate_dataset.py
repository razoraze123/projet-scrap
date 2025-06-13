import json
import random
from pathlib import Path

DATA_PATH = Path('data') / 'dataset.jsonl'

TEMPLATES = [
    "<a href='https://example.com/{i}'>Link {i}</a>",
    "<div class='box{i}' id='div{i}'><p>Paragraph {i}</p></div>",
    "<span class='highlight{i}' data-id='{i}'>Span {i}</span>",
    "<img src='img{i}.png' alt='Image {i}'/>",
    "<button class='btn{i}'>Button {i}</button>",
    "<header class='header{i}'><h1>Header {i}</h1></header>",
    "<form id='form{i}' action='/submit{i}'><input name='field{i}'/><button>Send</button></form>",
    "<article id='article{i}'><h2>Heading {i}</h2><p>Body {i}</p></article>",
    "<nav id='nav{i}'><a href='/home{i}'>Home</a><a href='/about{i}'>About</a></nav>",
    "<table class='table{i}'><tr><td>Cell {i}a</td><td>Cell {i}b</td></tr></table>",
    "<section id='section{i}'><h3>Title {i}</h3><p>Section {i}</p></section>",
    "<footer class='footer{i}'><p>Footer {i}</p></footer>",
    "<ul id='list{i}'><li>Item {i}a</li><li>Item {i}b</li></ul>",
    "<video controls src='video{i}.mp4'></video>",
    "<audio controls src='audio{i}.mp3'></audio>",
    "<input type='text' id='input{i}' value='Value {i}'/>",
    "<progress value='{i}' max='100'></progress>",
    "<iframe src='frame{i}.html' title='Frame {i}'></iframe>",
    "<select id='select{i}'><option value='A{i}'>A{i}</option><option value='B{i}'>B{i}</option></select>",
    "<canvas id='canvas{i}' width='200' height='100'></canvas>",
]


def generate_html(i: int) -> str:
    template = random.choice(TEMPLATES)
    return template.format(i=i)


def main() -> None:
    DATA_PATH.parent.mkdir(exist_ok=True)
    existing = set()
    if DATA_PATH.exists():
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    html = obj.get('html')
                    if html:
                        existing.add(html)
                except json.JSONDecodeError:
                    continue
    start_index = len(existing)
    new_entries = []
    i = start_index
    while len(new_entries) < 1000:
        html = generate_html(i)
        if html not in existing:
            new_entries.append({'html': html})
            existing.add(html)
        i += 1
    with open(DATA_PATH, 'a', encoding='utf-8') as f:
        for entry in new_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
