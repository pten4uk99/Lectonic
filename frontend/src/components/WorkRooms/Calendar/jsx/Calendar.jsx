import React, {useEffect, useState} from "react";

import MonthNav from "./MonthNav";
import DaysOfWeek from "./DaysOfWeek";
import {connect} from "react-redux";
import DatesListSwappable from "./Date/DatesListSwappable";


function Calendar(props) {
    return (
        <div className="calendar__container">
            <div className="inside__container">
                <MonthNav/>
                <DaysOfWeek/>
                <DatesListSwappable/>
            </div>
        </div>
    )
}

export default connect(
    state => ({store: state.calendar}),
    dispatch => ({})
)(Calendar);
