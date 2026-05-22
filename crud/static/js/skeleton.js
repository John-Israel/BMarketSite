setTimeout(function () {

  // Reveal banner
  document.getElementById('welcome-banner').classList.remove('opacity-0', 'translate-y-6');

  // Hide stats skeleton, show real
  document.getElementById('stats-skeleton').style.display = 'none';
  var statsReal = document.getElementById('stats-real');
  statsReal.classList.remove('hidden');
  setTimeout(function () {
    statsReal.classList.remove('opacity-0', 'translate-y-6');
  }, 50);

  // Hide bottom skeleton, show real
  setTimeout(function () {
    document.getElementById('bottom-skeleton').style.display = 'none';
    var bottomReal = document.getElementById('bottom-real');
    bottomReal.classList.remove('hidden');
    setTimeout(function () {
      bottomReal.classList.remove('opacity-0', 'translate-y-6');
    }, 50);
  }, 150);

}, 600);