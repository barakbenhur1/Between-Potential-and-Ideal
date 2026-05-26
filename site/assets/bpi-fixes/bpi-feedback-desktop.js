(function () {
  function isMobileLike() {
    return /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent || "") ||
      (window.matchMedia && window.matchMedia("(pointer: coarse)").matches);
  }

  function feedbackData(link) {
    var isHebrew = document.documentElement.lang === "he" ||
      document.documentElement.dir === "rtl" ||
      document.body.classList.contains("public-page-he");

    var to = link.getAttribute("data-feedback-to") || "betweenpotentialandideal@gmail.com";
    var subject = link.getAttribute("data-feedback-subject") ||
      (isHebrew ? "ביקורת על Between Potential and Ideal" : "Feedback on Between Potential and Ideal");
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

    return { to: to, subject: subject, body: body };
  }

  function encodedMailto(link) {
    var data = feedbackData(link);
    return "mailto:" + encodeURIComponent(data.to).replace(/%40/g, "@") +
      "?subject=" + encodeURIComponent(data.subject) +
      "&body=" + encodeURIComponent(data.body);
  }

  function encodedGmail(link) {
    var data = feedbackData(link);
    return "https://mail.google.com/mail/?view=cm&fs=1&tf=1" +
      "&to=" + encodeURIComponent(data.to) +
      "&su=" + encodeURIComponent(data.subject) +
      "&body=" + encodeURIComponent(data.body);
  }

  function targetHref(link) {
    return isMobileLike() ? encodedMailto(link) : encodedGmail(link);
  }

  function isFeedbackLink(link) {
    if (!link || !link.getAttribute) return false;
    var href = (link.getAttribute("href") || "").toLowerCase();
    var text = (link.textContent || "").toLowerCase();
    var label = (link.getAttribute("aria-label") || "").toLowerCase();
    return link.hasAttribute("data-gmail-compose") ||
      href.indexOf("mail.google.com") !== -1 ||
      href.indexOf("gmail.com/mail") !== -1 ||
      href.indexOf("mailto:") === 0 && (text.indexOf("ביקורת") !== -1 || text.indexOf("feedback") !== -1 || text.indexOf("מייל") !== -1) ||
      text.indexOf("שלח ביקורת") !== -1 ||
      text.indexOf("פתח מייל") !== -1 ||
      text.indexOf("send feedback") !== -1 ||
      label.indexOf("feedback") !== -1 ||
      label.indexOf("ביקורת") !== -1;
  }

  function patch(link) {
    var href = targetHref(link);
    link.setAttribute("href", href);
    link.removeAttribute("target");
    link.removeAttribute("rel");
    link.removeAttribute("onclick");
    link.onclick = null;
    link.setAttribute("data-feedback-link-fixed", isMobileLike() ? "mailto" : "gmail");
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
    if (event.stopImmediatePropagation) event.stopImmediatePropagation();
    window.location.href = link.getAttribute("href");
  }, true);

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", patchAll);
  } else {
    patchAll();
  }
  window.addEventListener("pageshow", patchAll);
})();
