<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>FastAPI JSON Sender</title>
</head>
<body>

    <button id="sendDataButton">Send New JSON Data to FastAPI</button>

    <p id="responseMessage"></p>

    <script>
        document.getElementById('sendDataButton').addEventListener('click', function() {
            // Define the JSON payload as a JavaScript object
            const dataToSend = {
                "report_id": "A478",
                "temperature": 72.5,
                "is_active": true 
            };

            // The URL of your FastAPI endpoint
            const fastapiEndpoint = 'http://127.0.0.1:8000/submit/'; 

            // Use the fetch API to send the POST request
            fetch(fastapiEndpoint, {
                method: 'POST', // Critical
                headers: {
                    // Critical: Tell the server the body is JSON
                    'Content-Type': 'application/json'
                },
                // Convert the JavaScript object to a JSON string
                body: JSON.stringify(dataToSend) 
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Success:', data);
                document.getElementById('responseMessage').textContent = `Success: ${data.message}`;
            })
            .catch((error) => {
                console.error('Error:', error);
                document.getElementById('responseMessage').textContent = `Error: ${error.message}`;
            });
        });
    </script>
</body>
</html>
