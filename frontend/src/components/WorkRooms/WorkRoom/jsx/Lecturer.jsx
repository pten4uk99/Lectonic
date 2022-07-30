import React, {useEffect, useState} from 'react'
import {connect} from 'react-redux'

import CreatedLectures from '~@/WorkRooms/WorkRoom/jsx/Elements/CreatedLectures'
import {
  getAllCustomersForLecturer,
  getAllLecturesForLecturer,
  getConfirmedLectures,
  getCreatedLecturesForLecturer
} from '../ajax/workRooms'
import LectureCardList from './Elements/LectureCardList'
import CustomersList from "./Elements/CustomersList";


function Lecturer(props) {
  let [createdLectures, setCreatedLectures] = useState([])
  let [potentialLectures, setPotentialLectures] = useState([])
  let [confirmedLectures, setConfirmedLectures] = useState([])
  let [lecturesHistory, setLecturesHistory] = useState([])
  let [customersList, setCustomersList] = useState([])

  let [createdError, setCreatedError] = useState(false)
  let [potentialError, setPotentialError] = useState(false)
  let [confirmedError, setConfirmedError] = useState(false)
  let [historyError, setHistoryError] = useState(false)
  let [customersError, setCustomersError] = useState(false)
  
  useEffect(() => {
    if (props.store.permissions.is_lecturer && props.store.permissions.logged_in) {
      getConfirmedLectures('customer')
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') setConfirmedLectures(data.data)
          else setConfirmedError(true)
        })
        .catch(() => setConfirmedError(true))

      getCreatedLecturesForLecturer()
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') setCreatedLectures(data.data)
          else setCreatedError(true)
        })
        .catch(() => setCreatedError(true))

      getAllLecturesForLecturer()
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') setPotentialLectures(data.data)
          else setPotentialError(true)
        })
        .catch(() => setPotentialError(true))
    }

    getAllCustomersForLecturer()
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') setCustomersList(data.data)
        else setCustomersError(true)
      })
      .catch(() => setCustomersError(true))
  }, [])

  return (
    <article className="lecturer__content">
      <CreatedLectures role='lecturer'
                       data={createdLectures}
                       setData={setCreatedLectures}
                       isError={createdError}/>
      <LectureCardList header='Потенциальные заказы'
                       isLecturer={true}
                       filterCallBack={getAllLecturesForLecturer}
                       setData={setPotentialLectures}
                       data={potentialLectures}
                       isError={potentialError}/>
      <LectureCardList header='Подтвержденные лекции'
                       isLecturer={true}
                       filterCallBack={(city, domain) => getConfirmedLectures('customer', city, domain)}
                       setData={setConfirmedLectures}
                       data={confirmedLectures}
                       isError={confirmedError}/>
      <CustomersList data={customersList}
                     setData={setCustomersList}
                     filterCallBack={getAllCustomersForLecturer}
                     isError={customersError}/>
    </article>
  )
}


export default connect(
  state => ({store: state}),
  dispatch => ({})
)(Lecturer)