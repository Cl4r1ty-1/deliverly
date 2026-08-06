document.getElementById('query_select').addEventListener('change', (event) => {
    const selected_option = event.target.selectedOptions[0];

    if (selected_option.dataset.args == "True") {
        document.getElementById('args_input').disabled = false;
    } else {
        document.getElementById('args_input').disabled = true;
    }

    if (event.target.value != "default") {
        document.getElementById('submit_query').disabled = false;
    } else {
        document.getElementById('submit_query').disabled = true;
    }
    
});

query_form.addEventListener('submit', (event) => {
    event.preventDefault();

    const formData = new FormData(query_form);
    const query_selected = formData.get('query_select');
    const args = formData.get('args_input');

    window.location.href = Flask.url_for('queries.render_query', {"query": query_selected, "args": args});
});