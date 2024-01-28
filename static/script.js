// Функция для форматирования числа в сокращенной форме (тысячи, миллионы и т. д.)
let data = null;
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    } else {
        return num.toString();
    }
}

function fetchData() {
    fetch('/api/data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            var depositAmountElement = document.querySelector('.values-sidebar2 p.deposit-amount');

            if (depositAmountElement) {
                depositAmountElement.innerText = formatNumber(data.deposit_amount) + '₽';
            } else {
                console.error('Element deposit_amount not found.');
            }

            // Оставляем обновление других значений без изменений
            var editedElement = document.querySelector('.values-sidebar3 p.edited-created');
            var totalReceivedElement = document.querySelector('.values-sidebar1 p.total-received');

            if (editedElement && totalReceivedElement) {
                editedElement.innerText = data.edited + '/' + data.created;
                totalReceivedElement.innerText = data.total_received + '₽';
            } else {
                console.error('One or more elements not found.');
            }

            var scrollingList = document.getElementById('scrollingList');
            scrollingList.innerHTML = '';

            data.slot_names.forEach(function (slot, index) {
                var listItem = document.createElement('li');
                listItem.className = 'item';
                listItem.innerHTML = `<span>${index + 1} ${slot}</span> <span>${data.purchase_costs[index].toLocaleString('en-US')}</span> <span>${data.received_per_slot[index].toLocaleString('en-US')}</span>`;
                scrollingList.appendChild(listItem);
            });

            console.log('Данные успешно получены и обновлены:', data);
        })
        .catch(error => console.error('Ошибка загрузки данных:', error));
}

window.addEventListener('load', function () {
fetchData();
setInterval(fetchData, 6000);
var listContainer = document.getElementById('listContainer');
var scrollingList = document.getElementById('scrollingList');
})


function submitTheme() {
    var selectedTheme = document.getElementById('theme-selector').value;
    console.log('Selected theme:', selectedTheme);

    fetch('/apply_theme', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ theme: selectedTheme })
    }).then(function(response) {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(function(data) {
        console.log('Theme updated:', data);
        // Reload the page to apply the new theme
        window.location.reload();
    }).catch(function(error) {
        console.error('Error updating theme:', error);
    });
}

// Example using fetch API
fetch('/login', {
    method: 'POST',
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));


function checkOverflow() {
var isOverflowing = scrollingList.offsetHeight > listContainer.offsetHeight;

if (isOverflowing) {
    var newItem = document.createElement("li");
    newItem.textContent = "Новый элемент";
    document.getElementById("scrollingList").appendChild(newItem);
} else {
    scrollingList.style.animation = 'none';
}
}

window.addEventListener('resize', checkOverflow);
checkOverflow(); // Вызываем при загрузке страницы
;
