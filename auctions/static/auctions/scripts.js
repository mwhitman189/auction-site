document.addEventListener('DOMContentLoaded', function () {
    const rmvBtn = document.querySelector('.remove-btn')
    rmvBtn.style.animationPlayState = 'paused'

    document.querySelector('a').onclick = () => {
        if (rmvBtn.style.animationPlayState === 'paused') {
            rmvBtn.style.animationPlayState = 'running'
        } else {
            rmvBtn.style.animationPlayState = 'paused'
        }
    }
})
