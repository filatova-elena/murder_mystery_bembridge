// Template script for character pages
// Replace CHARACTER_NAME with the actual character name

const characterName = 'CHARACTER_NAME';
setCharacter(characterName);

// Load character data and skills
Promise.all([
  fetch(`../data/character/${characterName}.json`).then(r => r.json()),
  fetch(`../data/skills.json`).then(r => r.json())
]).then(([character, skills]) => {
  // Set title and name
  document.getElementById('character-title').textContent = character.title;
  document.getElementById('character-name').textContent = character.title;

  // Set personality
  document.getElementById('personality').textContent = character.personality;

  // Set skills
  const skillsDiv = document.getElementById('skills');
  skillsDiv.innerHTML = '';
  
  // Expert skills
  if (character.skills.expert && character.skills.expert.length > 0) {
    const expertTitles = character.skills.expert.map(skill => skills[skill]?.title || skill).join(', ');
    const expertP = document.createElement('p');
    expertP.innerHTML = `<strong>⭐ Expert:</strong> ${expertTitles}`;
    skillsDiv.appendChild(expertP);
  }

  // Basic skills
  if (character.skills.basic && character.skills.basic.length > 0) {
    const basicTitles = character.skills.basic.map(skill => skills[skill]?.title || skill).join(', ');
    const basicP = document.createElement('p');
    basicP.innerHTML = `<strong>📖 Basic knowledge:</strong> ${basicTitles}`;
    skillsDiv.appendChild(basicP);
  }

  // Personal connections
  if (character.skills.personal && character.skills.personal.length > 0) {
    const personalTitles = character.skills.personal.map(skill => skills[skill]?.title || skill).join(', ');
    const personalP = document.createElement('p');
    personalP.innerHTML = `<strong>👥 Personal Connection:</strong> ${personalTitles}`;
    skillsDiv.appendChild(personalP);
  }

  // Set background (preserve original formatting)
  const backgroundDiv = document.getElementById('background');
  backgroundDiv.innerHTML = '';
  // Split by periods followed by space and capital letter (new sentence)
  const paragraphs = character.background.split(/(?<=\.)\s+(?=[A-Z])/).filter(p => p.trim());
  paragraphs.forEach(para => {
    const p = document.createElement('p');
    p.textContent = para.trim();
    backgroundDiv.appendChild(p);
  });

  // Set objectives
  const objectivesOl = document.getElementById('objectives');
  objectivesOl.innerHTML = '';
  const mainLi = document.createElement('li');
  mainLi.textContent = character.objectives.main;
  objectivesOl.appendChild(mainLi);
  const privateLi = document.createElement('li');
  privateLi.innerHTML = `<strong>Private (optional):</strong> ${character.objectives.private}`;
  objectivesOl.appendChild(privateLi);

  // Set strategy
  document.getElementById('strategy').textContent = character.strategy;

  // Set relationships
  const relationshipsDiv = document.getElementById('relationships');
  relationshipsDiv.innerHTML = '';
  Object.entries(character.relationships).forEach(([key, value]) => {
    const p = document.createElement('p');
    // Capitalize and format relationship key
    const title = key.charAt(0).toUpperCase() + key.slice(1).replace(/_/g, ' ');
    p.innerHTML = `<strong>The ${title}:</strong> ${value}`;
    relationshipsDiv.appendChild(p);
  });

  // Set starting items
  const startingItemsUl = document.getElementById('starting-items');
  startingItemsUl.innerHTML = '';
  if (character.starting_items && character.starting_items.length > 0) {
    character.starting_items.forEach(item => {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = item.link;
      a.textContent = item.name;
      li.appendChild(a);
      startingItemsUl.appendChild(li);
    });
  } else {
    startingItemsUl.innerHTML = '<li>None</li>';
  }
}).catch(error => {
  console.error('Error loading character data:', error);
  document.body.innerHTML = '<div class="container"><h1>Error loading character data</h1></div>';
});
