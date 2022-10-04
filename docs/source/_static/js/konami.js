function addKonamiCode() {
    let cursor = 0;
    const KONAMI = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65];

    const WORD = String.fromCharCode.apply(null, [42, 16, 11, 12, 27].map((v) => v ^ 0x69));

    window.addEventListener("keydown", (e) => {
        cursor = (e.keyCode == KONAMI[cursor]) ? cursor + 1 : 0;
        if (cursor == KONAMI.length) {
            // https://stackoverflow.com/a/61198587
            for (const parent of document.querySelectorAll("body *")) {
                for (const child of parent.childNodes) {
                    if (child.nodeType === Node.TEXT_NODE) {
                        const pattern = /Dissect/g;

                        const replacement = `<span class="konami-glitch" style="animation-delay: ${Math.random()}s;" data-text="${WORD}">${WORD}</span>`;
                        const subNode = document.createElement("span");
                        subNode.innerHTML = child.textContent.replace(pattern, replacement);
                        parent.insertBefore(subNode, child);
                        parent.removeChild(child);
                    }
                }
            }
            for (let el of document.getElementsByClassName("sidebar-logo")) {
                el.src = el.src.replace(/logo-.+\.svg/, "logo-konami.svg")
            }
        }
    });
}

addKonamiCode()
