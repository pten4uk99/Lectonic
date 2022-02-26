import React from 'react'
import { connect } from 'react-redux'
import photo1 from '~/assets/img/lecturer/photo1.svg'

function LectureCard(props) {
  return (
    <div className='lecture__card'>
      <div className='photo'>
        <img src={photo1} alt='' />
      </div>
      <div className='card-header'>Научные субботы</div>
      <div className='card-body'>
        Лекции от известных учёных о самых актуальных исследованиях
      </div>
      <button>Статус мероприятия</button>
    </div>
  )
}

export default connect(
  state => ({ store: state }),
  dispatch => ({})
)(LectureCard)
