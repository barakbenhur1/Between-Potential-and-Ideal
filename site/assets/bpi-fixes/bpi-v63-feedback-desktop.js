/* BPI V63 — desktop-safe feedback button.
   Opens Gmail on desktop, mail app on mobile, and keeps nav tabs untouched. */
(() => {
  const EMAIL = "betweenpotentialandideal@gmail.com";
  const SUBJECT = "Response to Between Potential and Ideal";
  const BODY = "שלום,\n\nאני רוצה להגיב על התאוריה:\n\n";

  function enc(value) {
    return encodeURIComponent(value);
  }

  function gmailUrl() {
    return "https://mail.google.com/mail/?view=cm&fs=1"
      + "&to=" + enc(EMAIL)
      + "&su=" + enc(SUBJECT)
      + "&body=" + enc(BODY);
  }

  function mailtoUrl() {
    return "mailto:" + EMAIL
      + "?subject=" + enc(SUBJECT)
      + "&body=" + enc(BODY);
  }

  function isMobileLike() {
    return /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent || "")
      || ((navigator.maxTouchPoints || 0) > 0 && window.innerWidth < 860);
  }

  function isFeedbackAction(anchor) {
    if (!anchor) return false;
    const href = anchor.getAttribute("href") || "";
    const text = (anchor.textContent || "").trim();
    const cls = anchor.className || "";

    // Explicit action markers only. This intentionally does NOT catch nav tabs
    // like "ביקורת" that link to critique.html.
    if (anchor.matches("[data-bpi-feedback-button='1'], .bpi-feedback-action, .response-button")) {
      return true;
    }

    const isMailToFeedback =
      href.startsWith("mailto:" + EMAIL)
      || href.includes("betweenpotentialandideal%40gmail.com")
      || href.includes(EMAIL);

    const actionText = /(פתח|שלח|שליחת|תגובה|ביקורת|feedback|response|mail|email)/i.test(text);
    const actionClass = /(response|feedback|mail|email)/i.test(String(cls));

    return isMailToFeedback && (actionText || actionClass);
  }

  document.addEventListener("click", function(event) {
    const anchor = event.target && event.target.closest ? event.target.closest("a") : null;
    if (!isFeedbackAction(anchor)) return;

    event.preventDefault();
    event.stopPropagation();

    const gmail = anchor.dataset.gmailCompose || gmailUrl();
    const mailto = anchor.dataset.mailto || mailtoUrl();

    if (isMobileLike()) {
      // Mobile usually has a native mail handler and already worked.
      window.location.href = mailto;
      return;
    }

    // Desktop: mailto is often unconfigured and looks like "nothing happened".
    // Gmail web is deterministic and opens in a new tab.
    const opened = window.open(gmail, "_blank", "noopener,noreferrer");
    if (!opened) {
      window.location.href = gmail;
    }
  }, true);
})();
