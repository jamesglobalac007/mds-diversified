const menuButton = document.querySelector('[data-menu-toggle]');
const menu = document.querySelector('[data-menu]');

if (menuButton && menu) {
  menuButton.addEventListener('click', () => menu.classList.toggle('open'));
}

const enquiryForm = document.getElementById('enquiry-form');
if (enquiryForm) {
  const topicInput = enquiryForm.querySelector('[data-enquiry-topic]');
  const tagStrong = enquiryForm.querySelector('[data-enquiry-tag] strong');
  document.querySelectorAll('.contact-option[data-topic]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const topic = btn.dataset.topic;
      topicInput.value = topic;
      tagStrong.textContent = btn.textContent.trim();
      enquiryForm.dataset.fallbackSubject = `Need help with ${topic.toLowerCase()}`;
      enquiryForm.hidden = false;
      document.querySelectorAll('.contact-option[data-topic]').forEach((b) => b.classList.toggle('is-active', b === btn));
      enquiryForm.scrollIntoView({ behavior: 'smooth', block: 'center' });
      const firstField = enquiryForm.querySelector('input[name="name"]');
      if (firstField) firstField.focus({ preventScroll: true });
    });
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
