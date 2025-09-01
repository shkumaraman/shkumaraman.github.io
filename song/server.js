const express = require("express");
const fetch = require("node-fetch");
const path = require("path");
const app = express();
const PORT = process.env.PORT || 3000;

// Static frontend folder
app.use(express.static(path.join(__dirname, "public")));

// JioSaavn search endpoint (unofficial)
app.get("/search", async (req, res) => {
  const query = req.query.q;
  if(!query) return res.status(400).json({error: "Query required"});

  try {
    const apiUrl = `https://www.jiosaavn.com/api.php?__call=search.getResults&query=${encodeURIComponent(query)}&_format=json`;
    const response = await fetch(apiUrl);
    let text = await response.text();

    // JioSaavn response weird format remove
    text = text.replace(")]}'", "");
    const data = JSON.parse(text);

    if(!data.results || !data.results.songs) return res.json({songs: []});

    const songs = data.results.songs.map(s => ({
      id: s.id,
      name: s.name,
      artist: s.singers,
      album: s.album,
      media_url: s.media_preview_url || s.media_url
    }));

    res.json({songs});
  } catch(err) {
    console.error(err);
    res.status(500).json({error: "Error fetching songs"});
  }
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
