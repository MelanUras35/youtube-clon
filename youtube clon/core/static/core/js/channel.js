// Channel page JavaScript

document.addEventListener('DOMContentLoaded', function () {
    const subscribeBtn = document.getElementById('subscribeBtn');
    const subscriberCount = document.getElementById('subscriberCount');

    if (subscribeBtn) {
        subscribeBtn.addEventListener('click', function () {
            if (!isAuthenticated) {
                window.location.href = '/login/';
                return;
            }

            fetch(`/subscribe/${channelId}/`, {
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
                    // Update subscriber count in the display
                    const currentText = subscriberCount.textContent;
                    const parts = currentText.split(' subscribers');
                    subscriberCount.textContent = `${data.subscriber_count} subscribers${parts[1] || ''}`;
                })
                .catch(error => console.error('Error:', error));
        });
    }
});
