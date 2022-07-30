import React, {useEffect, useState} from 'react'
import {connect} from 'react-redux'

import CreatedLectures from '~@/WorkRooms/WorkRoom/jsx/Elements/CreatedLectures'
import LectureCardList from './Elements/LectureCardList'
import {
  getAllLecturersForCustomer,
  getAllLecturesForCustomer, getConfirmedLectures,
  getCreatedLecturesForCustomer, getLecturesHistory
} from '../ajax/workRooms'
import LecturersList from './Elements/LecturersList'


function Customer(props) {
  let [createdLectures, setCreatedLectures] = useState([])
  let [potentialLectures, setPotentialLectures] = useState([])
  let [confirmedLectures, setConfirmedLectures] = useState([])
  let [lecturesHistory, setLecturesHistory] = useState([])
  let [lecturersList, setLecturersList] = useState([])
  
  let [createdError, setCreatedError] = useState(false)
  let [potentialError, setPotentialError] = useState(false)
  let [confirmedError, setConfirmedError] = useState(false)
  let [historyError, setHistoryError] = useState(false)
  let [lecturersError, setLecturersError] = useState(false)
  
  useEffect(() => {
    if (props.store.permissions.is_customer && props.store.permissions.logged_in) {
      getConfirmedLectures('lecturer')
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') setConfirmedLectures(data.data)
          else setConfirmedError(true)
        })
        .catch(() => setConfirmedError(true))
          
      getCreatedLecturesForCustomer()
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') setCreatedLectures(data.data)
          else setCreatedError(true)
        })
        .catch(() => setCreatedError(true))
      
      getAllLecturesForCustomer()
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') setPotentialLectures(data.data)
          else setPotentialError(true)
        })
        .catch(() => setPotentialError(true))
      
      getAllLecturersForCustomer()
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') setLecturersList(data.data)
          else setLecturersError(true)
        })
        .catch(() => setLecturersError(true))
    }
  }, [])
    return (
        <article className="customer__content">
          <CreatedLectures role='customer'
                           setData={setCreatedLectures}
                           data={createdLectures} 
                           isError={createdError}/>
          <LectureCardList header='Новые лекции' 
                           isLecturer={false}
                           filterCallBack={getAllLecturesForCustomer}
                           setData={setPotentialLectures}
                           data={potentialLectures} 
                           isError={potentialError}/>
          <LectureCardList header='Подтвержденные лекции' 
                           isLecturer={false} 
                           filterCallBack={(city, domain) => getConfirmedLectures('lecturer', city, domain)}
                           setData={setConfirmedLectures}
                           data={confirmedLectures} 
                           isError={confirmedError}/>
          <LecturersList data={lecturersList}
                         setData={setLecturersList}
                         filterCallBack={getAllLecturersForCustomer}
                         isError={lecturersError}/>
        </article>
    )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(Customer)