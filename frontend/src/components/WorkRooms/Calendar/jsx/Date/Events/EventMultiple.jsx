import React from "react";
import {connect} from "react-redux";

function EventMultiple(props) {
    let confirmedEvents = props.events.filter(event => event.status).length;
    let notConfirmedEvents = props.events.filter(event => !event.status).length;
    return (
        <>
            <div className="current-date-event-multiple">
                {confirmedEvents && notConfirmedEvents ?
                    props.dateHover ?
                        <>
                            <div className="event-multiple hover-grey">
                                <span>{notConfirmedEvents}</span>
                            </div>
                            <div className="event-multiple hover-blue">
                                <span>{confirmedEvents}</span>
                            </div>
                        </> :
                        <>
                            <div className="event-multiple half-grey">

                            </div>
                            <div className="event-multiple half-blue"/>
                            <span className="events-length">{props.events.length}</span>
                        </> :
                confirmedEvents ?
                    <div className="event-multiple blue">
                        <span>{props.events.length}</span>
                    </div> :
                notConfirmedEvents ?
                    <div className="event-multiple grey">
                        <span>{props.events.length}</span>
                    </div> :
                    <></>}
            </div>
        </>
    )          
}

export default connect(
    state => ({store: state.calendar}),
    dispatch => ({})
)(EventMultiple);