// Firebase configuration
// Replace with your own Firebase config
const firebaseConfig = {
  apiKey: "your-api-key",
  authDomain: "your-auth-domain",
  projectId: "your-project-id",
  storageBucket: "your-storage-bucket",
  messagingSenderId: "your-messaging-sender-id",
  appId: "your-app-id"
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
