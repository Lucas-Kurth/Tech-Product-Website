/*
    put this in templates/register.html
    <!-- Link to JavaScript file -->
    <script src="{{ url_for('static', filename='js/register.js') }}"></script>


    make sure 'registerForm' matches whatever <form id = ---> THIS <-----
                          ++++++++ */
document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // This sends JSON to your /api/register endpoint
    const response = await fetch('/api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, email, password })
    });

    const data = await response.json();

    if (data.success) {
        alert('Registration successful!');
        window.location.href = '/login';  // Redirect to login page
    } else {
        alert('Registration failed: ' + data.error);
    }
});