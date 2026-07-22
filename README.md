<p align="center">
	<img src="https://raw.githubusercontent.com/Nionim/Nionim/refs/heads/main/image/Project_Void.png" alt="Project~Void background">
</p>

---

```txt
Мега простой Maven репозиторий для DestroyTokyo

Сайт находится в ./site/
dev-мусор в ./.root/
Два скрипта в корне репы:
    Для скачивания джарок и генерации структуры репы для них же.

При добавлении/изменении чего-то из тех папок:
Всё автоматом пушится через Github Pages

Пользуйтесь, а я пойду ромашковый чай пить и спать наконец..

P.S: Посмотреть весь этот шедевр можно по ссылке, которая прям под текстом.
https://github.com/DestroyTokyo/DestroyTokyo.github.io/tree/repo
```

<p align="center" >
    <a href="https://github.com/DestroyTokyo/DestroyTokyo.github.io/tree/repo" target="_blank">Та самая ссылка</a>
</p>

---

```kts
// How to add api to ur project

repositories {
	mavenCentral()
    // Mirror if domain not exists:
    //     https://destroytokyo.github.io/
	maven("https://tokyo.citory.net/")
}

// see versions on: https://tokyo.citory.net/jsons/versions.json
dependencies {
	// example:   delta.cion.tokyo:tokyo:2.2.0-predemo
	// its old version   ->  tokyo-cherry:
    //                              2.1.0-predemo
    //                              2.0.0-predemo
    //                              1.0.0-predemo
	// its first version ->  tokyo-msnt:0.0.0
	compileOnly("delta.cion.tokyo:tokyo:{version}")
}
```

<p align="center" >
    <a href="https://tokyo.citory.net/jsons/versions.json" target="_blank">Maven Content & Build Versions</a>
</p>

---

<p align="center">
    <a href="#">
        <img src="https://img.shields.io/github/last-commit/DestroyTokyo/DestroyTokyo.github.io?display_timestamp=committer&style=flat-square&color=000000"></a>
    <a href="#">
        <img src="https://img.shields.io/github/created-at/DestroyTokyo/DestroyTokyo.github.io?style=flat-square&color=000000"></a>
</p>
