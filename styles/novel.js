document.addEventListener("DOMContentLoaded", () => {
    const nav = document.querySelector(".md-nav");
    let timeout;
    
    const hideNav = () => {
        nav.style.transform = "translateX(-100%)";
        nav.style.transition = "transform 0.3s ease-in-out";
    };

    const showNav = () => {
        nav.style.transform = "translateX(0)";
        nav.style.transition = "transform 0.3s ease-in-out";
    };

    const resetTimeout = () => {
        clearTimeout(timeout);
        showNav();
        timeout = setTimeout(hideNav, 3000);
    };

    document.addEventListener("mousemove", resetTimeout);
    document.addEventListener("keydown", resetTimeout);

    nav.addEventListener("mouseenter", showNav);

    nav.addEventListener("mouseleave", resetTimeout);

    timeout = setTimeout(hideNav, 3000);
});

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("pre code.language-zii").forEach((block) => {
        let lines = block.innerHTML.split("\n");
        let chatbox = document.createElement("div");
        chatbox.className = "chatbox";
        
        lines.forEach(line => {
            line = line.trim()
            if (line === "") return;

            let timestampMatch = line.match(/^\[(\d{2}:\d{2})\]\s*/);
            let timestamp = timestampMatch ? timestampMatch[1] : null;
            console.log(timestamp)
            line = line.replace(/^\[\d{2}:\d{2}\]\s*/, "");

            console.log(line)

            let nicknameMatch = line.match(/^([^:]+):\s*(.*)/);
            let nickname = nicknameMatch ? nicknameMatch[1].trim() : null;
            let messageText = nicknameMatch ? nicknameMatch[2].trim() : line.trim();

            let messageType = "chat-message";
            if (nickname) {
                if (nickname.startsWith('"')) {
                    nickname = nickname.replace('"', "Robinson->");
                    messageType = "private-message";
                } else if (nickname.endsWith('"')) {
                    nickname = nickname.replace('"', "->Robinson");
                    messageType = "private-message";
                } else if (nickname.startsWith("!")) {
                    messageType = "shout-message";
                } else if (nickname.startsWith("+")) {
                    messageType = "trade-message";
                } else if (nickname.startsWith("#")) {
                    messageType = "party-message";
                } else if (nickname.startsWith("@")) {
                    messageType = "clan-message";
                } else if (nickname.startsWith("$")) {
                    messageType = "alliance-message";
                }
            }

            let message = document.createElement("div");
            message.className = `message ${messageType}`;

            if (timestamp) {
                let timestampSpan = document.createElement("span");
                timestampSpan.className = "timestamp";
                timestampSpan.textContent = `[${timestamp}] `;
                message.appendChild(timestampSpan);
            }

            if (nickname) {
                let nicknameStrong = document.createElement("strong");
                nicknameStrong.textContent = `${nickname}: `;
                message.appendChild(nicknameStrong);
            }

            let textSpan = document.createElement("span");
            textSpan.textContent = messageText;
            message.appendChild(textSpan);
            chatbox.appendChild(message);
        });

        block.parentNode.replaceWith(chatbox);
    });
});