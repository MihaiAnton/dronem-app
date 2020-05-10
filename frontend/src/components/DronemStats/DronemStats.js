import React, { Component } from 'react';
import { LineChart } from 'react-chartkick';
import 'chart.js';

const defaultData = [
    {"name":"Average Reward", "data": {}},
    {"name":"Min Reward", "data": {}},
    {"name":"Max Reward", "data": {}}
];

const ws_url = 'ws://0.0.0.0:8000/ws/train_updates/';


class DronemStats extends Component{

    state = {
        data: defaultData,
        receivedData: false
    }

    onWebSocketMessage(message) {
        try {
            const msg_json = JSON.parse(message);
            const new_data = msg_json['data']
            const episodes = new_data['ep']
            const avgs = new_data['avg']
            const mins = new_data['min']
            const maxs = new_data['max']

            const newDataForState = defaultData;

            episodes.map((x, index) => {
                return [
                    newDataForState[0]["data"][x] = avgs[index].toFixed(2),
                    newDataForState[1]["data"][x] = maxs[index].toFixed(2),
                    newDataForState[2]["data"][x] = mins[index].toFixed(2),

                ]
            });
            console.log(mins)
            console.log(maxs)
            console.log(avgs)
            console.log(newDataForState)
            this.setState({data: newDataForState});

        } catch (error) {
            console.log("Error: ", error)
        }
    }

    componentDidMount() {
        this.startWebSocket(1);
    }

    startWebSocket(groupId) {
        let ws = new WebSocket(ws_url + groupId + "/");


        ws.onopen = () => {
            console.log("ws connected on " + groupId)
        };

        ws.onmessage = (event) => {
            // console.log("ws message");
            this.onWebSocketMessage(event.data)
        };

        ws.onclose = () => {
            console.log('ws disconnected')
        };

        this.setState({ws: ws})
    }


    render() {
        return (
            <LineChart data={this.state.data} />
        );
    }
}

export default DronemStats;