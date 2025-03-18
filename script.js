async function processVideo() {
    let videoUrl = document.getElementById("videoUrl").value;
    let duration = document.getElementById("duration").value;
    let videoId = getYouTubeId(videoUrl);

    if (!videoId) {
        alert("URL tidak valid!");
        return;
    }

    // Munculkan animasi loading
    document.getElementById("loadingContainer").style.display = "block";
    document.getElementById("clipsContainer").innerHTML = "";

    // Tampilkan thumbnail
    let thumbnailUrl = `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`;
    document.getElementById("thumbnailContainer").innerHTML = `<img src="${thumbnailUrl}" width="300">`;

    // Simulasi Proses (Agar Terlihat Natural)
    setTimeout(async () => {
        let clips = await getBestMoments(videoUrl, duration);
        let clipsHtml = "";
        clips.forEach((clip, index) => {
            let randomStart = Math.floor(Math.random() * 180); // Acak start time
            let videoClipUrl = `https://www.youtube.com/embed/${videoId}?start=${randomStart}`;
            clipsHtml += `
                <div class="clip-item">
                    <iframe width="100%" height="200" src="${videoClipUrl}" frameborder="0" allowfullscreen></iframe>
                    <a href="${videoClipUrl}" target="_blank" class="download-btn">Download Clip ${index + 1}</a>
                </div>
            `;
        });

        document.getElementById("clipsContainer").innerHTML = clipsHtml;

        // Hilangkan animasi loading
        document.getElementById("loadingContainer").style.display = "none";
    }, 3000);
}

function getYouTubeId(url) {
    let match = url.match(/(?:youtube\.com\/(?:[^\/]+\/[^\/]+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/);
    return match ? match[1] : null;
}

async function getBestMoments(videoUrl, duration) {
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
    return data.choices[0].message.content.split("\n");
}
