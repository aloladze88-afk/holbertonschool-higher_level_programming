const url = 'https://swapi-api.hbtn.io/api/films/?format=json';
const movieList = document.querySelector('#list_movies');

fetch(url)
  .then(function (response) {
    return response.json();
  })
  .then(function (data) {
    data.results.forEach(function (movie) {
      const listItem = document.createElement('li');
      listItem.textContent = movie.title;
      movieList.appendChild(listItem);
    });
  });