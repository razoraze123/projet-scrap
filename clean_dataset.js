const fs = require('fs');
const readline = require('readline');

const inputPath = 'data/dataset.jsonl';
const outputPath = 'data/dataset_clean.jsonl';

async function cleanDataset() {
  const linesSeen = new Set();
  let totalLines = 0;
  let validLines = 0;
  let invalidLines = 0;

  const input = fs.createReadStream(inputPath, { encoding: 'utf8' });
  const output = fs.createWriteStream(outputPath, { encoding: 'utf8' });

  const rl = readline.createInterface({ input, crlfDelay: Infinity });

  for await (const line of rl) {
    const trimmed = line.trim();
    if (trimmed === '') {
      continue;
    }
    totalLines++;
    try {
      const obj = JSON.parse(trimmed);
      if (obj && typeof obj.html === 'string') {
        if (!linesSeen.has(obj.html)) {
          linesSeen.add(obj.html);
          output.write(JSON.stringify({ html: obj.html }) + '\n');
          validLines++;
        }
      } else {
        invalidLines++;
      }
    } catch (err) {
      invalidLines++;
    }
  }

  output.end();
  console.log(`Total lines: ${totalLines}`);
  console.log(`Valid unique lines written: ${validLines}`);
  console.log(`Invalid lines ignored: ${invalidLines}`);
}

cleanDataset().catch(err => {
  console.error('Error cleaning dataset:', err);
});
