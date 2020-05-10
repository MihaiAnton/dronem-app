import React from 'react';
import dronemLogo from '../../assets/images/logo/logo.png';
import classes from './Logo.css';

const Logo = (props) => (
    <div className={classes.Logo}>
        <img src={dronemLogo} alt={"Dronem"}/>
    </div>
);

export default Logo;