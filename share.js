// share.js

document.addEventListener("DOMContentLoaded", () => {
  const shareBtn = document.getElementById("shareBtn");

  shareBtn.addEventListener("click", async () => {
    const shareData = {
      title: "TalkRush - Chat With Strangers!",
      text: "Connect with strangers, chat and Talk freely, and explore fun conversations. Try TalkRush now:",
      url: "https://shkumaraman.github.io"
    };

    if (navigator.share) {
      try {
        await navigator.share(shareData);
        console.log("Shared successfully");
      } catch (err) {
        console.error("Error sharing:", err);
      }
    } else {
      // Fallback for browsers that don't support Web Share API
      const whatsappUrl = `https://wa.me/?text=${encodeURIComponent(shareData.text + " " + shareData.url)}`;
      window.open(whatsappUrl, "_blank");
    }
  });
});
