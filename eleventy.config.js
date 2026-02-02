// Eleventy Configuration
// Run with: npx @11ty/eleventy --serve

module.exports = function(eleventyConfig) {
  // Pass through static assets unchanged
  eleventyConfig.addPassthroughCopy("assets");
  eleventyConfig.addPassthroughCopy("images");
  eleventyConfig.addPassthroughCopy("qr_codes");
  
  // Pass through section-specific CSS and JS files (exclude data.js)
  eleventyConfig.addPassthroughCopy({ "src/book/styles.css": "book/styles.css" });
  eleventyConfig.addPassthroughCopy({ "src/book/scripts.js": "book/scripts.js" });
  eleventyConfig.addPassthroughCopy({ "src/character/styles.css": "character/styles.css" });
  eleventyConfig.addPassthroughCopy({ "src/character/scripts.js": "character/scripts.js" });
  eleventyConfig.addPassthroughCopy({ "src/clue/styles.css": "clue/styles.css" });
  eleventyConfig.addPassthroughCopy({ "src/clue/scripts.js": "clue/scripts.js" });

  // Watch for changes in data files
  eleventyConfig.addWatchTarget("./data/");

  // Custom filter to format dates
  eleventyConfig.addFilter("formatDate", function(dateString) {
    if (!dateString) return '';
    const parts = dateString.split('-');
    if (parts.length === 3) {
      const date = new Date(parts[0], parts[1] - 1, parts[2]);
      return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      });
    }
    return dateString;
  });

  // Custom filter to get skill title
  eleventyConfig.addFilter("skillTitle", function(skillKey, skills) {
    return skills[skillKey]?.title || skillKey;
  });

  return {
    dir: {
      input: "src",           // Source files go in src/
      output: "_site",        // Built files go to _site/
      includes: "",           // Layouts/includes relative to src/ root
      data: "_data"           // Global data in src/_data/
    },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk"
  };
};
