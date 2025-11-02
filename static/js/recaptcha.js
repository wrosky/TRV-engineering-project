document.addEventListener('DOMContentLoaded', function () {
    const forms = document.querySelectorAll('form[data-recaptcha="true"]');

    forms.forEach(function (form) {
        const siteKey = form.dataset.recaptchaKey;

        form.addEventListener('submit', function (e) {
            e.preventDefault();

            grecaptcha.ready(function () {
                grecaptcha.execute(siteKey, {action: 'generic'}).then(function (token) {
                    let field = form.querySelector('input[name="g-recaptcha-response"]');
                    if (!field) {
                        field = document.createElement('input');
                        field.type = 'hidden';
                        field.name = 'g-recaptcha-response';
                        form.appendChild(field);
                    }
                    field.value = token;

                    let cap = form.querySelector('input[name="captcha"]');
                    if (!cap) {
                        cap = document.createElement('input');
                        cap.type = 'hidden';
                        cap.name = 'captcha';
                        form.appendChild(cap);
                    }
                    cap.value = token;

                    form.submit();
                });
            });
        });
    });
});
