import { checkLoginStatusLogin } from "./checkStatus.js";
import * as utils from "./utils.js";
checkLoginStatusLogin();


document.getElementById('loginForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    await login();
});

const login = async () => {
    const email = document.getElementById('form2Example1').value;
    const password = document.getElementById('form2Example2').value;
    if (!email || !password) {
        utils.showNotification('Vui lòng điền đầy đủ thông tin!', 'error');
        return;
    }
    document.querySelector(".fullscreen-overlay").classList.remove("d-none");

    try {
        const response = await axios.post('http://localhost:8080/api/auth/login', { email, password });
        if (response.data.error === 0) {
            window.location.href = '/mainPage';
        } else {
            utils.showNotification(response.data.message, 'error');
        }
    } catch (error) {
        console.error('Error logging in:', error);
        utils.showNotification(error.response.data.message, 'error');
    }
    document.querySelector(".fullscreen-overlay").classList.add("d-none");
};
