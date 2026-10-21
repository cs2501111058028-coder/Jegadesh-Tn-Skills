const generateButton = document.getElementById("generate");
const storyInput = document.getElementById("story");
const genreInput = document.getElementById("genre");
const panelsInput = document.getElementById("panels");
const comic = document.getElementById("comic");
const statusText = document.getElementById("status");
const downloadButton = document.getElementById("download");

let currentStory = "";

generateButton.addEventListener("click", async function () {
  const idea = storyInput.value.trim();

  if (!idea) {
    statusText.textContent = "Please enter your story idea first!";
    storyInput.focus();
    return;
  }

  generateButton.disabled = true;
  statusText.textContent = "AI is writing your comic story...";
  comic.replaceChildren();
  downloadButton.hidden = true;

  try {
    const response = await fetch("/api/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        idea: idea,
        genre: genreInput.value,
        panels: Number(panelsInput.value)
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Story generation failed.");
    }

    currentStory = data.story;

    const card = document.createElement("article");
    card.className = "panel";

    const title = document.createElement("h3");
    title.textContent = data.title;

    const genre = document.createElement("p");
    genre.textContent = "Genre: " + data.genre;

    const story = document.createElement("p");
    story.style.whiteSpace = "pre-wrap";
    story.textContent = data.story;

    card.append(title, genre, story);
    comic.appendChild(card);

    statusText.textContent = "Your AI story is ready!";
    downloadButton.hidden = false;

  } catch (error) {
    statusText.textContent = error.message;
  } finally {
    generateButton.disabled = false;
  }
});

downloadButton.addEventListener("click", function () {
  if (!currentStory) return;

  const file = new Blob([currentStory], {
    type: "text/plain;charset=utf-8"
  });

  const url = URL.createObjectURL(file);
  const link = document.createElement("a");

  link.href = url;
  link.download = "ComicCraft-AI-Story.txt";
  link.click();

  URL.revokeObjectURL(url);
});
