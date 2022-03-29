import React, {useEffect, useState} from "react";
import {connect} from "react-redux";

import CreatedLectures from "~@/WorkRooms/WorkRoom/jsx/Elements/CreatedLectures";
import {getAllLecturesForLecturer} from "../ajax/workRooms";
import LectureCardList from "./Elements/LectureCardList";
import {SetErrorMessage} from "../../../Layout/redux/actions/header";


function Lecturer(props){
  let [potentialLectures, setPotentialLectures] = useState([])
  
  useEffect(() => {
    getAllLecturesForLecturer()
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') setPotentialLectures(data.data)
      })
      .catch(() => props.SetErrorMessage('get_all_lectures'))
  }, [])
  return (
    <article className="lecturer__content">
      <CreatedLectures role='lecturer' 
                       data={[]}/>
      <LectureCardList header='Потенциальные заказы' 
                         data={potentialLectures}/>
    </article>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    SetErrorMessage: (message) => dispatch(SetErrorMessage(message))
  })
)(Lecturer);