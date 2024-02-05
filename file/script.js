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

// Check username availability
function checkAvailability() {
  const username = document.getElementById('username').value;

  // Implement Firebase logic to check username availability
  // Show suggestion if username is not available
  document.getElementById('suggestion').innerText = 'Suggested username: ' + username + '123';
}

// Open wallet page
function openWalletPage() {
  document.getElementById('registration-page').style.display = 'none';
  document.getElementById('wallet-page').style.display = 'block';
}

// Deposit/Withdraw from wallet
function depositWithdraw() {
  const amount = parseFloat(document.getElementById('amount').value);
  
  // Implement Firebase logic for wallet transactions
  // Update wallet balance and transaction history
  document.getElementById('wallet-balance').innerText = 'Balance: $' + amount;
}
