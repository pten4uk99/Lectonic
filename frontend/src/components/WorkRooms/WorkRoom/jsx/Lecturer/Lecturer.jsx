import React from "react";
import {connect} from "react-redux";
import WorkroomCard from "../WorkroomCard";
import CreatedLectures from "~@/WorkRooms/WorkRoom/jsx/Lecturer/CreatedLectures";


function Lecturer(props){
    return (
        <article className="lecturer__content">
          
        </article>
    )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(Lecturer);