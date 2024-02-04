// app.js

// Replace with your Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyBtYxPpS_Nl4uXVUHIYglGgw5NC8vYr7mo",
  authDomain: "chat-a1f20.firebaseapp.com",
  projectId: "chat-a1f20",
  storageBucket: "chat-a1f20.appspot.com",
  messagingSenderId: "462806461629",
  appId: "1:462806461629:web:ed02a01b6d3806fef15bd4",
  measurementId: "G-0EXE84FWPZ"
};

firebase.initializeApp(firebaseConfig);
const database = firebase.database();

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
        
