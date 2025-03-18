document.getElementById("video-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    let youtubeUrl = document.getElementById("youtube-url").value;
    let duration = document.getElementById("duration").value;
    let outputDiv = document.getElementById("output");

    outputDiv.innerHTML = "<p>Processing...</p>";

    let response = await fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ youtube_url: youtubeUrl, duration: duration })
    });

    let data = await response.json();
    outputDiv.innerHTML = `<img src="${data.thumbnail}" width="320"><br>
                            <button onclick="convert()">Convert to Clips</button>`;
});

async function convert() {
    let outputDiv = document.getElementById("output");
    outputDiv.innerHTML = "<p>Converting...</p>";

    let response = await fetch("/convert", { method: "POST" });
    let data = await response.json();
    outputDiv.innerHTML = "<p>" + data.message + "</p>";
}
