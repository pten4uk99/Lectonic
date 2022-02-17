import React, {useEffect, useState} from "react";
import {connect} from "react-redux";
import {WEEK_DAYS} from "../utils/calendar";
import {SetCheckedDate, SwapMonthToNext, SwapMonthToPrev} from "../../redux/actions/calendar";
import {checkEqualDates, checkNeedSwapToNextMonth, checkNeedSwapToPrevMonth} from "../utils/date";


function Date(props) {
    return (
        <div className={getClassName(props)} onClick={() => clickHandler(props)}>
            <span>{props.date.getDate()}</span>
            {props.date.getFullYear() === 2022 &&
        props.date.getMonth() === 1 &&
        props.date.getDate() === 18 ? (<div className="events-mini">
                <div className="blue"/>
                <div className="grey"/>
            </div>) : ""}
        </div>
    )
}

export default connect(
    state => ({store: state.calendar}),
    dispatch => ({
        SetCheckedDate:
            date => dispatch(SetCheckedDate(date)),
        SwapMonthToNext:
            () => dispatch(SwapMonthToNext()),
        SwapMonthToPrev:
            () => dispatch(SwapMonthToPrev()),
    })
)(Date);




function getClassName(props) {
    let className = "date";

    if (props.store.currentDate.getMonth() !==
        props.date.getMonth()) return "date inactive";
    else if (props.date.getDay() === WEEK_DAYS.Saturday ||
        props.date.getDay() === WEEK_DAYS.Sunday) className += " weekend";

    if (checkEqualDates(props.date, props.store.today)) className += " today"
    if (checkEqualDates(props.date, props.store.checkedDate)) className += " active"

    return className
}

function clickHandler(props) {
    if (checkNeedSwapToNextMonth(props.date, props.store.currentDate)) {
        props.SwapMonthToNext();
    } else if (checkNeedSwapToPrevMonth(props.date, props.store.currentDate)) {
        props.SwapMonthToPrev()
    }
    props.SetCheckedDate(props.date)
}