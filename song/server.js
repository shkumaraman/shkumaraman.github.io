const express = require("express");
const YTMusic = require("ytmusic-api");
const ytdl = require("ytdl-core");
const cors = require("cors");

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());

const api = new YTMusic();
(async () => {
  await api.initialize();
})();

app.get("/search", async (req, res) => {
  try {
    const query = req.query.q;
    const results = await api.search(query);
    res.json(results);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get("/song/:id", async (req, res) => {
  try {
    const videoId = req.params.id;
    const info = await ytdl.getInfo(videoId);

    // केवल audio formats filter करें
    const format = ytdl.chooseFormat(info.formats, { filter: "audioonly" });

    res.json({
      title: info.videoDetails.title,
      artist: info.videoDetails.author.name,
      url: format.url
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
        
