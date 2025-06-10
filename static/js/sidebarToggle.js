document.addEventListener("DOMContentLoaded", function () {
    const body = document.querySelector("body"),
        sidebar = document.getElementById("navBar"),
        toggle = document.querySelector(".sidebar-toggle"),
        modeSwitch = document.querySelector(".mode-toggle");

    let darkMode = localStorage.getItem("mode");
    if (darkMode && darkMode === "dark") {
        body.classList.add("dark");
    } else {
        body.classList.remove("dark");
    }

    let sidebarStatus = localStorage.getItem("status");
    if (sidebarStatus && sidebarStatus === "close") {
        sidebar.classList.add("close");
        body.classList.add("sidebar-closed");
    }else {
        sidebar.classList.remove("close");
        body.classList.remove("sidebar-closed");
    }
    
    toggle.addEventListener("click", () => {
        sidebar.classList.toggle("close");
        body.classList.toggle("sidebar-closed");
        localStorage.setItem("status", sidebar.classList.contains("close") ? "close" : "open");
    });

    modeSwitch.addEventListener("click", () => {
        body.classList.toggle("dark");
        localStorage.setItem("mode", body.classList.contains("dark") ? "dark" : "light");
    });

});
