import React from "react";

import MonthNav from "./MonthNav";
import DatesList from "./DatesList/DatesList";
import DaysOfWeek from "./DaysOfWeek";
import {connect} from "react-redux";


function Calendar(props) {
    return (
        <div className="calendar__container">
            <div className="inside__container">
                <MonthNav/>
                <DaysOfWeek/>
                <DatesList/>
            </div>
        </div>
    )
}

export default connect(
    state => ({store: state.calendar}),
    dispatch => ({})
)(Calendar);