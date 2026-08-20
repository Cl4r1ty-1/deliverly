const dishSelect = document.getElementById('dishs');
const dishs = new UseBootstrapSelect(dishSelect);

document.getElementById('restaurantID').addEventListener('change', (event) => {
    let restaurant = event.target.value;
    let reqBody = {
        id: restaurant
    }

    fetch(Flask.url_for("forms.get_dishes"), {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(reqBody)
    })
    .then(response => response.json())
    .then(data => {
        dishs.clearValue();

        Array.from(dishSelect.options)
            .filter(option => option.value !== '')
            .forEach(option => option.remove());

        for (let i = 0; i < data.dishes.length; i++) {
            dishs.addOption(data.dishes[i][0], `${data.dishes[i][1]} - \$${data.dishes[i][2]}`);
        }

        dishSelect.disabled = false;
        dishs.update();
    })
    .catch(error => {
        console.error("Error:", error);
    });
});