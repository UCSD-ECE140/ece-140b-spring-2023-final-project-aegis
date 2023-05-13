document.addEventListener("DOMContentLoaded", () => {

    let currentTempDisplay = document.getElementsByClassName('tempDisplay')[0];

    let messageForm = document.getElementsByClassName('messageForm')[0];

    let temperature=0.0;
    let humidity=0.0;
    let current=0.0;
    let time=0.0;
    let history;

    function server_request(url, data={}, verb, callback) {
        return fetch(url, {
            credentials: 'same-origin',
            method: verb,
            body: JSON.stringify(data),
            headers: {'Content-Type': 'application/json'}
        })
            .then(response => response.json())
            .then(response => {
                if(callback)
                    callback(response);
            })
            .catch(error => console.error('Error:', error));
    }

    function server_request_get(url, data={}, verb, callback) {
        return fetch(url, {
            credentials: 'same-origin',
            method: verb,
            headers: {'Content-Type': 'application/json'}
        })
            .then(response => response.json())
            .then(response => {
                if(callback)
                    callback(response);
            })
            .catch(error => console.error('Error:', error));
    }

    function getTemperature() {
        const action = '/recieve';
        const method = 'get';
        server_request_get(action,{}, method, function (response) {
            let points = response["data"].split(';')
            for (let point in points){
                let nums = point.split(',')
                time = nums[0]
                temperature = nums[1]
                humidity = nums[2]
                current = nums[3]

                history[time] = {"time":time,"temp":temperature, 'hum':humidity, 'current':current}
                updateCurrentDisplay()
                updateHistoryGraph1()
                updateHistoryGraph2()
                updateHistoryGraph3()
            }
        });
    }

    function updateCurrentDisplay() {
        currentTempDisplay.innerHTML = "Temperature: " + temperature + " Humidity: " + humidity + " Brightness: " + brightness + " Time: " + time;
    }

    messageForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const action = '/send';
        const method = 'post';
        const data = Object.fromEntries(new FormData(messageForm).entries());
        server_request(action, data, method, function (response) {
        });
    });

    function updateHistoryGraph1(){
        let xarray = [];
        let yarray = [];
        for (let key in history) {
            xarray.push(history[key]['time']);
            yarray.push(history[key]['temp']);
        }
        Plotly.newPlot( 'historicalDisplay1', [{
            x: xarray,
            y: yarray }], {
            margin: { t: 0 } } );
    }
    function updateHistoryGraph2(){
        let xarray = [];
        let yarray = [];
        for (let key in history) {
            xarray.push(history[key]['time']);
            yarray.push(history[key]['hum']);
        }
        Plotly.newPlot( 'historicalDisplay2', [{
            x: xarray,
            y: yarray }], {
            margin: { t: 0 } } );
    }
    function updateHistoryGraph3(){
        let xarray = [];
        let yarray = [];
        for (let key in history) {
            xarray.push(history[key]['time']);
            yarray.push(history[key]['current']);
        }
        Plotly.newPlot( 'historicalDisplay3', [{
            x: xarray,
            y: yarray }], {
            margin: { t: 0 } } );
    }


    // //call the updaters every 3 seconds
    // setInterval(function () {
    //     getTemperature();
    //     updateCurrentDisplay();
    //     updateHistoryGraph();
    // }, 1000);

});