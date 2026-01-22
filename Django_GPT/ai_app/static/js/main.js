document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const btn = form?.querySelector("button");
    const resultBox = document.querySelector(".result-box");

    if (!form || !btn) return;

    form.addEventListener("submit", () => {
        btn.disabled = true;
        btn.innerText = "Processing...";

        if (resultBox) {
            resultBox.innerText = "Processing...";
        }
        });
});
