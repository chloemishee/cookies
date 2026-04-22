const stealButton = document.getElementById("steal-button");
const resultBox = document.getElementById("result-box");

if (stealButton && resultBox) {
    stealButton.addEventListener("click", async () => {
        // if the cookie is not HttpOnly, JS can read it here
        // in secure mode the browser should hide session_id from document.cookie
        const visibleCookies = document.cookie;
        const mode = stealButton.dataset.mode;
        const username = stealButton.dataset.username;

        resultBox.textContent =
            "JavaScript can currently see: " + (visibleCookies || "[nothing]");

        try {
            const response = await fetch("/steal", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({
                    stolen_cookie: visibleCookies,
                    mode: mode,
                    username: username,
                }),
            });

            const data = await response.json();

            if (visibleCookies.includes("session_id=")) {
                resultBox.textContent +=
                    "\nAttack result: session cookie was readable and sent to /steal.\n" +
                    "Server reply: " + JSON.stringify(data);
            } else {
                resultBox.textContent +=
                    "\nAttack result: session_id was not available to JavaScript.\n" +
                    "This is what HttpOnly is meant to help with.";
            }
        } catch (error) {
            resultBox.textContent += "\nRequest failed: " + error;
        }
    });
}
