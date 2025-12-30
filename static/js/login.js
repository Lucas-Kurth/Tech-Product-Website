/*
    put this in login.html
    <!-- Link to JavaScript file -->
    <script src="{{ url_for('static', filename='js/login.js') }}"></script>


    make sure 'loginForm' matches whatever <form id = ---> THIS <-----
                         ++++++++ */
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    // This sends JSON to your /api/login endpoint
    const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });
    
    const data = await response.json();
    
    if (data.success) {
        window.location.href = '/';  // Redirect to home
    } else {
        alert('Login failed: ' + data.error);
    }
});
