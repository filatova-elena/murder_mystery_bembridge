// Character data - provides data to all templates in this folder
const fs = require('fs');
const path = require('path');

module.exports = function() {
  const characterDir = path.join(__dirname, '../../data/character');
  const skillsPath = path.join(__dirname, '../../data/skills.json');
  
  const characters = [];
  const files = fs.readdirSync(characterDir).filter(f => f.endsWith('.json'));
  
  for (const file of files) {
    const slug = path.basename(file, '.json');
    const content = fs.readFileSync(path.join(characterDir, file), 'utf8');
    const data = JSON.parse(content);
    
    characters.push({
      slug: slug,
      ...data
    });
  }
  
  // Also load skills
  const skills = JSON.parse(fs.readFileSync(skillsPath, 'utf8'));
  
  return { characters: characters, skills: skills };
};
