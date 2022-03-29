import React, {useEffect, useState} from "react";
import {connect} from "react-redux";
import WorkroomCard from "./WorkroomCard";
import CreatedLectures from "~@/WorkRooms/WorkRoom/jsx/Elements/CreatedLectures";
import LectureCardList from "./Elements/LectureCardList";
import {getAllLecturesForCustomer} from "../ajax/workRooms";


function Customer(props) {
  let [potentialLectures, setPotentialLectures] = useState([])
  
  useEffect(() => {
    getAllLecturesForCustomer()
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') setPotentialLectures(data.data)
      })
      .catch(() => props.SetErrorMessage('get_all_lectures'))
  }, [])
    return (
        <article className="customer__content">
          <CreatedLectures role='customer' 
                           data={[]}/>
          <LectureCardList header='Новые лекции' 
                           data={potentialLectures}/>
        </article>
    )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(Customer);