import React, { useEffect, useState } from 'react'
import { connect } from 'react-redux'
import Event from './Event'
import { checkEqualDates } from '~@/WorkRooms/FullCalendar/Calendar/utils/date'
import {useNavigate} from "react-router-dom";
import {reverse} from "../../../../../ProjectConstants";
import {SetCheckedDate} from "../../Calendar/redux/actions/calendar";


function DateDetail(props) {
  let navigate = useNavigate()
  
  let date = props.store.calendar.checkedDate
  let year = date?.getFullYear()
  let month = getMonth(date?.getMonth())
  let day = getDay(date?.getDate())
  let [events, setEvents] = useState(null)

  useEffect(() => {
    if (props.store.calendar.currentDate.getMonth() === date?.getMonth()) {
      let currentEvents = props.store.dateDetail.filter(value => {
        return checkEqualDates(value.date, date)
      })
      if (currentEvents.length > 0) setEvents(currentEvents[0].events) 
      else setEvents(null)
    }
  }, [date, props.store.dateDetail])

  return (
    <div className='date-detail__wrapper'>
      <div className='date-detail__header'>
        <span>
          {day}.{month}.{year}
        </span>
      </div>
      {events ? (
        <div className='date-detail__body'>
          <main className='date-detail__main'>
            {events.map((event, index) => {
              return (
                <Event
                  key={index}
                  header={
                    event.status
                      ? 'Подтвержденная лекция'
                      : 'Неподтвержденная лекция'
                  }
                  status={event.status}
                  name={event.name}
                  lecturer={event.lecturer}
                  listener={event.listener}
                  address={event.address}
                  timeStart={event.start}
                  timeEnd={event.end}
                />
              )
            })}
          </main>
        </div>
      ) : (
        <div className='no-events'>
          <p>На данный момент у Вас нет запланированных мероприятий.</p>
          <p>
            Вы можете создать одно или несколько мероприятий, чтобы
            потенциальные слушатели могли откликнуться
          </p>
          <button className='create-event' 
                  onClick={() => navigate(reverse('create_event'))}>Создать мероприятие</button>
        </div>
      )}
    </div>
  )
}

export default connect(
  state => ({ store: state }),
  dispatch => ({
    SetCheckedDate: (date) => dispatch(SetCheckedDate(date))
  })
)(DateDetail)


function getMonth(month) {
  let newMonth = month + 1
  if (month < 9) {
    return '0' + newMonth
  } else return newMonth
}

function getDay(day) {
  if (day < 9) {
    return '0' + day
  } else return day
}
