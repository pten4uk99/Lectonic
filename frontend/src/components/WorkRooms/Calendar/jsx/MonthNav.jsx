import React, {useEffect, useState} from "react";
import {connect} from "react-redux";
import {
    SwapMonthToNext, 
    SwapMonthToPrev
} from "../redux/actions/calendar";
import {MONTHS} from "../utils/calendar";
import {getEventsForMonth} from "../ajax/dateDetail";


function MonthNav(props) {
    let currentMonth = props.store.currentDate.getMonth();
    let currentYear = props.store.currentDate.getFullYear();
    
    let [events, setEvents] = useState(null);
    
    // useEffect(() => {
    //     getEventsForMonth()
    //       .then(response => response.json())
    //       .then(data => setEvents(data))
    //       .catch(error => console.log('Ошибка при получении данных:', error))
    // }, [])
    //
    // console.log(events)
    return (
        <nav className="month-nav">
            <div onClick={props.SwapMonthToPrev}><button className="left"/></div>
            <span>{getMonth(currentMonth)} {currentYear}</span>
            <div onClick={props.SwapMonthToNext}><button className="right"/></div>
        </nav>
    )
}

export default connect(
    state => ({store: state.calendar}),
    dispatch => ({
        SwapMonthToNext:
            () => dispatch(SwapMonthToNext()),
        SwapMonthToPrev:
            () => dispatch(SwapMonthToPrev()),
    })
)(MonthNav);


function getMonth(monthId) {
    return MONTHS[monthId];
}
