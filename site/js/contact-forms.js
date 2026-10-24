/* Contact transport for the exported design. Netlify handles storage and CAPTCHA. */
(function () {
  'use strict';
  document.addEventListener('submit', async function (event) {
    var form = event.target;
    if (!form.matches('form[data-contact-form]')) return;
    event.preventDefault();
    // Capture phase prevents the exported Webflow handler from sending a second request.
    event.stopImmediatePropagation();
    if (form.dataset.submitting === 'true' || !form.reportValidity()) return;
    var wrapper = form.closest('.w-form');
    var success = wrapper.querySelector('.w-form-done');
    var failure = wrapper.querySelector('.w-form-fail');
    var button = form.querySelector('[type="submit"]');
    var originalLabel = button.tagName === 'INPUT' ? button.value : button.textContent;
    function setButtonLabel(label) {
      if (button.tagName === 'INPUT') button.value = label;
      else button.textContent = label;
    }
    function fail(message) {
      failure.textContent = message;
      failure.style.display = 'block';
      failure.setAttribute('role', 'alert');
      failure.setAttribute('tabindex', '-1');
      failure.focus();
    }
    failure.style.display = 'none';
    success.style.display = 'none';
    var data = new FormData(form);
    if (location.hostname === 'localhost' || location.hostname === '127.0.0.1' || location.protocol === 'file:') {
      fail('This preview cannot send messages. Please call 770-946-1697 or email ConcreteLCH@gmail.com.');
      return;
    }
    if (!data.get('g-recaptcha-response')) {
      fail('Please complete the CAPTCHA before sending. You can also call 770-946-1697.');
      return;
    }
    form.dataset.submitting = 'true';
    button.disabled = true;
    setButtonLabel(button.dataset.wait || 'Please wait...');
    try {
      var response = await fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(data).toString()
      });
      if (!response.ok) throw new Error('Submission rejected');
      form.style.display = 'none';
      success.style.display = 'block';
      success.setAttribute('role', 'status');
      success.setAttribute('tabindex', '-1');
      success.focus();
      form.reset();
    } catch (error) {
      fail('Your message could not be sent. Please try again or call 770-946-1697.');
    } finally {
      form.dataset.submitting = 'false';
      button.disabled = false;
      setButtonLabel(originalLabel);
      if (window.grecaptcha) window.grecaptcha.reset();
    }
  }, true);
}());
