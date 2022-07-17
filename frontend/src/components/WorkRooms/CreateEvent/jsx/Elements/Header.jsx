import React from 'react'
import {connect} from 'react-redux'


function Header(props) {
  let role = props.role
  let edit = props.edit

  let lecturerHeader = 'Создание мероприятия'
  let customerHeader = 'Создание заказа на мероприятие'

  let lecturerContent = 'Вы можете создать одно или несколько мероприятий, ' +
    'чтобы потенциальные слушатели могли откликнуться.'
  let customerContent = 'Вы можете создать один или несколько заказов на мероприятие, ' +
    'чтобы потенциальнее лекторы могли откликнуться.'
  return (
    <>
      <div className='heading'>
        <h1 className='main-heading'>{role === 'lecturer' ? lecturerHeader : customerHeader}</h1>
      </div>
      <div className='subheading'>
        <h2 className='main-subheading'>
          {role === 'lecturer' ? lecturerContent : customerContent}
        </h2>
      </div>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(Header)
