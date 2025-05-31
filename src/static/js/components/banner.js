document.addEventListener("DOMContentLoaded", () => {
  const marqueeContent = document.getElementById("marquee-content");
  const originalText = marqueeContent.innerHTML;
  let contentWidth = marqueeContent.scrollWidth;
  const containerWidth = marqueeContent.parentElement.offsetWidth;

  // Duplica il contenuto fino a coprire almeno 2 volte la larghezza del container
  while (contentWidth < containerWidth * 2) {
    marqueeContent.innerHTML += originalText;
    contentWidth = marqueeContent.scrollWidth;
  }
});
