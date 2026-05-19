/**
 * toast.js
 * ─────────────────────────────────────────────────────────────────
 * Two responsibilities:
 *   1. Auto-show & auto-dismiss Django-message toasts (rendered by toast.html)
 *   2. showToast(message, type) – programmatic toasts from JS (e.g. add-to-cart)
 * ─────────────────────────────────────────────────────────────────
 */

const TOAST_DURATION = 3000; // ms before toast fades out
const TOAST_FADE     = 500;  // ms for the CSS transition

/**
 * Animate a single toast element in, then auto-dismiss it.
 * @param {HTMLElement} el
 */
function _activateToast(el) {
  // Trigger enter animation (remove opacity-0 + translate-y-4)
  requestAnimationFrame(() => {
    el.classList.remove('opacity-0', 'translate-y-4');
    el.classList.add('opacity-100', 'translate-y-0');
  });

  // Auto-dismiss
  setTimeout(() => {
    _dismissToast(el);
  }, TOAST_DURATION);
}

function _dismissToast(el) {
  el.classList.remove('opacity-100', 'translate-y-0');
  el.classList.add('opacity-0', 'translate-y-4');
  setTimeout(() => el.remove(), TOAST_FADE);
}

/**
 * Programmatically create and show a toast.
 * @param {string} message
 * @param {'success'|'error'} type
 */
function showToast(message, type = 'success') {
  const isSuccess = type === 'success';

  const el = document.createElement('div');
  el.className = [
    'toast-msg',
    'fixed', 'bottom-6', 'right-6', 'z-50',
    'flex', 'items-center', 'gap-3',
    'px-5', 'py-3.5', 'rounded-2xl', 'shadow-2xl',
    'font-semibold', 'text-sm',
    'transition-all', 'duration-500',
    'opacity-0', 'translate-y-4',
    isSuccess ? 'bg-yellow-400' : 'bg-red-500',
    isSuccess ? 'text-gray-900' : 'text-white',
  ].join(' ');

  const icon = isSuccess
    ? `<svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
         <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/>
       </svg>`
    : `<svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
         <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z"/>
       </svg>`;

  el.innerHTML = `
    ${icon}
    <span>${message}</span>
    <button
      onclick="this.closest('.toast-msg').remove()"
      class="ml-2 opacity-60 hover:opacity-100 transition-opacity duration-200"
      aria-label="Dismiss"
    >
      <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12"/>
      </svg>
    </button>
  `;

  document.body.appendChild(el);
  _activateToast(el);
}

// ── Auto-activate any server-rendered toasts (from toast.html) ──
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.toast-msg').forEach(el => _activateToast(el));
});