import React, {Component} from 'react';
import Aux from '../../hoc/Aux/Aux';
import ConfigForm from "./ConfigForm/ConfigForm";
import DronemStats from "../../components/DronemStats/DronemStats";
import axios from '../../axios-config';
import Spinner from '../../components/UI/Spinner/Spinner';

class EnvironmentTrain extends Component {

    state = {
        completedForm: false,
        loading: false,
    }

    handleFormCompleted = (formData) => {
        this.setState({loading: true});
        const payload = {
            env_name: formData.envName
        }
        console.log("payload", payload);
        axios.post('/rl/train/', payload)
            .then((response) => {
                this.setState({
                    completedForm: true,
                    loading: false
                });
            })
            .catch(err => {console.log(err); this.setState({loading: false, completedForm: false})});
    }



    render() {
        let graph = null;
        let spinner = null;
        if (this.state.completedForm) {
            graph = <DronemStats/>
        }
        if(this.state.loading){
            spinner = <Spinner/>
        }
        return (
            <Aux>
                <ConfigForm clicked={this.handleFormCompleted}/>
                {graph}
                {spinner}
            </Aux>
        );
    }
}

export default EnvironmentTrain;