import React, {useEffect, useState} from 'react'
import {connect} from 'react-redux'

import tooltip from '~/assets/img/workrooms/workroom/tooltip.svg'
import WorkroomCard from '../WorkroomCard'
import Loader from '../../../../Utils/jsx/Loader'
import {reverse} from '../../../../../ProjectConstants'
import {useNavigate} from 'react-router-dom'


function LecturersList(props){
  let [isLoaded, setIsLoaded] = useState(false)
  let navigate = useNavigate()
  
  useEffect(() => {
    if (props.data) setIsLoaded(true)
  }, [props.data])
  return (
    <section className="block__created-lectures">
      <div className="workroom__block-header">
        <span>Лекторы</span>
        <img src={tooltip} alt="Подсказка"/>
        {!isLoaded && <Loader size={15} left={12}/>}
      </div>
      
      <div className="cards-block mt-20">
        {props.isError ? 
          <div className="lecture-cards__error">Ошибка загрузки данных</div> :
          props.data.length > 0 && 
          <div className="created-lectures__wrapper">
            <div className="created-lectures">
              {props.data.map((lecturer, index) => {
                return <WorkroomCard key={index} 
                                     onClick={() => navigate(reverse('role_page', {lecturer: lecturer.user_id}))}
                                     data={{
                                       src: lecturer.photo,
                                       name: `${lecturer.last_name} \n ${lecturer.first_name} ${lecturer.middle_name}`,
                                       firstName: lecturer.first_name,
                                       lastName: lecturer.last_name,
                                       lectorCard: true,
                                       colorNumber: lecturer.bgc_number
                                     }}/>})}
          </div>
        </div>}
      </div>
      
      <div className="workroom__block-underline"/>
    </section>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(LecturersList)