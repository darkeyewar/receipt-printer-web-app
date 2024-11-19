document.getElementById('add-item').addEventListener('click', function () {
    const tbody = document.getElementById('items-list');
    const newRow = document.createElement('tr');
    newRow.className = 'item-row';

    newRow.innerHTML = `
        <td><input type="text" class="item-name" placeholder="Enter item name" required></td>
        <td><input type="number" class="item-quantity" placeholder="Enter quantity" required></td>
        <td><input type="number" step="0.01" class="item-price" placeholder="Enter price" required></td>
        
    `;

    tbody.appendChild(newRow);
});

document.getElementById('receipt-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const customerName = document.getElementById('customer-name').value;
    const rows = document.querySelectorAll('.item-row');
    const items = Array.from(rows).map(row => ({
        name: row.querySelector('.item-name').value,
        quantity: parseInt(row.querySelector('.item-quantity').value),
        price: parseFloat(row.querySelector('.item-price').value)
    }));

    const response = await fetch('/create-receipt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ customerName, items })
    });

    const data = await response.json();
    
    // Create a new window with the formatted receipt
    const printWindow = window.open('', '_blank', 'height=600,width=800');
    printWindow.document.write(data.html_content);
    printWindow.document.close();
    
    // Wait for styles to load
    setTimeout(() => {
        printWindow.print();
        // Close the window after printing (optional)
        // printWindow.close();
    }, 500);
});


