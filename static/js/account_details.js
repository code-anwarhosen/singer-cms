
let AccDetilsDOM = {
    newPaymentForm: document.getElementById('newPaymentForm'),

    paymentAmount: document.getElementById('paymentAmount'),
    receiptNumber: document.getElementById('receiptNumber'),
    paymentDate: document.getElementById('paymentDate'),

    paymentSubmitBtn: document.getElementById('paymentSubmitBtn'),
    paymentsTable: document.getElementById('paymentsTable'),
    cashBalance: document.getElementById('cashBalance'),
}

setSaleDate(AccDetilsDOM.paymentDate);

AccDetilsDOM.paymentSubmitBtn.addEventListener('click', () => {
    createNewPayment();
});



function addToPaymentTable(payment) {
    if (!payment) {
        return;
    }

    const paymentDate = new Date(payment.paymentDate);
    const formattedDate = paymentDate.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });

    // Create the row HTML as a string
    const rowData = `
        <tr class="even:bg-gray-700 odd:bg-gray-800 hover:bg-gray-600 transition-colors">
            <td class="p-3">${formattedDate || 'N\A'}</td>
            <td class="p-3">${payment.receiptId || 'N\A'}</td>
            <td class="p-3">${payment.paymentAmount || 'N\A'}</td>
        </tr>
    `;
    AccDetilsDOM.paymentsTable.insertAdjacentHTML('beforeend', rowData);

    // Update cashBalance 
    AccDetilsDOM.cashBalance.innerHTML = payment.cashBalance;
}


// Submit Form
async function createNewPayment() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    if (!csrfToken) {
        console.error('CSRF token not found!');
        return;
    }

    const formData = {
        paymentAmount: AccDetilsDOM.paymentAmount.value,
        receiptNumber: AccDetilsDOM.receiptNumber.value,
        paymentDate: AccDetilsDOM.paymentDate.value,
    }

    // Validate form data
    for (const [key, value] of Object.entries(formData)) {
        if (!value) {
            showToast(`Please fill in the "${key}" field.`);
            return;
        }
    }

    AccDetilsDOM.paymentSubmitBtn.disabled = true;
    AccDetilsDOM.paymentSubmitBtn.innerHTML = "Submitting...";

    const account = document.getElementById('hireAccountNumber').textContent;
    try {
        const response = await fetch(`/make-payment/${account}/`, {
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
            addToPaymentTable(result.data);
            toggleModal(false);

            AccDetilsDOM.paymentAmount.value = '';
            AccDetilsDOM.receiptNumber.value = '';
            setSaleDate(AccDetilsDOM.paymentDate);
        } else {
            showToast("Error: " + result.message);
        }
    } catch (error) {
        console.error('Error:' + error);
        showToast('An error occurred while creating the account.');
    } finally {
        AccDetilsDOM.paymentSubmitBtn.disabled = false;
        AccDetilsDOM.paymentSubmitBtn.innerHTML = "Create";
    }
}



// =========== Handles payment modal =====================
const openBtn = document.getElementById('openPaymentModal');
const closeBtn = document.getElementById('cancelModal');
const paymentModal = document.getElementById('paymentModal');

// Modal Animation Handling
function toggleModal(show) {
    if(show) {
        paymentModal.classList.remove('hidden');
        paymentModal.classList.add('flex');
        paymentModal.children[0].style.animation = 'paymentModalIn 0.1s ease-in';
    } else {
        paymentModal.children[0].style.animation = 'paymentModalOut 0.1s ease-out';
        setTimeout(() => paymentModal.classList.add('hidden'), 200);
        setTimeout(() => paymentModal.classList.remove('flex'), 100);
    }
}

// Event Listeners
openBtn.addEventListener('click', () => toggleModal(true));
closeBtn.addEventListener('click', () => toggleModal(false));
paymentModal.addEventListener('click', (e) => e.target === paymentModal && toggleModal(false));



// Close account section
function closeAccount(account) {
    askConfirmation("This action will close this account: " + account).then((confirmed) => {
        confirmed ? alert('Account is being closed') : alert('Account is not being closed');
    });
}
