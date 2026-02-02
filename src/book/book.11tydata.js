// Book data - provides data to all templates in this folder
const fs = require('fs');
const path = require('path');

module.exports = function() {
  const bookDir = path.join(__dirname, '../../data/book');
  const chapters = [];
  
  const files = fs.readdirSync(bookDir)
    .filter(f => f.endsWith('.json'))
    .sort();
  
  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const slug = path.basename(file, '.json');
    const content = fs.readFileSync(path.join(bookDir, file), 'utf8');
    const data = JSON.parse(content);
    
    chapters.push({
      slug: slug,
      index: i,
      prevSlug: i > 0 ? path.basename(files[i-1], '.json') : null,
      nextSlug: i < files.length - 1 ? path.basename(files[i+1], '.json') : null,
      ...data
    });
  }
  
  return { bookChapters: chapters };
};
