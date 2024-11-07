export const checkLoginStatusIndexPage = async () => {
  try {
    const response = await axios.get(
      "http://localhost:3006/api/auth/checkStatus"
    );

    if (response.data.error === 0) {
      window.location.href = "/mainPage";
      return;
    }
    window.location.href = "/login";
  } catch (error) {
    console.error("Error checking login status:", error);
    window.location.href = "/login";
  }
};
export const checkLoginStatusMainPage = async () => {
  document.querySelector(".fullscreen-overlay").classList.remove("d-none");
  try {
    const response = await axios.get(
      "http://localhost:3006/api/auth/checkStatus"
    );

    if (response.data.error !== 0) {
      window.location.href = "/login";
      return;
    }
  } catch (error) {
    console.error("Error checking login status:", error);
    window.location.href = "/login";
  }
  document.querySelector(".fullscreen-overlay").classList.add("d-none");
};
export const checkLoginStatusLogin = async () => {
  document.querySelector(".fullscreen-overlay").classList.remove("d-none");
  try {
    const response = await axios.get(
      "http://localhost:3006/api/auth/checkStatus"
    );

    if (response.data.error === 0) {
      window.location.href = "/mainPage";
      return;
    }
  } catch (error) {
    console.error("Error checking login status:", error);
  }
  document.querySelector(".fullscreen-overlay").classList.add("d-none");
};
export const checkLoginStatusRegister = async () => {
  document.querySelector(".fullscreen-overlay").classList.remove("d-none");
  try {
    const response = await axios.get(
      "http://localhost:3006/api/auth/checkStatus"
    );

    if (response.data.error === 0) {
      window.location.href = "/mainPage";
      return;
    }
  } catch (error) {
    console.error("Error checking login status:", error);
  }
  document.querySelector(".fullscreen-overlay").classList.add("d-none");
};
export const checkLoginStatusChangePassword = async () => {
  document.querySelector(".fullscreen-overlay").classList.remove("d-none");
  try {
    const response = await axios.get(
      "http://localhost:3006/api/auth/checkStatus"
    );

    if (response.data.error !== 0) {
      window.location.href = "/login";
      return;
    }
  } catch (error) {
    console.error("Error checking login status:", error);
  }
  document.querySelector(".fullscreen-overlay").classList.add("d-none");
};
