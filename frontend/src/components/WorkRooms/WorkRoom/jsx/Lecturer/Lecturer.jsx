import React from "react";
import {connect} from "react-redux";
import WorkroomCard from "../WorkroomCard";
import FullCalendar from "~@/WorkRooms/FullCalendar/FullCalendar";
import CreatedLectures from "~@/WorkRooms/WorkRoom/jsx/Lecturer/CreatedLectures";


function Lecturer(props){
    return (
        <article className="lecturer__content">
          <CreatedLectures/>
          <FullCalendar/>
        </article>
    )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(Lecturer);