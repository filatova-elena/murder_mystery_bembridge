// Book chapter navigation
// Note: `entries`, `prevChapter`, `nextChapter` are set by the template

let currentEntryIndex = 0;

function formatDate(dateString) {
  if (!dateString) return '';
  const parts = dateString.split('-');
  if (parts.length === 3) {
    const date = new Date(parts[0], parts[1] - 1, parts[2]);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  }
  return dateString;
}

function displayEntry(index) {
  if (!entries || index < 0 || index >= entries.length) return;
  
  currentEntryIndex = index;
  window.location.hash = (index + 1);
  
  const entry = entries[index];
  document.getElementById('entryDate').innerText = formatDate(entry.date) + ' - ' + (entry.location || '');
  
  // Format content with paragraphs
  let content = entry.content || '';
  let paragraphs = content.split(/\n\n+/).filter(p => p.trim());
  let formatted = paragraphs.map(p => '<p>' + p.replace(/\n/g, ' ') + '</p>').join('');
  if (entry.is_italic) formatted = '<em>' + formatted + '</em>';
  document.getElementById('entryContent').innerHTML = formatted;
  
  document.getElementById('pageNum').innerText = `Entry ${index + 1} of ${entries.length}`;
  
  // Update navigation buttons
  const isFirst = index === 0;
  const isLast = index === entries.length - 1;
  
  const prevBtn = document.getElementById('prevBtn');
  prevBtn.disabled = isFirst && !prevChapter;
  prevBtn.textContent = isFirst && prevChapter ? '← Previous Chapter' : '← Previous Entry';
  
  const nextBtn = document.getElementById('nextBtn');
  nextBtn.disabled = isLast && !nextChapter;
  nextBtn.textContent = isLast && nextChapter ? 'Next Chapter →' : 'Next Entry →';
}

function previousEntry() {
  if (currentEntryIndex > 0) {
    displayEntry(currentEntryIndex - 1);
    window.scrollTo(0, 0);
  } else if (prevChapter) {
    window.location.href = '/book/' + prevChapter + '.html#last';
  }
}

function nextEntry() {
  if (currentEntryIndex < entries.length - 1) {
    displayEntry(currentEntryIndex + 1);
    window.scrollTo(0, 0);
  } else if (nextChapter) {
    window.location.href = '/book/' + nextChapter + '.html';
  }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
  let startEntry = 0;
  if (window.location.hash) {
    const hash = window.location.hash.substring(1);
    if (hash === 'last') {
      startEntry = entries.length - 1;
    } else {
      const num = parseInt(hash);
      if (!isNaN(num) && num > 0 && num <= entries.length) {
        startEntry = num - 1;
      }
    }
  }
  displayEntry(startEntry);
});
