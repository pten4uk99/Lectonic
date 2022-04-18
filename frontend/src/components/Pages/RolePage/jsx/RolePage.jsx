import React, {useEffect, useState} from 'react'

import background from '~/assets/img/rolepage/rolepage_header_bg.svg';
import backArrow from '~/assets/img/back-arrow.svg'
import '../styles/RolePage.styl'
import LectureCardList from "../../../WorkRooms/WorkRoom/jsx/Elements/LectureCardList";
import {useNavigate, useSearchParams} from "react-router-dom";
import {getLecturerDetail} from "../ajax/rolePage";
import PhotoName from "../../../Utils/jsx/PhotoName";
import {reverse} from "../../../../ProjectConstants";
import {getCreatedLecturesForLecturer} from "../../../WorkRooms/WorkRoom/ajax/workRooms";


function RolePage(props) {
  const [lastLectures, setLastLectures] = useState(true);
  let [searchParams, setSearchParams] = useSearchParams()
  let navigate = useNavigate()
  let lecturerId = searchParams.get('lecturer')
  let customerId = searchParams.get('customer')
  
  let [data, setData] = useState(null)
  let [createdLecturesList, setCreatedLecturesList] = useState([])
  
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
      
    }
  }, [])

  return (
    <>
      <div className="navigate-back__block"
           onClick={() => navigate(reverse('workroom'))}>
        <img src={backArrow} alt="назад"/>
      </div>
      
        <div className="rolepage__header" style={{backgroundImage: `url(${background})`}}/>
        <div className='container'>
            <div className='rolepage__title'>
                <div className='rolepage__img-wrapper'>
                  {data?.person.photo ?
                    <img src={data.person.photo} alt="photo"/> :
                    <PhotoName size={140} 
                               firstName={data?.person.first_name} 
                               lastName={data?.person.last_name}/>
                  }
                </div>
                <div className='rolepage__title-box'>
                    <div className='rolepage__name'>
                        <span>{data?.person.first_name}</span>
                        <span>{data?.person.last_name}</span>
                    </div>
                    <div>
                        <div className='rolepage__tag tag-role'>Лектор</div>
                        <div className='rolepage__tag tag-city'>г. {data?.person.city.name}</div>
                    </div>
                </div>
            </div>
            <div className='rolepage__description'>
                <div className='rolepage__box-1'>
                    <div className='rolepage__description-box'>
                        <span>Лектор о себе:</span>
                        <p>{data?.person.description || "Нет"}</p>
                    </div>
                    <div className='rolepage__description-box'>
                        <span>Образование:</span>
                        <p>{data?.education || "Не указано"}</p>
                    </div>
                    <div className='rolepage__description-box'>
                        <span>Ссылки на видео выступлений:</span>
                      {data?.performances_links.length > 0 ? data.performances_links.map((elem, index) => {
                        return <div className='pill pill-grey' key={index}>{elem}</div>
                      }) : "Нет"}
                    </div>
                    <div className='rolepage__description-box'>
                        <span>Ссылки на публикации:</span>
                      {data?.performances_links.length > 0 ? data.publication_links.map((elem, index) => {
                        return <div className='pill pill-grey' key={index}>{elem}</div>
                      }) : "Нет"}
                    </div>
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
                <span onClick={() => setLastLectures(true)} className={lastLectures ? '' : 'no-active'}>
                  Проведеные лекции
                </span>
                <span onClick={() => setLastLectures(false)} className={!lastLectures ? '' : 'no-active'}>
                  Будущие лекции
                </span>
              
                <div>{lastLectures ?
                  <LectureCardList data={[]} inPage={true}/> : 
                  <LectureCardList data={createdLecturesList} inPage={true}/>
                }
                </div>
              
              <div className='rolepage__line rolepage__line-mt'/>
              {/*<button className='rolepage__lecture-btn'>Предложить заказ</button>*/}
            </div>
        </div>
    </>
  )
}

export default RolePage;
