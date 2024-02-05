// Firebase configuration
// Replace with your own Firebase config
const firebaseConfig = {
  apiKey: "AIzaSyDjoMP3bybVOAbfO5SG06RAPZKU7F8zsQs",
  authDomain: "myapp-33961.firebaseapp.com",
  projectId: "myapp-33961",
  storageBucket: "myapp-33961.appspot.com",
  messagingSenderId: "266302156367",
  appId: "1:266302156367:web:9595eb5ad03adb7950843a",
  measurementId: "G-YQCNYER0EK"
};


// Initialize Firebase
firebase.initializeApp(firebaseConfig);

const db = firebase.firestore();
let currentUser;

// Check username availability and register user
function checkAvailability() {
  const username = document.getElementById('username').value;

  db.collection("users").where("username", "==", username)
    .get()
    .then((querySnapshot) => {
      if (querySnapshot.empty) {
        // Username is available, register the user
        registerUser(username);
      } else {
        // Username is not available, suggest a new one
        document.getElementById('suggestion').innerText = 'Suggested username: ' + username + '123';
      }
    })
    .catch((error) => {
      console.error("Error checking username availability: ", error);
    });
}

// Register user and open wallet page
function registerUser(username) {
  firebase.auth().createUserWithEmailAndPassword(username + "@example.com", "password")
    .then((userCredential) => {
      currentUser = userCredential.user;
      // Save user data to Firestore
      db.collection("users").doc(currentUser.uid).set({
        username: username,
        walletBalance: 0
      })
      .then(() => {
        openWalletPage();
      })
      .catch((error) => {
        console.error("Error saving user data: ", error);
      });
    })
    .catch((error) => {
      console.error("Error registering user: ", error);
    });
}

// Open wallet page
function openWalletPage() {
  document.getElementById('registration-page').style.display = 'none';
  document.getElementById('wallet-page').style.display = 'block';
}
