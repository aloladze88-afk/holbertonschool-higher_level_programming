document.addEventListener('DOMContentLoaded', function () {
  const url = 'https://hellosalut.stefanbohacek.com/?lang=fr';

  fetch(url)
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      document.querySelector('#hello').textContent = data.hello;
    });
});