let themes = [];
let backgrounds = [];

const theme_name = "theme_dc";
const background_name = "background_dc";

function setCookie(themeID) {
    const expires = new Date();
    expires.setFullYear(expires.getFullYear() + 1);
    document.cookie = `theme=${themeID}; expires=${expires.toUTCString()}; path=/`;
}

function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
}

async function loadAll() {
    const themesResponse = await fetch('/jsons/themes.json');
    themes = await themesResponse.json();
    
    const backgroundsResponse = await fetch('/jsons/backgrounds.json');
    backgrounds = await backgroundsResponse.json();
}

function applyTheme(themeID) {
    const theme = themes[themeID];
    if (!theme) return;

    const link = document.getElementById(theme_name);
    if (!link) return;

    let currentHref = link.href;
    let match = currentHref.match(/^(.*?)(?:styles\/|assets\/themes\/)[^\/]+$/);
    if (match) link.href = match[1] + 'assets/themes/' + theme;
    else {
        let basePath = currentHref.substring(0, currentHref.lastIndexOf('/') + 1);
        link.href = basePath + theme;
    }
}

function changeTheme() {
    console.log("1");
    let currentThemeID = parseInt(getCookie('theme'), 10);
    if (isNaN(currentThemeID)) currentThemeID = 0;
    let nextThemeID = currentThemeID + 1;
    if (nextThemeID >= themes.length) nextThemeID = 0;
    applyTheme(nextThemeID);
    setCookie(nextThemeID);
}

window.addEventListener('DOMContentLoaded', async () => {
    await loadAll();
    
    let themeID = getCookie('theme');
    if (themeID === null) {
        themeID = 0;
        setCookie(themeID);
    } else {
        themeID = parseInt(themeID, 10);
    }
    applyTheme(themeID);
    
    const button = document.getElementById('theme-button');
    if (button) button.onclick = changeTheme;
});