import React, {useEffect, useState} from 'react'
import {connect} from 'react-redux'

import tooltip from '~/assets/img/workrooms/workroom/tooltip.svg'
import WorkroomCard from '../WorkroomCard'
import Loader from '../../../../Utils/jsx/Loader'
import {reverse} from '../../../../../ProjectConstants'
import {useNavigate} from 'react-router-dom'
import Filter from "./Filter";


function CustomersList(props){
  let [isLoaded, setIsLoaded] = useState(false)
  let navigate = useNavigate()
  
  useEffect(() => {
    if (props.data) setIsLoaded(true)
  }, [props.data])
  return (
    <section className="block__created-lectures">
      <div className="workroom__block-header">
        <span>Заказчики</span>
        <Filter filterCallBack={props.filterCallBack} setData={props.setData}/>
        {/*<img src={tooltip} alt="Подсказка"/>*/}
        {!isLoaded && <Loader size={15} left={12}/>}
      </div>
      
      <div className="cards-block mt-20">
        {props.isError ? 
          <div className="lecture-cards__error">Ошибка загрузки данных</div> :
          props.data.length > 0 && 
          <div className="created-lectures__wrapper">
            <div className="created-lectures">
              {props.data.map((customer, index) => {
                return <WorkroomCard key={index} 
                                     onClick={() => navigate(reverse('role_page', {customer: customer.user_id}))}
                                     data={{
                                       src: customer.photo,
                                       name: `${customer.last_name} \n ${customer.first_name} ${customer.middle_name}`,
                                       firstName: customer.first_name,
                                       lastName: customer.last_name,
                                       lectorCard: true,
                                       colorNumber: customer.bgc_number
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
)(CustomersList)