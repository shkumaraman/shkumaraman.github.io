window.getBotUsers = function() {
  const bots = {
    "Sneha24": { nickname: "Sneha24", gender: "female", country: "🇮🇳 India" },
    "pooja@chat": { nickname: "pooja@chat", gender: "female", country: "🇮🇳 India" },
    "KavyaV": { nickname: "KavyaV", gender: "female", country: "🇮🇳 India" },
    "emma_rose": { nickname: "emma_rose", gender: "female", country: "🇺🇸 United States" },
    "@chloestar": { nickname: "@chloestar", gender: "female", country: "🇦🇺 Australia" },
    "ZaraQueen": { nickname: "ZaraQueen", gender: "female", country: "🇬🇧 United Kingdom" },
    "riya99_": { nickname: "riya99_", gender: "female", country: "🇮🇳 India" },
    "RahulDev": { nickname: "RahulDev", gender: "male", country: "🇮🇳 India" },
    "aman@live": { nickname: "aman@live", gender: "male", country: "🇮🇳 India" },
    "Alex_07": { nickname: "Alex_07", gender: "male", country: "🇺🇸 United States" }
  };

  const now = Date.now();
  const threeHoursInMs = 3 * 60 * 60 * 1000;

  for (let key in bots) {
    bots[key].timestamp = now - Math.floor(Math.random() * threeHoursInMs);
  }

  return bots;
};
