(function () {
  function encodedMailto(link) {
    var to = link.getAttribute("data-feedback-to") || "betweenpotentialandideal@gmail.com";
    var subject = link.getAttribute("data-feedback-subject") || "Response to Between Potential and Ideal";
    var isHebrew = document.documentElement.lang === "he" || document.documentElement.dir === "rtl" || document.body.classList.contains("public-page-he");
    var body = link.getAttribute("data-feedback-body") || (isHebrew
      ? [
          "שלום,",
          "",
          "קראתי את Between Potential and Ideal ויש לי הערה / ביקורת:",
          "",
          "העמוד שבו הייתי:",
          window.location.href,
          "",
          "הערה:"
        ].join("\n")
      : [
          "Hi,",
          "",
          "I read Between Potential and Ideal and have feedback / a note:",
          "",
          "Page I was on:",
          window.location.href,
          "",
          "Feedback:"
        ].join("\n"));

    return "mailto:" + encodeURIComponent(to).replace(/%40/g, "@") +
      "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(body);
  }

  function isFeedbackLink(link) {
    if (!link || !link.getAttribute) return false;
    var href = (link.getAttribute("href") || "").toLowerCase();
    var text = (link.textContent || "").toLowerCase();
    var label = (link.getAttribute("aria-label") || "").toLowerCase();
    return link.hasAttribute("data-gmail-compose") ||
      href.indexOf("mail.google.com") !== -1 ||
      href.indexOf("gmail.com/mail") !== -1 ||
      text.indexOf("שלח ביקורת") !== -1 ||
      text.indexOf("פתח מייל") !== -1 ||
      text.indexOf("send feedback") !== -1 ||
      label.indexOf("feedback") !== -1 ||
      label.indexOf("ביקורת") !== -1;
  }

  function patch(link) {
    var mailto = encodedMailto(link);
    link.setAttribute("href", mailto);
    link.removeAttribute("target");
    link.removeAttribute("rel");
    link.removeAttribute("onclick");
    link.setAttribute("data-feedback-mailto-fixed", "true");
  }

  function patchAll() {
    document.querySelectorAll("a[href], a[data-gmail-compose]").forEach(function (link) {
      if (isFeedbackLink(link)) patch(link);
    });
  }

  document.addEventListener("click", function (event) {
    var link = event.target.closest && event.target.closest("a[href], a[data-gmail-compose]");
    if (!isFeedbackLink(link)) return;
    patch(link);
    event.preventDefault();
    event.stopPropagation();
    window.location.href = link.getAttribute("href");
  }, true);

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", patchAll);
  } else {
    patchAll();
  }
  window.addEventListener("pageshow", patchAll);
})();
