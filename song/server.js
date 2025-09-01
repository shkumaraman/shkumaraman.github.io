const express = require("express");
const fetch = require("node-fetch");
const path = require("path");
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static(path.join(__dirname, "public")));

app.get("/search", async (req, res) => {
  const query = req.query.q;
  if (!query) return res.status(400).json({ error: "Query required" });

  try {
    const apiUrl = `https://saavn.dev/search?query=${encodeURIComponent(query)}`; 
    const response = await fetch(apiUrl);
    const data = await response.json();

    // data.songs should contain proper song objects with audio URLs
    res.json({ songs: data.songs || [] });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Error fetching songs" });
  }
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
