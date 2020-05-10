import React from 'react';
import NavigationItem from './NavigationItem/NavigationItem';
import classes from './NavigationItems.css';

const navigationItems = (props) => (
    <ul className={classes.NavigationItems}>
        <NavigationItem link={"/"} active>
            Train Environment
        </NavigationItem>
        <NavigationItem link={"/"}>
            Environments
        </NavigationItem>
    </ul>
);

export default navigationItems;