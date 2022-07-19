import React from 'react'
import {connect} from 'react-redux'
import DataBlock from '../DataBlock'
import {reverse} from '../../../../../ProjectConstants'
import PhotoName from '../../../../Utils/jsx/PhotoName'
import {useNavigate} from 'react-router-dom'


function LectureCreator(props) {
  let navigate = useNavigate()
  let data = props.data

  function handleClick() {
    data?.creator_is_lecturer ?
      navigate(reverse('role_page', {lecturer: data.creator_user_id})) :
      navigate(reverse('role_page', {customer: data.creator_user_id}))
  }

  return (
    <DataBlock header={data?.creator_is_lecturer ? 'Лектор:' : 'Заказчик:'}>
      <div className="block__person" onClick={handleClick}>
        <div className="block__data">
          <div className="person-photo">
            {data?.creator_photo ?
              <img src={data.creator_photo} alt="фото"/> :
              data &&
              <PhotoName firstName={data?.creator_first_name}
                         lastName={data?.creator_last_name}
                         size={90}
                         colorNumber={data?.creator_bgc_number}/>
            }
          </div>
          <div className="person-data">
            <span>{data?.creator_last_name}</span>
            <span>{data?.creator_first_name}</span>
            <span>{data?.creator_middle_name}</span>
          </div>
        </div>
      </div>
    </DataBlock>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(LectureCreator)

