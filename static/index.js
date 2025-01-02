document.addEventListener("DOMContentLoaded", function () {
    const entries = document.getElementById("entries");

    // Fetch data from the Flask API
    /*fetch("/entries")
        .then(response => response.json())
        .then(entries => {
            entries.forEach(entry => {
                // Create list item for each entry
                const listItem = document.createElement("li");
                listItem.innerHTML = `
                    <a href="/view/${entry.id}">${entry.title}</a> 
                    (<a href="/edit/${entry.id}">Edit</a>) 
                    <button onclick="deleteEntry(${entry.id})">Delete</button>
                `;
                contentList.appendChild(listItem);
            });
        });*/
});
