import React, {useEffect, useState} from 'react'

import lectureBg from '~/assets/img/lecture-bg.png'
import backArrowWhite from '~/assets/img/back-arrow-white.svg'

import {useNavigate, useSearchParams} from 'react-router-dom'
import {reverse} from '../../../../ProjectConstants'
import {connect} from 'react-redux'
import {AddNotifications, RemoveNotification} from '../../../Layout/redux/actions/notifications'
import {UpdateLectureDetailChosenDates} from '../redux/actions/lectureDetail'
import Loader from '../../../Utils/jsx/Loader'
import {getLectureData} from '../services/server'
import LecturePhotoBlock from './Elements/LecturePhoto'
import LectureCreator from './Elements/LectureCreator'
import DataBlock from './DataBlock'
import Listeners from './Elements/Listeners'
import DomainList from './Elements/DomainList'
import LectureDatesBlock from './Elements/LectureDatesBlock'
import LectureResponseButton from './Elements/LectureResponseButton'
import LectureEditButton from './Elements/LectureEditButton'


function Lecture(props) {
  let [isLoaded, setIsLoaded] = useState(false)
  let [responseLoaded, setResponseLoaded] = useState(true)

  let userId = props.store.permissions.user_id
  let [searchParams, setSearchParams] = useSearchParams()
  let navigate = useNavigate()
  let lectureId = searchParams.get('id')

  let [lectureData, setLectureData] = useState(null)
  let [isCreator, setIsCreator] = useState(null)
  let [confirmedRespondent, setConfirmedRespondent] = useState(null)

  useEffect(() => {
    props.UpdateLectureDetailChosenDates([])

    getLectureData(userId, lectureId,
      setIsLoaded, setLectureData,
      setIsCreator, setConfirmedRespondent, navigate)
  }, [])

  if (!isLoaded) return <Loader main={true}/>
  return (
    <>
      <div className="navigate-back__block" onClick={() => navigate(reverse('workroom'))}>
        <img src={backArrowWhite} alt="назад" style={{fill: 'white'}}/>
      </div>

      <div className="lecture__container">
        <div className="header__picture">
          <img src={lectureBg} alt="задний фон"/>
        </div>

        <div className="lecture__wrapper">

          <div className="left-block">
            <LecturePhotoBlock data={lectureData}/>
            <LectureCreator data={lectureData}/>
            <DataBlock header='Оборудование в наличии:'
                       text={lectureData?.equipment || 'Нет'}/>
            <Listeners data={lectureData}/>
            <DataBlock header='Стоимость:' text={lectureData?.cost + ' р. / лекцию'}/>
          </div>

          <div className="right-block">
            <div className="lecture-name">{lectureData?.name}</div>
            <DomainList lectureData={lectureData}/>
            <LectureDatesBlock data={lectureData}/>
            <DataBlock header='Место проведения:'
                       text={lectureData?.hall_address || 'Не согласовано'}/>
            <DataBlock header='Описание:'
                       text={lectureData?.description || 'Нет'}
                       classNameModifier='block__description'/>

            <LectureResponseButton isCreator={isCreator}
                                   confirmedRespondent={confirmedRespondent}
                                   lectureId={lectureId}
                                   responseLoaded={responseLoaded}
                                   setResponseLoaded={setResponseLoaded}
                                   lectureData={lectureData}/>
          </div>

          {isCreator && <LectureEditButton lectureId={lectureId}
                                           creatorIsLecturer={lectureData?.creator_is_lecturer}
                                           canEdit={lectureData?.can_edit}/>}
        </div>
      </div>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    RemoveNotification: (data) => dispatch(RemoveNotification(data)),
    AddNotifications: (data) => dispatch(AddNotifications(data)),
    UpdateLectureDetailChosenDates: (dates) => dispatch(UpdateLectureDetailChosenDates(dates))
  })
)(Lecture)
