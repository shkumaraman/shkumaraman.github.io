const express = require("express");
const YTMusic = require("ytmusic-api");
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
    const track = await api.getSong(req.params.id);
    res.json(track);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
