import React from "react";
import {connect} from "react-redux";
import tooltip from "~/assets/img/workrooms/workroom/tooltip.svg";


function LectureRequests(props){
    return (
        <section className="block__lecture-requests">
          <div className="lecture-requests__header">
            <span>Мои запросы на лекции</span>
            <img src={tooltip} alt="Подсказка"/>
          </div>
          
        </section>
    )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(LectureRequests);