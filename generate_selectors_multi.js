const fs = require('fs');
const readline = require('readline');
const { JSDOM } = require('jsdom');
const cssEscape = require('css.escape');

// Prepare global DOM APIs expected by css-selector-generator
const domForGlobals = new JSDOM('');
const win = domForGlobals.window;
['Node','NodeList','Element','HTMLElement','HTMLDocument','DocumentFragment','HTMLCollection'].forEach(name => {
  if (win[name]) global[name] = win[name];
});
// Minimal polyfill for CSS.escape
global.CSS = { escape: cssEscape };
// Expose document and self for libraries that expect browser globals
global.document = win.document;
global.self = win;

const { getCssSelector } = require('css-selector-generator');

const inputPath = 'data/dataset_clean.jsonl';
const outputPath = 'data/dataset_with_selector_multi.jsonl';

async function generateSelectors() {
  const input = fs.createReadStream(inputPath, { encoding: 'utf8' });
  const output = fs.createWriteStream(outputPath, { encoding: 'utf8' });
  const rl = readline.createInterface({ input, crlfDelay: Infinity });

  let count = 0;
  for await (const line of rl) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    try {
      const obj = JSON.parse(trimmed);
      const html = obj.html;
      const dom = new JSDOM(html);
      const body = dom.window.document.body;
      for (const child of body.children) {
        const selector = getCssSelector(child);
        output.write(JSON.stringify({ html: child.outerHTML, selector }) + '\n');
        count++;
      }
    } catch (err) {
      console.error('Error processing line:', err.message);
    }
  }
  output.end(() => {
    console.log(`Total selectors generated: ${count}`);
  });
}

generateSelectors().catch(err => {
  console.error('Fatal error:', err);
});
