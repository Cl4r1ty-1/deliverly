const dishSelect = document.getElementById('dishs');
const cartBody = document.getElementById('cartBody');
const dishs = new UseBootstrapSelect(dishSelect);
const dishData = new Map()
const totalInput = document.getElementById('total');
const deliveryFee = 5.95;

function updateTotal() {
    let total = deliveryFee;

    cartBody.querySelectorAll('tr').forEach(row => {
        const price = Number(row.dataset.price);
        const quantity = Number(row.querySelector('input').value) || 0;

        total += price * quantity;
    });

    totalInput.value = `$${total.toFixed(2)}`;
}

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
        dishData.clear();
        cartBody.replaceChildren();

        Array.from(dishSelect.options)
            .filter(option => option.value !== '')
            .forEach(option => option.remove());

        for (let i = 0; i < data.dishes.length; i++) {
            const [id, name, price] = data.dishes[i];
            dishData.set(String(id), {
                name: name,
                price: price
            })
            dishs.addOption(id, `${name} - \$${price}`);
        }

        dishSelect.disabled = false;
        dishs.update();
    })
    .catch(error => {
        console.error("Error:", error);
    });
});

dishSelect.addEventListener('change', () => {
    cartBody.replaceChildren();
    
    Array.from(dishSelect.selectedOptions).forEach(option => {
        const dishId = option.value;
        const dish = dishData.get(dishId);

        if (!dish) return;

        const row = document.createElement('tr');
        row.dataset.price = dish.price;
        row.innerHTML = `
            <td>${dish.name}</td>
            <td>$${dish.price}</td>
            <td>
                <input
                    class="form-control"
                    type="number"
                    name="quantity_${dishId}"
                    min="1"
                    value="1"
                    required
                >
            </td>
        `;

        cartBody.appendChild(row);
    });

    updateTotal()
})

cartBody.addEventListener('input', event => {
    if (event.target.matches('input[type="number"]')) {
        updateTotal();
    }
});