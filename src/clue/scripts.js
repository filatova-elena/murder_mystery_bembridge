// Clue and Journal page functionality

// For clue pages - show character-specific observations
function showCharacterObservation(interpretations) {
  const character = getCharacter();
  if (character && interpretations && interpretations[character]) {
    document.getElementById('characterAnalysis').innerHTML = '<p>' + interpretations[character] + '</p>';
    document.getElementById('characterObservations').style.display = 'block';
  }
}

// For journal pages - show per-entry and overall observations
function showJournalObservations(entries, journalInterpretations) {
  const character = getCharacter();
  
  // Handle per-entry interpretations
  if (entries && character) {
    entries.forEach((entry, index) => {
      if (entry.character_interpretations && entry.character_interpretations[character]) {
        const obsEl = document.getElementById('entryObservation-' + (index + 1));
        const analysisEl = document.getElementById('entryAnalysis-' + (index + 1));
        if (obsEl && analysisEl) {
          analysisEl.innerHTML = entry.character_interpretations[character];
          obsEl.style.display = 'block';
        }
      }
    });
  }
  
  // Handle journal-level interpretations
  if (character && journalInterpretations && journalInterpretations[character]) {
    document.getElementById('characterAnalysis').innerHTML = journalInterpretations[character];
    document.getElementById('characterObservations').style.display = 'block';
  }
}
