import React from "react";

import {connect} from "react-redux";

function DaysOfWeek(props) {
    return (
        <div className="days-of-week__container">
            <div className="days-of-week">
                {getDaysOfWeek().map((day, index)=> <div key={index} className="day-of-week">{day}</div> )}
            </div>
            <hr className="days-of-week__underline"/>
        </div>
    )
}

export default connect(
    state => ({store: state.calendar}),
    dispatch => ({})
)(DaysOfWeek);


function getDaysOfWeek() {
    return ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
}