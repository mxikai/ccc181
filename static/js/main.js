// Served at /static/js/main.js and linked from templates/base.html.
console.log("ClinicQ starter app loaded");

// 8a. Stop double submits on the New Order form.
const joinForm = document.getElementById("join-form");
if (joinForm) {
  const button = joinForm.querySelector("button[type=submit]");
  const originalText = button.textContent;
  joinForm.addEventListener("submit", () => {
    button.disabled = true;
    button.textContent = "Getting your ticket…";
  });
  // If the browser's Back button restores this page, un-freeze the button.
  window.addEventListener("pageshow", () => {
    button.disabled = false;
    button.textContent = originalText;
  });
}