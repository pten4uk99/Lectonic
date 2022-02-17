import React from "react";
import {connect} from "react-redux";


function LectureCard(props) {
    return (
        <div className="potential__card">
            <div className="photo"><img src={props.photo} alt=""/></div>
            <div className="card-header">{props.header}</div>
            <div className="card-body">{props.body}</div>
            <button>Откликнуться</button>
        </div>
    )
}

export default connect(
    state => ({store: state}),
    dispatch => ({})
)(LectureCard);