import React, {useEffect, useState} from "react";
import {connect} from "react-redux";


function Event(props) {
    let [className, setClass] = useState("left-block");
    useEffect(() => {
        if (props.status) setClass("left-block grey");
    }, [])
    return (
        <li className="date-detail__event">
            <div className={className}>
                <div className="circle"/>
                <div className="dynamic-circle"/>
            </div>
            <div className="event-info">
                <div className="header">{props.header}</div>
                <div className="theme">Тема: <span>{props.theme}</span></div>
                <div className="lecturer">Лектор: <span>{props.lecturer}</span></div>
                <div className="listener">Слушатель: <span>{props.listener}</span></div>
                <div className="address">Место: <span>{props.address}</span></div>
            </div>
            <div className="time-range">
                <span className="start">10:00</span>
                <span className="end">12:00</span>
            </div>
        </li>
    )
}

export default connect(
    state => ({store: state.dateDetail}),
    dispatch => ({})
)(Event);