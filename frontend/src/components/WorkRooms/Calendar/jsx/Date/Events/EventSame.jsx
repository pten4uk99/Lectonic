import React from "react";
import {connect} from "react-redux";

function EventSame(props) {

    return  (
            <div className="current-date-event-multiple">
                <div className={props.confirmed ? "event-same blue" : "event-same grey"}>
                    <span>{props.events.length}</span>
                </div>
            </div>
    )
}

export default connect(
    state => ({store: state.calendar}),
    dispatch => ({})
)(EventSame);