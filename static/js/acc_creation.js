// Centralized DOM references
const UIDOM = {
    // Modals
    findModal: document.getElementById('findModal'),
    createCustomerModal: document.getElementById('createCustomerModal'),
    customerList: document.getElementById('customerList'),
    searchInput: document.getElementById('searchInput'),

    customerUid: document.getElementById('customerUid'),

    // Product Selection
    productCategory: document.getElementById('productCategory'),
    modelList: document.getElementById('modelList'),
    selectedModel: document.getElementById('selectedModel'),
    selectedModelName: document.getElementById('selectedModelName'),
    modelFilter: document.getElementById('modelFilter'),

    // Form Submission
    createAccountBtn: document.getElementById('createAccountBtn'),
    accountNumber: document.getElementById('accountNumber'),
    saleDate: document.getElementById('saleDate'),
    cashValue: document.getElementById('cashValue'),
    hireValue: document.getElementById('hireValue'),
    downPayment: document.getElementById('downPayment'),
    monthlyPayment: document.getElementById('monthlyPayment'),
    length: document.getElementById('length'),
};


setSaleDate(UIDOM.saleDate);


// Global data storage
let APP_DATA = {
    customers: [],
    productCategories: [],
    products: []
};


// Fetch initial data from Django backend
async function fetchInitialData() {
    try {
        const response = await fetch('/account/precreation-data/');
        const result = await response.json();

        if (result.success) {
            APP_DATA = {
                customers: result.data.customers || [],
                productCategories: result.data.productCategories || [],
                products: result.data.products || []
            };

            // Populate product categories dropdown
            UIDOM.productCategory.innerHTML = '<option value="">Select Category</option>';
            APP_DATA.productCategories.forEach(category => {
                const option = document.createElement('option');
                option.value = category.value;
                option.textContent = category.name;
                UIDOM.productCategory.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error fetching initial data:', error);
        showToast('Failed to fetch initial data. Please try again.');
    }
}



// Populate customer/guarantor list in find modal
function populateCustomerList() {
    try {
        UIDOM.customerList.innerHTML = ''; // Clear existing items
        const data = APP_DATA.customers;

        data.forEach(item => {
            const listItem = document.createElement('div');
            listItem.className = 'px-4 py-2 hover:bg-gray-700 cursor-pointer';
            listItem.innerHTML = `
                <div class="flex items-center space-x-4">
                    <div class="h-12 w-12 rounded-full bg-gray-600"></div>
                    <div>
                        <div class="font-semibold">${item.name}</div>
                        <div class="text-sm text-gray-400">${item.phone}</div>
                        <div class="text-sm text-gray-400">UID: ${item.uid}</div>
                    </div>
                </div>
            `;
            listItem.onclick = () => handleCustomerSelection(item);
            UIDOM.customerList.appendChild(listItem);
        });
    } catch (error) {
        console.error('Error populating list:', error);
        showToast('Failed to populate list. Please try again.');
    }
}




// Handle customer/guarantor selection
function handleCustomerSelection(item) {
    if (item) {
        UIDOM.customerUid.value = item.uid;
        fetchCustomerDetails(item.uid);
        closeFindModal();
    }
}




// Fetch customer details
function fetchCustomerDetails(uid='', isNewCus=false, newCustomer={}) {
    
    let customer = APP_DATA.customers.find(cust => cust.uid == uid);

    if (isNewCus) {
        customer = newCustomer;
        UIDOM.customerUid.value = customer.uid;
    }

    const customerDetails = document.getElementById('customerDetails');
    if (customer) {
        customerDetails.classList.remove('hidden');
        document.getElementById('custName').textContent = customer.name;
        document.getElementById('custPhone').textContent = customer.phone;
        document.getElementById('custAddress').textContent = customer.address;
    } else {
        customerDetails.classList.add('hidden');
    }
}


// Populate product models based on selected category
function populateProductModels(category) {
    UIDOM.modelList.innerHTML = '';
    const filteredProducts = APP_DATA.products.filter(product => product.category === category);

    filteredProducts.forEach(product => {
        const modelItem = document.createElement('div');
        modelItem.className = 'p-2 hover:bg-gray-500 cursor-pointer';
        modelItem.textContent = product.model;
        modelItem.onclick = () => {
            UIDOM.selectedModel.classList.remove('hidden');
            UIDOM.selectedModelName.textContent = product.model;
        };
        UIDOM.modelList.appendChild(modelItem);
    });
}

// Handle product category change
UIDOM.productCategory.addEventListener('change', (e) => {
    populateProductModels(e.target.value);
});


// Handle search input in find modal
UIDOM.searchInput.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    const items = document.querySelectorAll('#customerList > div');

    items.forEach(item => {
        const name = item.querySelector('.font-semibold').textContent.toLowerCase();
        const phone = item.querySelector('.text-sm').textContent.toLowerCase();
        if (name.includes(searchTerm) || phone.includes(searchTerm)) {
            item.classList.remove('hidden');
        } else {
            item.classList.add('hidden');
        }
    });
});



// Handle model filter input
UIDOM.modelFilter.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    const models = document.querySelectorAll('#modelList > div');

    models.forEach(model => {
        if (model.textContent.toLowerCase().includes(searchTerm)) {
            model.classList.remove('hidden');
        } else {
            model.classList.add('hidden');
        }
    });
});



