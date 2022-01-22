let xhr = new XMLHttpRequest();

let query = deparam(location.search.slice(1));


function renderData(data) {
    let container = document.getElementsByClassName('rating-container')[0]
    for (let [name, objects] of Object.entries(data)) {
        console.log(name, objects);

        for (let [key, values] of Object.entries(objects)) {
            let newRow = document.createElement('div');
            newRow.className = 'panel';

            let keySpan = document.createElement('span');
            keySpan.innerText = '<' + name + '> ' +  key + ':';

            let valueSpan = document.createElement('span');
            valueSpan.style.float = 'right';

            valueSpan.innerText += values;

            newRow.appendChild(keySpan);
            newRow.appendChild(valueSpan);

            container.appendChild(newRow);
        }
    }

     _.template('test')
}

xhr.open('GET', '/get_timetable', true);

xhr.onload = function () {
    let data = {};

    for (let obj of JSON.parse(xhr.response)['objects']) {
        let name = obj[2];

        let key = obj[0];
        let value = obj[1];

        if (name in data) {
        } else {
            data[name] = {};
        }

        if (key in data[name]) {
            data[name][key] += ' ' + value;
        } else {
            data[name][key] = value;
        }
    }

    renderData(data);
}

xhr.send();

