import { checkLoginStatusRegister } from "./checkStatus.js";
import * as regex from "./regex.js";
import * as utils from "./utils.js";
checkLoginStatusRegister();

document.getElementById('registerForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    await register();
});

export const register = async () => {
    const email = document.getElementById('form2Example1').value;
    const password = document.getElementById('form2Example2').value;
    const repeatPassword = document.getElementById('form2Example3').value;
    if (!email || !password || !repeatPassword) {
        utils.showNotification('Vui lòng điền đầy đủ thông tin!', 'error');
        return;
    }
    if (!regex.rgEmail.test(email)) {
        utils.showNotification('Email không hợp lệ!', 'error');
        return;
    }
    if (!regex.rgPw.test(password)) {
        utils.showNotification('Mật khẩu phải có ít nhất 8 ký tự, trong đó có ít nhất 1 ký tự viết hoa', 'error');
        return;
    }
    if (password !== repeatPassword) {
        utils.showNotification('Mật khẩu xác nhận không trùng khớp!', 'error');
        return;
    }
    document.querySelector(".fullscreen-overlay").classList.remove("d-none");


    try {
        const response = await axios.post('http://localhost:8080/api/auth/register', { email, password, repeatPassword });
        if (response.data.error === 0) {
            utils.showNotification(response.data.message, 'success');
            window.location.href = '/login';
        } else {
            utils.showNotification(response.data.message, 'error');
        }
    } catch (error) {
        console.error('Error logging in:', error);
        utils.showNotification(error.response.data.message, 'error');
    }
    document.querySelector(".fullscreen-overlay").classList.add("d-none");
};
