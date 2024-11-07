import { checkLoginStatusChangePassword } from "./checkStatus.js";
import * as utils from "./utils.js";
import { rgPw } from "./regex.js";
checkLoginStatusChangePassword();
document
  .getElementById("changePasswordForm")
  .addEventListener("submit", async event => {
    event.preventDefault();
    await changePassword();
  });
const changePassword = async () => {
  const password = document.getElementById("form2Example1").value;
  const newPassword = document.getElementById("form2Example2").value;
  const repeatPassword = document.getElementById("form2Example3").value;
  if (!password || !newPassword || !repeatPassword) {
    utils.showNotification("Vui lòng điền đầy đủ thông tin!", "error");
    return;
  }
  if (!rgPw.test(newPassword)) {
    utils.showNotification(
      "Mật khẩu phải có ít nhất 8 ký tự, trong đó có ít nhất 1 ký tự viết hoa",
      "error"
    );
    return;
  }
  if (newPassword !== repeatPassword) {
    utils.showNotification("Mật khẩu xác nhận không trùng khớp!", "error");
    return;
  }
  document.querySelector(".fullscreen-overlay").classList.remove("d-none");
  try {
    const response = await axios.put(
      "http://localhost:3006/api/user/change-password",
      {
        password,
        newPassword,
        repeatPassword,
      }
    );
    if (response.data.error === 0) {
      utils.showNotification(response.data.message, "success");
    } else {
      utils.showNotification(response.data.message, "error");
    }
  } catch (error) {
    console.error("Error changing password:", error);
    utils.showNotification(error.response.data.message, "error");
  }
  document.querySelector(".fullscreen-overlay").classList.add("d-none");
};
