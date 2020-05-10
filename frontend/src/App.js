import React, {Component} from 'react';
import DronemStats from "./components/DronemStats/DronemStats";
import Layout from "./hoc/Layout/Layout";
import EnvironmentTrain from "./containers/EnvironmentTrain/EnvironmentTrain";

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
    // <div className={classes.App}>
    // {/*<DronemStats/>*/}
    //
    // </div>

    render() {
        return (
            <Layout>
                <EnvironmentTrain/>
            </Layout>
        );
    }
}

export default App;
