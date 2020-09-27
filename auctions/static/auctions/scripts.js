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
})

function toggleWatchlistItem(item_id) {
    fetch(`watchlist/toggle/${item_id}`)
        .then(res => console.log(res))
        .catch(err => console.log(err))
}