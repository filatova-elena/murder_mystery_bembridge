// Clue data - provides data to all templates in this folder
const fs = require('fs');
const path = require('path');

function loadCluesFromDir(dirPath, clueType) {
  const clues = [];
  if (!fs.existsSync(dirPath)) return clues;
  
  const files = fs.readdirSync(dirPath).filter(f => f.endsWith('.json'));
  for (const file of files) {
    const slug = path.basename(file, '.json');
    const content = fs.readFileSync(path.join(dirPath, file), 'utf8');
    const data = JSON.parse(content);
    clues.push({
      slug: slug,
      clueType: clueType,
      title: data.title || data.name,
      ...data
    });
  }
  return clues;
}

module.exports = function() {
  const dataDir = path.join(__dirname, '../../data');
  
  // Load clues (documents, botanicals, artifacts)
  const clues = [
    ...loadCluesFromDir(path.join(dataDir, 'documents'), 'document'),
    ...loadCluesFromDir(path.join(dataDir, 'botanicals'), 'botanical'),
    ...loadCluesFromDir(path.join(dataDir, 'artifacts'), 'artifact')
  ];
  
  // Load journals
  const journalsDir = path.join(dataDir, 'journals');
  const journals = [];
  if (fs.existsSync(journalsDir)) {
    const files = fs.readdirSync(journalsDir).filter(f => f.endsWith('.json'));
    for (const file of files) {
      const slug = path.basename(file, '.json');
      const content = fs.readFileSync(path.join(journalsDir, file), 'utf8');
      const data = JSON.parse(content);
      journals.push({
        slug: slug,
        title: data.title || slug.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()),
        ...data
      });
    }
  }
  
  return { clues: clues, journals: journals };
};
