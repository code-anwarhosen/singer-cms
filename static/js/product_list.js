// Form submission handler
const addProductBtn = document.querySelector('button[type="submit"]');
addProductBtn.addEventListener('click', async function(event) {
    event.preventDefault();

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    if (!csrfToken) {
        showToast('CSRF Token not found!');
        console.error('CSRF token not found!');
        return;
    }
    
    const category = document.getElementById('product-category').value;
    const models = document.getElementById('model-number').value;
    
    if (!category) {
        showToast('Please select product category.');
        return;
    }
    if (!models) {
        showToast('Please enter product model number.');
        return;
    }

    addProductBtn.disabled = true;
    addProductBtn.querySelector('span').textContent = 'Creating...';

    const productModels = models.split(';').map(model => model.trim()).filter(model => model !== "");
    await Promise.all(
        productModels.map(async (model) => {
            try {
                const response = await fetch(`/product/create/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({
                        category: category,
                        model: model
                    }),
                });
        
                const result = await response.json();
        
                if (result.status === 'success') {
                    showToast("Success: " + result.message);
                    insertProductIntoTable(result.data);
                } else {
                    showToast("Error: " + result.message);
                }
            } catch (error) {
                console.error('Error:' + error);
                showToast('An error occurred while adding product.');
            }
        })
    );

    document.getElementById('product-category').value = "";
    document.getElementById('model-number').value = "";
    
    addProductBtn.disabled = false;
    addProductBtn.querySelector('span').textContent = 'Add Product';
});


function insertProductIntoTable(product={}) {
    if (!product) {
        return;
    }

    const productHTML = `
        <tr class="product-item">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-100">${product.category}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-100">${product.model.toUpperCase()}</td>
            
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-400">
                <button class="text-blue-400 hover:text-blue-300 mr-3"><i class="fas fa-edit"></i></button>
                <button class="text-red-400 hover:text-red-300"><i class="fas fa-trash"></i></button>
            </td>
        </tr>
    `;

    const tableBody = document.getElementById('product-table-body');
    tableBody.insertAdjacentHTML('beforebegin', productHTML);
}
