document.getElementById("generateBtn").addEventListener("click", function() {
    let url = document.getElementById("youtubeUrl").value;
    if (!url.includes("youtube.com") && !url.includes("youtu.be")) {
        alert("Masukkan URL YouTube yang valid!");
        return;
    }

    let videoId = url.split("v=")[1]?.split("&")[0] || url.split("/").pop();
    let thumbnailUrl = `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`;
    document.getElementById("thumbnail").src = thumbnailUrl;
    document.getElementById("title").innerText = "Thumbnail dari video";
    document.getElementById("videoInfo").style.display = "block";
});

document.getElementById("convertBtn").addEventListener("click", function() {
    let duration = document.getElementById("duration").value;
    
    let progressContainer = document.getElementById("progressContainer");
    let progressBar = document.getElementById("progressBar");
    let progressText = document.getElementById("progressText");
    
    progressContainer.style.display = "block";
    let progress = 0;

    let interval = setInterval(() => {
        progress += 10;
        progressBar.style.width = progress + "%";
        progressText.innerText = progress + "%";

        if (progress >= 100) {
            clearInterval(interval);
            showGeneratedClips(duration);
        }
    }, 500);
});

function showGeneratedClips(duration) {
    let clipsContainer = document.getElementById("clipsContainer");
    clipsContainer.innerHTML = "";

    for (let i = 1; i <= 3; i++) {
        let clip = document.createElement("div");
        clip.className = "clip";
        clip.innerHTML = `
            <p>Clip ${i} - Durasi: ${duration} detik</p>
            <video width="100%" controls>
                <source src="https://samplelib.com/lib/preview/mp4/sample-5s.mp4" type="video/mp4">
                Browser Anda tidak mendukung video tag.
            </video>
            <a href="https://samplelib.com/lib/preview/mp4/sample-5s.mp4" download="clip${i}.mp4">
                <button>Download</button>
            </a>
        `;
        clipsContainer.appendChild(clip);
    }
      }
