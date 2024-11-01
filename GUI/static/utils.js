let alertTimeout;
export const showNotification = (message, type) => {
    let alert = document.getElementById('alert-container');
    alert.classList.remove('d-none');
    alert.classList.add(`alert-container-${type}`);
    alert.innerText = message;
    if (alertTimeout) {
        clearTimeout(alertTimeout);
    }
    alertTimeout = setTimeout(() => {
        alert.classList.remove('alert-container-success', 'alert-container-error');
        alert.classList.add('d-none');
        alert.innerText = '';
    }, 3000);
}