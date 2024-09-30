// Function to get CSRF token from cookies
function getCSRFToken() {
    let cookieValue = null;
    const cookies = document.cookie.split(';');
    cookies.forEach(cookie => {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            cookieValue = decodeURIComponent(value);
        }
    });
    return cookieValue;
}

// Get the input fields and elements
const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid_feedback");
const emailField = document.querySelector("#emailField");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const submitBtn = document.querySelector(".submit-btn");

// Get the password input and checkbox element
const passwordField = document.querySelector("#passwordField");
const showPasswordCheckbox = document.querySelector("#showPasswordCheckbox");

const handleToggleInput = (e) => {
    if (showPasswordCheckbox.checked) {
        passwordField.setAttribute("type", "text");
    } else {
        passwordField.setAttribute("type", "password");
    }
};

// Add event listener for the checkbox toggle
showPasswordCheckbox.addEventListener('change', handleToggleInput);

// Email validation event listener
emailField.addEventListener("keyup", (e) => {
    const emailVal = e.target.value;

    // Feedback for checking
    usernameSuccessOutput.textContent = `Checking ${emailVal}`;
    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display = "none";

    if (emailVal.length > 0) {
        const csrftoken = getCSRFToken(); // Get the CSRF token
        fetch("/authentication/validate-email", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken // Include CSRF token in headers
            },
            body: JSON.stringify({ email: emailVal }), // Correct email value sent
        })
        .then(res => res.json())
        .then((data) => {
            console.log('data', data);
            if (data.email_error) {
                submitBtn.disabled = true;
                emailField.classList.add("is-invalid");
                emailFeedBackArea.style.display = "block";
                emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`; // Corrected template literal
            } else {
                submitBtn.removeAttribute('disabled');
            }
        });
    }
});

// Username validation event listener
usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;

    usernameSuccessOutput.style.display = 'block';
    usernameSuccessOutput.textContent = `Checking ${usernameVal}`; // Corrected template literal

    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display = "none";

    if (usernameVal.length > 0) {
        const csrftoken = getCSRFToken(); // Get the CSRF token

        fetch("/authentication/validate-username", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken // Include CSRF token in headers
            },
            body: JSON.stringify({ username: usernameVal }),
        })
        .then(res => res.json())
        .then((data) => {
            console.log('data', data);

            if (data.username_error) {
                usernameField.classList.add("is-invalid");
                feedBackArea.style.display = "block";
                feedBackArea.innerHTML = `<p>${data.username_error}</p>`; // Corrected template literal
                submitBtn.disabled = true;
            } else {
                submitBtn.removeAttribute('disabled');
            }
        });
    }
});
