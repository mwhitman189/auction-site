document.addEventListener('DOMContentLoaded', function () {
    document.addEventListener('click', event => {
        const element = event.target

        if (element.className === 'remove-btn btn') {
            element.parentElement.style.animationPlayState = 'running'
            element.parentElement.addEventListener('animationend', () => {
                element.parentElement.remove()
                toggleWatchlistItem(element.dataset.listing_id)
            })
        }
    })

    watchlistToggleBtn = document.getElementById('watchlist-btn')
    watchlistToggleBtn.addEventListener('click', () => {
        toggleWatchlistItem(watchlistToggleBtn.dataset.listing_id)
        if (watchlistToggleBtn.classList.contains('watchlisted')) {
            watchlistToggleBtn.innerHTML = "Watch item"
            watchlistToggleBtn.classList.remove('watchlisted')
        } else {
            watchlistToggleBtn.innerHTML = "Unwatch item"
            watchlistToggleBtn.classList.add('watchlisted')
        }
        watchlistToggleBtn.innerHTML('')
    })
})

function toggleWatchlistItem(item_id) {
    fetch(`http://localhost:8000/watchlist/toggle/${item_id}`)
        .then(res => console.log(res))
        .catch(err => console.log(err))
}