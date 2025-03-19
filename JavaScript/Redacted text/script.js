const redactedSpans = document.querySelectorAll(".redacted");

redactedSpans.forEach((span) => {
  span.addEventListener("click", () => {
    span.classList.toggle("unredacted");
  });
});

const coveredSpans = document.querySelectorAll(".cover");

coveredSpans.forEach((span) => {
  span.addEventListener("click", () => {
    span.classList.toggle("unredacted");
  });
});
