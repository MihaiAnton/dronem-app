import React, {Component} from 'react';
import TestComponent from "./components/TestComponent/TestComponent";
import axios from './axios-config';


const ws_url = 'ws://127.0.0.1:8000/ws/train_updates/';

class App extends Component {
    // componentDidMount() {
    //   const payload = {
    //       username: 'geobadita',
    //       email: 'geo.badita@gmail.com',
    //       password: 'qwertyuiop'
    //   }
    //   axios.post('api/users/signup/', payload)
    //       .then(response => console.log(response))
    //       .then(err => console.log(err));
    // }


    onWebSocketMessage(message) {
        try {
            let msg_json = JSON.parse(message);
            // console.log(msg_json)
            msg_json = msg_json['data'];
            let type = msg_json['type'];

            if (type === "PIPELINE_FEEDBACK" || type === "EVOLUTIONARY_FEEDBACK") {
                //moved to console view
            } else if (type === 'PROCESSED_DATA_PREVIEW') {
                let data = msg_json['data'];
                this.setState({converted_preview: data})
            } else if (type === "TRIED_MODEL") {
                //moved to convergence grid
            } else if (type === "EVOLUTIONARY_NEW_BEST_FEEDBACK") {
                //moved to epoch scores
            }

        } catch (error) {
            console.log("Error: ", error)
        }
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
            <div className="App">
                <button onClick={() => this.startWebSocket(1)}>BTN</button>
                <TestComponent/>
            </div>
        );
    }
}

export default App;
