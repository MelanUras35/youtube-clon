// Video page JavaScript

document.addEventListener('DOMContentLoaded', function () {
    const likeBtn = document.getElementById('likeBtn');
    const dislikeBtn = document.getElementById('dislikeBtn');
    const likeCount = document.getElementById('likeCount');
    const dislikeCount = document.getElementById('dislikeCount');
    const subscribeBtn = document.getElementById('subscribeBtn');
    const subscriberCount = document.getElementById('subscriberCount');

    // Like/Dislike functionality
    if (likeBtn && dislikeBtn) {
        likeBtn.addEventListener('click', function () {
            if (!isAuthenticated) {
                window.location.href = '/login/';
                return;
            }
            toggleLike('like');
        });

        dislikeBtn.addEventListener('click', function () {
            if (!isAuthenticated) {
                window.location.href = '/login/';
                return;
            }
            toggleLike('dislike');
        });
    }

    function toggleLike(action) {
        fetch(`/like/${videoId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken,
            },
            body: `action=${action}`,
        })
            .then(response => response.json())
            .then(data => {
                likeCount.textContent = data.like_count;
                dislikeCount.textContent = data.dislike_count;

                // Update button states
                if (action === 'like') {
                    if (data.status === 'removed') {
                        likeBtn.classList.remove('active');
                    } else {
                        likeBtn.classList.add('active');
                        dislikeBtn.classList.remove('active');
                    }
                } else {
                    if (data.status === 'removed') {
                        dislikeBtn.classList.remove('active');
                    } else {
                        dislikeBtn.classList.add('active');
                        likeBtn.classList.remove('active');
                    }
                }
            })
            .catch(error => console.error('Error:', error));
    }

    // Subscribe functionality
    if (subscribeBtn) {
        subscribeBtn.addEventListener('click', function () {
            if (!isAuthenticated) {
                window.location.href = '/login/';
                return;
            }

            const userId = this.dataset.userId;

            fetch(`/subscribe/${userId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken,
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (data.subscribed) {
                        subscribeBtn.classList.add('subscribed');
                        subscribeBtn.textContent = 'Subscribed';
                    } else {
                        subscribeBtn.classList.remove('subscribed');
                        subscribeBtn.textContent = 'Subscribe';
                    }
                    subscriberCount.textContent = `${data.subscriber_count} subscribers`;
                })
                .catch(error => console.error('Error:', error));
        });
    }
});
