<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Allergen Detection Result</title>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Nunito', sans-serif;
            background-color: #fff0f0;
            color: #2c3e50;
            margin: 0;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding-top: 100px; /* Increased padding to prevent cutting off */
        }
        h1 {
            color: #ff6b6b;
            font-size: 3rem;
            margin-bottom: 50px;
            line-height: 1.2;
        }
        h1 span {
            display: block;
        }
        .content {
            background-color: #ffffff;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 80%;
            max-width: 600px;
            text-align: left;
            line-height: 1.6;
        }
        .content h2 {
            color: #2980b9;
            font-size: 1.8rem;
            margin-bottom: 15px;
        }
        .content ul, .content ol {
            margin-left: 20px;
            margin-top: 10px;
        }
        .content p {
            font-size: 1.2rem;
            margin-top: 15px;
        }
        .back-link {
            margin-top: 30px;
            display: inline-block;
            padding: 15px 20px;
            background-color: #ff6b6b;
            color: white;
            text-decoration: none;
            font-size: 1.2rem;
            border-radius: 5px;
        }
        .back-link:hover {
            background-color: #ff5252;
        }
    </style>
</head>
<body>

    <h1>
        <span>Allergen</span>
        <span>Detection</span>
        <span>Result</span>
    </h1>

    <div class="content">
        {{ result | safe }} <!-- Assuming result contains structured data in Markdown-like format -->
    </div>

    <a href="/" class="back-link">Go back</a>

</body>
</html>
