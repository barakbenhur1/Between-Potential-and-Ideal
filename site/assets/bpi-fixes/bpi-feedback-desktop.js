(function () {
  function isMobileLike() {
    return /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent || "") ||
      (window.matchMedia && window.matchMedia("(pointer: coarse)").matches);
  }

  function openGmailOrMailto(event, link) {
    var gmailUrl = link.getAttribute("data-gmail-compose");
    var mailtoUrl = link.getAttribute("href");

    if (!gmailUrl || !mailtoUrl) return;

    // On phones/tablets, keep the native mail behavior.
    if (isMobileLike()) return;

    // On desktop, mailto often does nothing if no mail app is configured.
    // Open Gmail instead.
    event.preventDefault();
    event.stopPropagation();

    var opened = window.open(gmailUrl, "_blank", "noopener,noreferrer");

    // Fallback if popup blocking prevents opening Gmail.
    if (!opened) {
      window.location.href = mailtoUrl;
    }
  }

  document.addEventListener("click", function (event) {
    var link = event.target.closest && event.target.closest("a.response-button[data-gmail-compose], a[data-gmail-compose].response-button");
    if (!link) return;
    openGmailOrMailto(event, link);
  }, true);
})();
