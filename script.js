async function generate() {
    let videoUrl = document.getElementById("videoUrl").value;
    let videoId = getYouTubeId(videoUrl);

    if (!videoId) {
        alert("URL tidak valid!");
        return;
    }

    document.getElementById("loading").style.display = "block";

    let thumbnailUrl = `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`;
    document.getElementById("thumbnailContainer").innerHTML = `<img src="${thumbnailUrl}" width="300">`;

    document.getElementById("loading").style.display = "none";
}

function getYouTubeId(url) {
    let match = url.match(/(?:youtube\.com\/(?:[^\/]+\/[^\/]+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/);
    return match ? match[1] : null;
}

async function convertToClips() {
    let videoUrl = document.getElementById("videoUrl").value;
    let duration = document.getElementById("duration").value;
    let apiKey = "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"; // Ganti dengan API key OpenAI kamu

    let response = await fetch("https://api.openai.com/v1/chat/completions", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${apiKey}`
        },
        body: JSON.stringify({
            model: "gpt-4",
            messages: [{ role: "user", content: `Cari momen terbaik dari video ini: ${videoUrl}, durasi: ${duration}` }]
        })
    });

    let data = await response.json();
    let clips = data.choices[0].message.content.split("\n");

    let clipsHtml = "";
    clips.forEach(clip => {
        clipsHtml += `<p>${clip}</p>`;
    });

    document.getElementById("clipsContainer").innerHTML = clipsHtml;
      }
