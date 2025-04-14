const apiKey = window.GIPHY_API_KEY || "";
const username = "blinkies"; 
const changeOnRefresh = true; 
const refreshHours = 6;

function getGifOffset() {
    if (changeOnRefresh) {
        return Math.floor(Math.random() * 50); // New GIF every refresh
    } else {
        const lastUpdate = localStorage.getItem("lastGifUpdate");
        const currentTime = Date.now();
        const hoursSinceLastUpdate = lastUpdate ? (currentTime - lastUpdate) / (1000 * 60 * 60) : refreshHours;

        if (!lastUpdate || hoursSinceLastUpdate >= refreshHours) {
            localStorage.setItem("lastGifUpdate", currentTime);
            localStorage.setItem("gifOffset", Math.floor(Math.random() * 50));
        }
        return localStorage.getItem("gifOffset");
    }
}

async function fetchGif() {
    const offset = getGifOffset();
    const url = `https://api.giphy.com/v1/gifs/search?api_key=${apiKey}&q=&username=${username}&limit=1&offset=${offset}`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        if (data.data.length > 0) {
            const gifElement = document.getElementById("gif");
            gifElement.src = data.data[0].images.original.url;
        } else {
            document.getElementById("gif").alt = "No GIF found.";
        }
    } catch (error) {
        console.error("Error fetching GIF:", error);
        document.getElementById("gif").alt = "Error loading GIF.";
    }
}

document.addEventListener('DOMContentLoaded', function() {
    fetchGif();
});