// Modal Handling
function openFindModal() {
    UIDOM.findModal.classList.add('open');
    populateCustomerList();
}

function closeFindModal() {
    UIDOM.findModal.classList.remove('open');
}

function openCreateCustomerModal() {
    UIDOM.createCustomerModal.classList.add('open');
}

function closeCreateCustomerModal() {
    UIDOM.createCustomerModal.classList.remove('open');
}


// Handle Create Customer Form Submission
async function handleCreateCustomerSubmit(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    const submitButton = event.target.querySelector('button[type="submit"]');
    submitButton.disabled = true;
    submitButton.innerHTML = 'Creating...';

    try {
        const response = await fetch('/customer/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': data.csrfmiddlewaretoken,
            },
            body: JSON.stringify(data),
        });

        const result = await response.json();

        if (result.status === 'success') {
            showToast("Success: " + result.message);
            APP_DATA.customers.push(result.customer);

            event.target.reset();
            closeCreateCustomerModal();
            fetchCustomerDetails("", true, result.customer);
        } else {
            showToast("Error: " + result.message);
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('An error occurred while creating the customer.');
    } finally {
        submitButton.disabled = false;
        submitButton.innerHTML = 'Create';
    }
}


// Submit Form
async function submitForm() {

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    if (!csrfToken) {
        console.error('CSRF token not found!');
        return;
    }

    const formData = {
        accountNumber: UIDOM.accountNumber.value,
        saleDate: UIDOM.saleDate.value,
        customerUid: UIDOM.customerUid.value,
        productCategory: UIDOM.productCategory.value,
        selectedModel: UIDOM.selectedModelName.textContent,
        cashValue: UIDOM.cashValue.value,
        hireValue: UIDOM.hireValue.value,
        downPayment: UIDOM.downPayment.value,
        monthlyPayment: UIDOM.monthlyPayment.value,
        length: UIDOM.length.value,
    };

    // Validate form data
    for (const [key, value] of Object.entries(formData)) {
        if (!value) {
            showToast(`Please fill in the "${key}" field.`);
            return;
        }
    }

    UIDOM.createAccountBtn.disabled = true;
    UIDOM.createAccountBtn.innerHTML = 'Submitting...';

    try {
        const response = await fetch('/account/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(formData),
        });

        const result = await response.json();

        if (result.status === 'success') {
            showToast("Success: " + result.message);

            UIDOM.accountNumber.value = '';
            UIDOM.customerUid.value = '';
            UIDOM.productCategory.value = '';
            UIDOM.selectedModelName.textContent = '';

            UIDOM.cashValue.value = '';
            UIDOM.hireValue.value = '';
            UIDOM.downPayment.value = '';
            UIDOM.monthlyPayment.value = '';
            UIDOM.length.value = '';
            setSaleDate(UIDOM.saleDate);
        } else {
            showToast("Error: " + result.message);
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('An error occurred while creating the account.');
    } finally {
        UIDOM.createAccountBtn.disabled = false;
        UIDOM.createAccountBtn.innerHTML = 'Create Account';
    }
}

// Close modals on outside click
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('open');
    }
};

UIDOM.createAccountBtn.addEventListener('click', () => {
    submitForm();
});

// Initialize data fetch when page loads
document.addEventListener('DOMContentLoaded', () => {
    fetchInitialData();
});
