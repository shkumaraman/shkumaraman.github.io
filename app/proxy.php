<?php
// Web Proxy Script in PHP

// Target URL jo aap access karna chahte hain
if (isset($_GET['url'])) {
    $url = $_GET['url'];
} else {
    die("URL parameter missing. Usage: proxy.php?url=http://example.com");
}

// Validate URL
if (!filter_var($url, FILTER_VALIDATE_URL)) {
    die("Invalid URL format.");
}

// cURL ka use karke content fetch karna
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false); // SSL verify disable (for testing only)
curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3');

$response = curl_exec($ch);

// Check for errors
if (curl_errno($ch)) {
    die("Error: " . curl_error($ch));
}

// Content type header set karna
$contentType = curl_getinfo($ch, CURLINFO_CONTENT_TYPE);
header("Content-Type: $contentType");

// Response ko display karna
echo $response;

// cURL session close karna
curl_close($ch);
?>
