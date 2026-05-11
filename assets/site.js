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
      alert("Couldn't send right now. Email sales@mdsdiversified.ai and we'll pick it up.");
    }
  });
}

// ----- CURRENCY SWITCHER -----
// Auto-detect visitor country on first visit, manual override persists via localStorage.
// Display-only — Stripe Payment Links still process in AUD. International cards convert at the
// customer's bank exchange rate. The displayed AED/USD prices are rounded marketing equivalents.
const COUNTRY_TO_CURRENCY = { AU: 'AUD', AE: 'AED', US: 'USD' };

function applyCurrency(currency) {
  const code = currency.toUpperCase();
  document.querySelectorAll('[data-price-aud]').forEach((el) => {
    const next = el.dataset[`price${code.charAt(0)}${code.slice(1).toLowerCase()}`];
    if (next) el.textContent = next;
  });
  document.querySelectorAll('[data-currency-switch]').forEach((btn) => {
    btn.classList.toggle('is-active', btn.dataset.currencySwitch === code);
  });
  // GST only applies to AUD customers — hide the "ex GST" pill for AED/USD
  document.querySelectorAll('.package-price-tax').forEach((el) => {
    el.style.display = code === 'AUD' ? '' : 'none';
  });
  try { localStorage.setItem('mds_currency', code); } catch (_) {}
}

async function detectCountry() {
  try {
    const res = await fetch('https://api.country.is/', { mode: 'cors' });
    if (!res.ok) return null;
    const data = await res.json();
    return data && data.country;
  } catch (_) {
    return null;
  }
}

(async function initCurrency() {
  // Manual choice wins over auto-detect
  let chosen = null;
  try { chosen = localStorage.getItem('mds_currency'); } catch (_) {}
  if (chosen && ['AUD', 'AED', 'USD'].includes(chosen)) {
    applyCurrency(chosen);
  } else {
    const country = await detectCountry();
    applyCurrency(COUNTRY_TO_CURRENCY[country] || 'AUD');
  }
  document.querySelectorAll('[data-currency-switch]').forEach((btn) => {
    btn.addEventListener('click', () => applyCurrency(btn.dataset.currencySwitch));
  });
})();

// ----- SCROLL-TRIGGERED REVEALS -----
// Each element with [data-reveal] fades + slides in when it enters the viewport.
// Uses IntersectionObserver — zero library, near-zero CPU, respects prefers-reduced-motion.
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (!prefersReducedMotion) {
  const revealTargets = document.querySelectorAll('.apple-card, .package-card, .faq-item, .always-inner, .contact-inner, .hero-tagline');
  revealTargets.forEach((el) => el.setAttribute('data-reveal', ''));
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.setAttribute('data-reveal-in', '');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 });
    revealTargets.forEach((el) => io.observe(el));
  } else {
    // Fallback: just show everything if IntersectionObserver isn't supported
    revealTargets.forEach((el) => el.setAttribute('data-reveal-in', ''));
  }
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
    window.location.href = `mailto:sales@mdsdiversified.ai?subject=${subject}&body=${body}`;
  });
});
