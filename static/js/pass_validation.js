document.addEventListener("DOMContentLoaded", function () {
    const pwd = document.getElementById("id_password");
    if (!pwd) return;

    const rules = {
        length: document.querySelector('#password-rules [data-rule="length"]'),
        upper: document.querySelector('#password-rules [data-rule="upper"]'),
        lower: document.querySelector('#password-rules [data-rule="lower"]'),
        digit: document.querySelector('#password-rules [data-rule="digit"]'),
        symbol: document.querySelector('#password-rules [data-rule="symbol"]'),
    };

    pwd.addEventListener("input", function () {
        const v = pwd.value;

        if (v.length >= 9) {
            rules.length.style.color = "green";
        } else {
            rules.length.style.color = "red";
        }

        if (/[A-Z]/.test(v)) {
            rules.upper.style.color = "green";
        } else {
            rules.upper.style.color = "red";
        }

        if (/[a-z]/.test(v)) {
            rules.lower.style.color = "green";
        } else {
            rules.lower.style.color = "red";
        }

        if (/\d/.test(v)) {
            rules.digit.style.color = "green";
        } else {
            rules.digit.style.color = "red";
        }

        if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>/?]/.test(v)) {
            rules.symbol.style.color = "green";
        } else {
            rules.symbol.style.color = "red";
        }
    });
});