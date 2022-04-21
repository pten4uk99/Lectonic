import React, {useEffect, useState} from "react";
import {connect} from "react-redux";

import CreatedLectures from "~@/WorkRooms/WorkRoom/jsx/Elements/CreatedLectures";
import {getAllLecturesForLecturer, getCreatedLectures, getCreatedLecturesForLecturer} from "../ajax/workRooms";
import LectureCardList from "./Elements/LectureCardList";


function Lecturer(props){
  let [createdLectures, setCreatedLectures] = useState([])
  let [potentialLectures, setPotentialLectures] = useState([])

  useEffect(() => {
    getCreatedLecturesForLecturer()
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') setCreatedLectures(data.data)
      })
      .catch((error) => console.log(error))
    
    getAllLecturesForLecturer()
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') setPotentialLectures(data.data)
      })
      .catch((error) => console.log(error))
  }, [])
  
  return (
    <article className="lecturer__content">
      <CreatedLectures role='lecturer'
                       data={createdLectures} 
                       setData={setCreatedLectures}/>
      <LectureCardList header='Потенциальные заказы' 
                       isLecturer={true}
                       data={potentialLectures}/>
    </article>
  )
}


export default connect(
  state => ({store: state}),
  dispatch => ({})
)(Lecturer);