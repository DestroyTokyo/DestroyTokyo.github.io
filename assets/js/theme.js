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

function getRootPath() {
    const path = window.location.pathname;
    const parts = path.replace(/^\/|\/$/g, '').split('/');
    if (parts.length > 0 && parts[parts.length - 1].includes('.')) parts.pop();
    const depth = parts.length;
    return depth === 0 ? '' : '../'.repeat(depth);
}

async function loadAll(rootPath) {
    const themesResponse = await fetch(rootPath + 'jsons/themes.json');
    themes = await themesResponse.json();
    const backgroundsResponse = await fetch(rootPath + 'jsons/backgrounds.json');
    backgrounds = await backgroundsResponse.json();
}

function applyTheme(themeID, rootPath) {
    const theme = themes[themeID];
    if (!theme) return;
    const link = document.getElementById(theme_name);
    if (!link) return;
    link.href = rootPath + 'assets/themes/' + theme;
}

function changeTheme(rootPath) {
    let currentThemeID = parseInt(getCookie('theme'), 10);
    if (isNaN(currentThemeID)) currentThemeID = 0;
    let nextThemeID = currentThemeID + 1;
    if (nextThemeID >= themes.length) nextThemeID = 0;
    applyTheme(nextThemeID, rootPath);
    setCookie(nextThemeID);
}

window.addEventListener('DOMContentLoaded', async () => {
    const rootPath = getRootPath();
    const link = document.getElementById(theme_name);
    
    if (link) link.href = rootPath + 'assets/styles/root.css';

    await loadAll(rootPath);

    let themeID = getCookie('theme');
    if (themeID === null) {
        themeID = 0;
        setCookie(themeID);
    } else themeID = parseInt(themeID, 10);

    applyTheme(themeID, rootPath);
    const button = document.getElementById('theme-button');
    if (button) button.onclick = () => changeTheme(rootPath);
});