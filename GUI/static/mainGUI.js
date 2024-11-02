import { checkLoginStatusMainPage } from "./checkStatus.js";
import * as utils from "./utils.js";
checkLoginStatusMainPage();

document.getElementById("logout").addEventListener("click", async (event) => {
  event.preventDefault();
  await logout();
});
const logout = async () => {
  document.querySelector(".fullscreen-overlay").classList.remove("d-none");
  try {
    const response = await axios.get("http://localhost:8080/api/auth/logout");
    if (response.data.error === 0) {
      window.location.href = "/mainPage";
    } else {
      utils.showNotification(response.data.message, "error");
    }
  } catch (error) {
    console.error("Error logging in:", error);
    utils.showNotification(error.response.data.message, "error");
  }
  document.querySelector(".fullscreen-overlay").classList.add("d-none");
};
