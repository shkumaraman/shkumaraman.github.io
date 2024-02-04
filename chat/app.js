// app.js

// Replace with your Firebase configuration
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_AUTH_DOMAIN",
    databaseURL: "YOUR_DATABASE_URL",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_STORAGE_BUCKET",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID"
};

firebase.initializeApp(firebaseConfig);
const database = firebase.database();
// app.js continued

const chatMessages = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');

document.getElementById('send-message').addEventListener('click', () => {
    const message = messageInput.value;
    sendMessage(message);
});

function sendMessage(message) {
    database.ref('messages').push({
        message: message
    });
    messageInput.value = '';
}

database.ref('messages').on('child_added', (snapshot) => {
    const message = snapshot.val().message;
    chatMessages.innerHTML += `<div>${message}</div>`;
});
