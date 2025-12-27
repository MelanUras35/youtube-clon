// YouTube iframe player with fallback for embed errors.
(function () {
    const playerEl = document.getElementById('youtube-player');
    if (!playerEl) {
        return;
    }

    const videoId = playerEl.dataset.videoId;
    const fallback = document.getElementById('video-fallback');

    const showFallback = () => {
        if (fallback) {
            fallback.classList.remove('is-hidden');
        }
    };

    const hideFallback = () => {
        if (fallback) {
            fallback.classList.add('is-hidden');
        }
    };

    const initPlayer = () => {
        if (!window.YT || !window.YT.Player) {
            showFallback();
            return;
        }

        new window.YT.Player(playerEl, {
            videoId: videoId,
            playerVars: {
                autoplay: 1,
                rel: 0,
                modestbranding: 1,
                playsinline: 1,
                origin: window.location.origin,
            },
            events: {
                onReady: () => hideFallback(),
                onError: () => showFallback(),
            },
        });
    };

    const loadApi = () => {
        if (document.getElementById('youtube-iframe-api')) {
            return;
        }
        const tag = document.createElement('script');
        tag.id = 'youtube-iframe-api';
        tag.src = 'https://www.youtube.com/iframe_api';
        document.head.appendChild(tag);
    };

    const previousReady = window.onYouTubeIframeAPIReady;
    window.onYouTubeIframeAPIReady = () => {
        if (typeof previousReady === 'function') {
            previousReady();
        }
        initPlayer();
    };

    if (window.YT && window.YT.Player) {
        initPlayer();
    } else {
        loadApi();
        setTimeout(() => {
            if (!window.YT || !window.YT.Player) {
                showFallback();
            }
        }, 4000);
    }
})();
