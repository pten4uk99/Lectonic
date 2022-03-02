import React from "react";
import {connect} from "react-redux";

function Event(props) {
    let className = "";

    props.confirmed ?
        className = "current-date-event blue" :
        className = "current-date-event grey";

    return (
        <div className={className}/>
    )
}

export default connect(
    state => ({store: state.calendar}),
    dispatch => ({})
)(Event);