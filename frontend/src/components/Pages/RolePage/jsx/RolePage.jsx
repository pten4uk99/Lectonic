import React, {useEffect, useState} from 'react'

import lecturerBackground from '~/assets/img/rolepage/rolepage_header_bg.svg';
import customerBackground from '~/assets/img/rolepage/customer-bg.png';
import backArrow from '~/assets/img/back-arrow-white.svg'
import LectureCardList from "../../../WorkRooms/WorkRoom/jsx/Elements/LectureCardList";
import {useNavigate, useSearchParams} from "react-router-dom";
import {getCustomerDetail, getLecturerDetail} from "../ajax/rolePage";
import PhotoName from "../../../Utils/jsx/PhotoName";
import {reverse} from "../../../../ProjectConstants";
import {
  getCreatedLecturesForCustomer,
  getCreatedLecturesForLecturer,
  getLecturesHistory
} from "../../../WorkRooms/WorkRoom/ajax/workRooms";
import Loader from "../../../Utils/jsx/Loader";


function RolePage(props) {
  let [isLoaded, setIsLoaded] = useState(false)
  let [lastLectures, setLastLectures] = useState(true);
  let [searchParams, setSearchParams] = useSearchParams()
  let navigate = useNavigate()
  let lecturerId = searchParams.get('lecturer')
  let customerId = searchParams.get('customer')
  
  let [data, setData] = useState(null)
  let [createdLecturesList, setCreatedLecturesList] = useState([])
  let [lecturesHistory, setLecturesHistory] = useState([])
  
  useEffect(() => {
    if (data) setIsLoaded(true)
  }, [data])
  
  useEffect(() => {
    if (lecturerId) {
      getLecturerDetail(lecturerId)
        .then(r => r.json())
        .then(data => setData(data.data[0]))
        .catch(e => console.log(e))
      
      getCreatedLecturesForLecturer(lecturerId)
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') setCreatedLecturesList(data.data)
        })
        .catch((error) => console.log(error))
    } else if (customerId) {
      getCustomerDetail(customerId)
        .then(r => r.json())
        .then(data => setData(data.data[0]))
        .catch(e => console.log(e))
      
      getCreatedLecturesForCustomer(customerId)
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') setCreatedLecturesList(data.data)
        })
        .catch((error) => console.log(error))
      
      getLecturesHistory('customer', customerId)
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') setLecturesHistory(data.data)
        })
        .catch((error) => console.log(error))
    }
  }, [])
  
  if (!isLoaded) return <Loader main={true}/>
  return (
    <>
      <div className="navigate-back__block"
           onClick={() => navigate(reverse('workroom'))}>
        <img src={backArrow} alt="назад"/>
      </div>
      
        <div className="rolepage__header" 
             style={{backgroundImage: `url(${customerId ? customerBackground : lecturerBackground})`}}/>
        <div className='container'>
            <div className='rolepage__title'>
                <div className='rolepage__img-wrapper'>
                  {data?.person.photo ?
                    <img src={data.person.photo} alt="photo"/> :
                    <PhotoName size={140} 
                               firstName={data?.person.first_name} 
                               lastName={data?.person.last_name} 
                               colorNumber={data?.person.bgc_number}/>
                  }
                </div>
                <div className='rolepage__title-box'>
                    <div className='rolepage__name'>
                        <span>{data?.person.first_name}</span>
                        <span>{data?.person.last_name}</span>
                    </div>
                    <div>
                        <div className='rolepage__tag tag-role'>{customerId ? "Заказчик" : "Лектор"}</div>
                        <div className='rolepage__tag tag-city'>г. {data?.person.city}</div>
                    </div>
                </div>
            </div>
            <div className='rolepage__description'>
                <div className='rolepage__box-1'>
                    <div className='rolepage__description-box'>
                      {customerId ? 
                        <span>{data?.company_name}</span> :
                        <>
                          <span>Лектор о себе:</span>
                          <p>{data?.person.description || "Нет"}</p>
                        </>}

                    </div>
                    <div className='rolepage__description-box'>
                      <span>{customerId ? "Описание:" : "Образование:"}</span>
                      <p>
                        {customerId ? 
                          (data?.company_description || "Нет") : 
                          (data?.education || "Не указано")}
                      </p>
                    </div>
                    <div className='rolepage__description-box'>
                        <span>{customerId ? "Сайт:" : "Ссылки на видео выступлений:"}</span>
                      {customerId ?
                        <div className='pill pill-grey'>
                          <a href={data?.company_site} target="_blank">{data?.company_site}</a>
                        </div> : 
                        (data?.performances_links?.length > 0 ? data.performances_links.map((elem, index) => {
                        return <div className='pill pill-grey' key={index}>
                          <a href={elem} target="_blank">{elem}</a>
                        </div>
                      }) : "Нет")}
                    </div>
                  {lecturerId && <div className='rolepage__description-box'>
                        <span>Ссылки на публикации:</span>
                      {data?.performances_links?.length > 0 ? data.publication_links.map((elem, index) => {
                        return <div className='pill pill-grey' key={index}>
                          <a href={elem} target="_blank">{elem}</a>
                        </div>
                      }) : "Нет"}
                    </div>}
                </div>
                <div className='rolepage__box-2'>
                    <div className='rolepage__description-box'>
                      <span>Тематики:</span>
                      {data?.domain.map((elem, index) => {
                        return <div className='pill pill-grey' key={index}>{elem}</div>
                      })}
                    </div>
                    <div className='rolepage__description-box'>
                        <span>Помещение для лекций:</span>
                        <p>{data?.optional.hall_address || "Нет"}</p>
                    </div>
                    <div className='rolepage__description-box'>
                        <span>Оборудование для лекций:</span>
                        <p>{data?.optional.equipment || "Нет"}</p>
                    </div>
                </div>
            </div>
        </div>
        <div>
            <div className='rolepage__lecture'>
              <div className='rolepage__line'/>
              <button>Будущие лекции</button>
              <div><LectureCardList data={createdLecturesList} inPage={true}/></div>
              
              <div className='rolepage__line rolepage__line-mt'/>
            </div>
        </div>
    </>
  )
}

export default RolePage;
