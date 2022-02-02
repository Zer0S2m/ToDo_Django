const btnOpenFilter = document.querySelector(".btn-open-filter");
const filterBlock = document.querySelector(".filter");

if ( btnOpenFilter ) {
    btnOpenFilter.addEventListener("click", () => {
        filterBlock.classList.toggle("filter--active");

        if ( filterBlock.classList.contains("filter--active") ) {
            heightFilter = filterBlock.querySelector("form").offsetHeight;
            filterBlock.style.maxHeight = `${heightFilter}px`;
        } else {
            filterBlock.style.maxHeight = `0px`;
        };
    });
};
