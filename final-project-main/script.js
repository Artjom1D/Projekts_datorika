// Funkcija, lai parādītu kļūdas ziņojumu
function displayError(message) {
    const errorElement = document.getElementById('error');
    if (errorElement) {
        errorElement.innerText = message;
    }
}

// Funkcija, lai validētu pieteikšanās formu
function validateLoginForm(email, password) {
    if (!email || !password) {
        displayError('Lūdzu, aizpildiet visus laukus.');
        return false;
    }
    return true;
}

// Funkcija, lai pievienotu notikumu klausītāju pieteikšanās formai
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('.login');
    if (loginForm) {
        loginForm.addEventListener('submit', (event) => {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            if (!validateLoginForm(email, password)) {
                event.preventDefault(); // Novērš formas iesniegšanu, ja validācija neizdodas
            }
        });
    }
});
