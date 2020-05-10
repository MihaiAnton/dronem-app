import React, { Component } from 'react';
import {TextField, Button} from "@material-ui/core";
import { withStyles } from "@material-ui/core/styles";

const useStyles =(theme) => ({
    root: {
        '& .MuiTextField-root': {
            margin: theme.spacing(1),
            width: 200,
        },
    },
});

class ConfigForm extends Component{
    state = {
        envName: null
    }

    modelNameChanged = (event) => {
        const newModelName = event.target.value;
        this.setState({envName: newModelName});
        console.log(this.state);
    }

    render() {
        const {classes} = this.props;
        return (
            <form className={classes.root} noValidate autoComplete={"off"}>
                <TextField label={"Environment"} onChange={(event) => this.modelNameChanged(event)}/>
                <Button variant="contained" color="primary" onClick={() => this.props.clicked(this.state)}>
                    Train
                </Button>
            </form>
        );
    }
}

export default withStyles(useStyles)(ConfigForm);