import React, {useEffect, useState} from "react";
import {connect} from "react-redux";
import {
    SetCheckedDate,
    SetHoverDate,
    SwapMonthToNext,
    SwapMonthToPrev
} from "../../redux/actions/calendar";
import {checkEqualDates, checkNeedSwapToNextMonth, checkNeedSwapToPrevMonth} from "../../utils/date";
import Events from "./Events/Events";


function Date(props) {
    let [hover, setHover] = useState(false);
    let [active, setActive] = useState(false);
    let [events, setEvents] = useState(null);

    useEffect(() => {
        let currentEvents = props.store.dateDetail.filter(value => {
            return checkEqualDates(value.date, props.date)
        })
        if (currentEvents.length > 0) setEvents(currentEvents[0].events);
        else setEvents(null);

        if (checkEqualDates(props.store.calendar.checkedDate, props.date)) setActive(true);
        else setActive(false);
    }, [props.date])

    useEffect(() => {
        if (checkEqualDates(props.store.calendar.hoverDate, props.date)) setHover(true);
        else setHover(false);
    }, [props.store.calendar.hoverDate])

    return (
            <div className={getClassName(props)}
                 onClick={() => clickHandler(props)}
                 onMouseEnter={() => {hoverHandler(props, true)}}
                 onMouseLeave={() => {hoverHandler(props, false)}}>
                <span>{props.date.getDate()}</span>
                <Events events={events}
                        dateHover={hover}
                        dateActive={active}/>
            </div>
    )
}

export default connect(
    state => ({store: state}),
    dispatch => ({
        SetCheckedDate:
            date => dispatch(SetCheckedDate(date)),
        SwapMonthToNext:
            () => dispatch(SwapMonthToNext()),
        SwapMonthToPrev:
            () => dispatch(SwapMonthToPrev()),
        SetHoverDate:
            (date) => dispatch(SetHoverDate(date)),
    })
)(Date);


function getClassName(props) {
    let className = "calendar-date";

    if (props.store.calendar.currentDate.getMonth() !==
        props.date.getMonth()) return "calendar-date inactive";

    if (checkEqualDates(props.date, props.store.calendar.today)) className += " today"
    if (checkEqualDates(props.date, props.store.calendar.hoverDate)) className += " active"

    return className
}

function clickHandler(props) {
    if (checkNeedSwapToNextMonth(props.date, props.store.calendar.currentDate)) {
        props.SwapMonthToNext();
    } else if (checkNeedSwapToPrevMonth(props.date, props.store.calendar.currentDate)) {
        props.SwapMonthToPrev()
    }
    props.SetCheckedDate(props.date)
}


function hoverHandler(props, enter) {

    if (props.store.calendar.currentDate.getMonth() !== props.date.getMonth()) {
        return props.SetHoverDate(props.store.calendar.checkedDate);
    }

    enter ?
        props.SetHoverDate(props.date) :
        props.SetHoverDate(props.store.calendar.checkedDate)
}
