import React, {useEffect, useState} from "react";
import {connect} from "react-redux";
import Event from "./Event";
import {checkEqualDates} from "../../Calendar/utils/date";


function DateDetail(props) {
    let year = props.date.getFullYear();
    let month = getMonth(props.date.getMonth());
    let day = getDay(props.date.getDate());
    let [events, setEvents] = useState(null);

    useEffect(() => {
        let currentEvents = props.store.dateDetail.filter(value => {
            return checkEqualDates(value.date, props.date)
        })
        if (currentEvents.length > 0) {
            setEvents(currentEvents[0].events)
        } else {
            setEvents(null)
        }
    }, [props.date])

    return (
        <div className="date-detail__wrapper">
            <div className="date-detail__header">
                <span>{day}.{month}.{year}</span>
            </div>
            {events ? 
            (<div className="date-detail__body">
                <main className="date-detail__main">
                    {events.map((event, index) => {
                        return<Event key={index}
                                     header={event.status ?
                                         "Лекция подтверждена" :
                                         "Лекция не подтверждена"}
                                     status={event.status}
                                     theme={event.theme}
                                     lecturer={event.lecturer}
                                     listener={event.listener}
                                     address={event.address}
                                     timeStart={event.timeStart}
                                     timeEnd={event.timeEnd}/>
                    } )}
                </main>
            </div>) : 
            (<div className="no-events">
                <p>На данный момент у Вас нет запланированных мероприятий.</p>
                <p>Вы можете создать одно или несколько мероприятий,
                    чтобы потенциальные слушатели могли откликнуться</p>
                <button className="create-event">Создать мероприятие</button>
            </div>
            )}
        </div>
    )
}

export default connect(
    state => ({store: state}),
    dispatch => ({})
)(DateDetail);


function getMonth(month) {
    let newMonth = month + 1;
    if (month < 9) {
        return "0" + newMonth;
    } else return newMonth;
}

function getDay(day) {
    if (day < 9) {
        return "0" + day;
    } else return day;
}
