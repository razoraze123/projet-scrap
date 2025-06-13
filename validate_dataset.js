const fs = require('fs');
const readline = require('readline');

let filePath = process.argv[2] || 'data/dataset_with_selector.jsonl';
if (!fs.existsSync(filePath)) {
  const altPath = 'data/dataset_with_selector_multi.jsonl';
  if (fs.existsSync(altPath)) {
    filePath = altPath;
  } else {
    console.error('Dataset file not found.');
    console.error('Usage: node validate_dataset.js [path_to_dataset]');
    process.exit(1);
  }
}

async function validate(path) {
  const input = fs.createReadStream(path, { encoding: 'utf8' });
  const rl = readline.createInterface({ input, crlfDelay: Infinity });

  let count = 0;
  const samples = [];

  for await (const line of rl) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    count++;
    try {
      const obj = JSON.parse(trimmed);
      if (obj && typeof obj.html === 'string' && typeof obj.selector === 'string') {
        if (samples.length < 5) {
          samples.push(obj);
        } else {
          const j = Math.floor(Math.random() * count);
          if (j < 5) samples[j] = obj;
        }
      }
    } catch (err) {
      console.error(`Invalid JSON on line ${count}`);
    }
  }

  console.log(`Total lines: ${count}`);
  console.log('Exemples :');
  samples.forEach(s => console.log(JSON.stringify(s)));
}

validate(filePath).catch(err => {
  console.error('Error validating dataset:', err);
});
