const menuButton = document.querySelector('[data-menu-toggle]');
const menu = document.querySelector('[data-menu]');

if (menuButton && menu) {
  menuButton.addEventListener('click', () => menu.classList.toggle('open'));
}

const enquiryForm = document.getElementById('enquiry-form');
const enquirySuccess = document.getElementById('enquiry-success');
if (enquiryForm) {
  const topicInput = enquiryForm.querySelector('[data-enquiry-topic]');
  const subjectInput = enquiryForm.querySelector('[data-enquiry-subject]');
  const tagStrong = enquiryForm.querySelector('[data-enquiry-tag] strong');
  document.querySelectorAll('[data-topic]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const topic = btn.dataset.topic;
      const tagText = btn.classList.contains('contact-option') ? btn.textContent.trim() : `Interested in: ${topic}`;
      topicInput.value = topic;
      tagStrong.textContent = tagText;
      if (subjectInput) subjectInput.value = `MDS enquiry — ${topic}`;
      if (enquirySuccess) enquirySuccess.hidden = true;
      enquiryForm.hidden = false;
      enquiryForm.reset();
      topicInput.value = topic;
      if (subjectInput) subjectInput.value = `MDS enquiry — ${topic}`;
      tagStrong.textContent = tagText;
      // Only highlight the contact-option pills (not package CTAs)
      document.querySelectorAll('.contact-option[data-topic]').forEach((b) => b.classList.toggle('is-active', b === btn));
      enquiryForm.scrollIntoView({ behavior: 'smooth', block: 'center' });
      const firstField = enquiryForm.querySelector('input[name="name"]');
      if (firstField) firstField.focus({ preventScroll: true });
    });
  });

  enquiryForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const submitBtn = enquiryForm.querySelector('button[type="submit"]');
    const originalLabel = submitBtn ? submitBtn.textContent : '';
    if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Sending…'; }
    try {
      const data = new FormData(enquiryForm);
      const response = await fetch(enquiryForm.action, {
        method: 'POST',
        body: data,
        headers: { 'Accept': 'application/json' }
      });
      if (!response.ok) throw new Error('send failed');
      enquiryForm.hidden = true;
      if (enquirySuccess) {
        enquirySuccess.hidden = false;
        enquirySuccess.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    } catch (err) {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = originalLabel || 'Send';
      }
      alert("Couldn't send right now. Email james@mdsdiversified.ai and we'll pick it up.");
    }
  });
}

document.querySelectorAll('form[data-fallback-subject]').forEach((form) => {
  form.addEventListener('submit', (event) => {
    const action = form.getAttribute('action') || '';
    if (!action.includes('YOUR_FORM_ID')) return;

    event.preventDefault();
    const data = new FormData(form);
    const lines = [];
    data.forEach((value, key) => lines.push(`${key}: ${value}`));
    const subject = encodeURIComponent(form.dataset.fallbackSubject || 'MDS enquiry');
    const body = encodeURIComponent(lines.join('\n'));
    window.location.href = `mailto:james@mdsdiversified.ai?subject=${subject}&body=${body}`;
  });
});
