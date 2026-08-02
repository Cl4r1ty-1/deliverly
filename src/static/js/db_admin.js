document.getElementById('create_empty_tables').addEventListener('click', () => {
    const output = document.getElementById("init_status");
    output.innerText = "Status: Creating tables...";

    fetch(Flask.url_for("blank"), {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        output.innerText = `Status: ${data.message}`;
    })
    .catch(error => {
        output.innerText = "Status: Error creating tables.";
        console.error('Error:', error);
    });
});


document.getElementById('insert_prod_data').addEventListener('click', () => {
    const output = document.getElementById("p_data_status");
    output.innerText = "Status: Inserting data...";

    fetch(Flask.url_for("prod_data"), {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        output.innerText = `Status: ${data.message}`;
    })
    .catch(error => {
        output.innerText = "Status: Error inserting data.";
        console.error('Error:', error);
    });
});
