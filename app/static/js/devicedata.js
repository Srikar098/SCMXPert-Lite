const rowsPerPage = 10; // number of rows per page
const tableBody = document.querySelector('tbody');
const paginationLinks = document.querySelector('.pagination');

// create an array of all rows in the table body
const tableRows = Array.from(tableBody.querySelectorAll('tr'));

// calculate the total number of pages
const totalPages = Math.ceil(tableRows.length / rowsPerPage);

// display the first page and create pagination links
displayPage(1);
createPaginationLinks();

function displayPage(pageNumber) {
  // calculate the starting and ending indexes of the rows to display on the given page
  const startIndex = (pageNumber - 1) * rowsPerPage;
  const endIndex = startIndex + rowsPerPage;

  // hide all rows in the table body
  tableRows.forEach(row => row.style.display = 'none');

  // display the rows for the given page
  for (let i = startIndex; i < endIndex && i < tableRows.length; i++) {
    tableRows[i].style.display = 'table-row';
  }
}

function createPaginationLinks() {
  // create a link for each page and add it to the pagination container
  for (let i = 1; i <= totalPages; i++) {
    const link = document.createElement('a');
    link.href = '#';
    link.textContent = i;
    link.classList.add('page-link');
    link.dataset.pageNumber = i;

    // add an event listener to each link to display the corresponding page when clicked
    link.addEventListener('click', () => {
      const pageNumber = parseInt(link.dataset.pageNumber);
      displayPage(pageNumber);
      setActiveLink(link);
    });

    paginationLinks.querySelector('ul').appendChild(document.createElement('li')).appendChild(link);
  }

  // // add event listeners to the "Previous" and "Next" links #prev-page-link
  // const prevLink = document.getElementById("prev-page-link");
  // const nextLink = document.getElementById("next-page-link");
  // prevLink.addEventListener('click', () => {
  //   const activeLink = paginationLinks.querySelector('.active');
  //   if (activeLink.previousElementSibling) {
  //     const pageNumber = parseInt(activeLink.previousElementSibling.dataset.pageNumber);
  //     displayPage(pageNumber);
  //     setActiveLink(activeLink.previousElementSibling);
  //   }
  // });
  // nextLink.addEventListener('click', () => {
  //   const activeLink = paginationLinks.querySelector('.active');
  //   if (activeLink.nextElementSibling) {
  //     const pageNumber = parseInt(activeLink.nextElementSibling.dataset.pageNumber);
  //     displayPage(pageNumber);
  //     setActiveLink(activeLink.nextElementSibling);
  //   }
  // });

  // set the first link as active by default
  setActiveLink(paginationLinks.querySelector('.page-link'));
}

function setActiveLink(link) {
  // remove the "active" class from all links
  paginationLinks.querySelectorAll('a').forEach(a => a.classList.remove('active'));

  // add the "active" class to the given link
  link.classList.add('active');
}
