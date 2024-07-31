document.addEventListener('DOMContentLoaded', (event) => {
    const addRowButton = document.getElementById('addRowButton');
    const table = document.getElementById('predictionTable').getElementsByTagName('tbody')[0];

    addRowButton.addEventListener('click', () => {
        const newRow = table.insertRow();

        const columns = ['N° LOYD NAVIRE','ETA_year', 'ETA_month', 'ETA_day', 'LONGUEUR NAVIRE', "TIRANT D'EAU",'NBTC import 2_old','NBTC import 4_old','tavg','wspd','pres'];
        
        columns.forEach(column => {
            const newCell = newRow.insertCell();
            const input = document.createElement('input');
            input.type = 'number';
            input.name = column;
            newCell.appendChild(input);
        });

        // Add cell for prediction output
        const outputCell2 = newRow.insertCell();
        const outputInput2 = document.createElement('input');
        outputInput2.type = 'number';
        outputInput2.name = 'NBTC2';
        outputInput2.disabled = true;
        newRow.appendChild(outputCell2).appendChild(outputInput2);

        // Add cell for prediction output
        const outputCell4 = newRow.insertCell();
        const outputInput4 = document.createElement('input');
        outputInput4.type = 'number';
        outputInput4.name = 'NBTC4';
        outputInput4.disabled = true;
        newRow.appendChild(outputCell4).appendChild(outputInput4);

        // Add cell for predict button
        const actionCell = newRow.insertCell();
        const predictButton = document.createElement('button');
        predictButton.textContent = 'Prédire';
        predictButton.classList.add('button');
        actionCell.appendChild(predictButton);

        predictButton.addEventListener('click', () => {
            const rowInputs = newRow.getElementsByTagName('input');
            const data = {};
            for (let input of rowInputs) {
                if (input.name !== 'NBTC2' && input.name !== 'NBTC4') {
                    data[input.name] = input.value;
                }
            }

            fetch('/predictConteneur2', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(result => {
                outputInput2.value = result.NBTC2;
            })
            .catch(error => console.error('Error:', error));

            fetch('/predictConteneur4', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(result => {
                outputInput4.value = result.NBTC4;
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
