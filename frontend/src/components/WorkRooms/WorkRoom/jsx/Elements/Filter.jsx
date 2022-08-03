import React, {useEffect, useState} from 'react'
import {connect} from 'react-redux'

import filterIcon from '~/assets/img/workrooms/workroom/filter.svg'
import filterActiveIcon from '~/assets/img/workrooms/workroom/filter-active.svg'
import {ActivateModal, DeactivateModal} from '../../../../Layout/redux/actions/header'
import {getCities} from '../../../../Profile/ajax/profile'
import DropDown from '../../../../Utils/jsx/DropDown'
import {getDomainArray} from '../../../CreateEvent/ajax/event'
import Tooltip from "../../../../Utils/jsx/Tooltip";

function Filter({filterCallBack, setData}) {
  let [isLoaded, setIsLoaded] = useState(true)
  let [filterActive, setFilterActive] = useState(false)
  let [domainArray, setDomainArray] = useState([])
  let [tooltipActive, setTooltipActive] = useState(false)

  let [selectedCity, setSelectedCity] = useState('')
  let [selectedDomain, setSelectedDomain] = useState('')
  let [selectedDomainName, setSelectedDomainName] = useState('')

  useEffect(() => {
    setSelectedDomainName('')
    setSelectedDomain('')
    setSelectedCity('')

    getDomainArray()
      .then(response => response.json())
      .then(data => setDomainArray(data.data))
      .catch(error => console.log(error))
  }, [])

  useEffect(() => {
    setIsLoaded(false)
    if (selectedCity || selectedDomain) {
      filterCallBack(selectedCity, selectedDomain)
        .then(r => r.json())
        .then(data => {
          setIsLoaded(true)
          setData(data.data)
        })
        .catch(e => console.log(e))
    }
  }, [selectedDomain, selectedCity])

  function handleClick() {
    if (filterActive) {
      filterCallBack()
        .then(r => r.json())
        .then(data => {
          setIsLoaded(true)
          setFilterActive(false)
          setSelectedDomain('')
          setSelectedDomainName('')
          setSelectedCity('')
          setData(data.data)
        })
        .catch(e => console.log(e))
    } else setFilterActive(true)
  }

  function domainSelectHandler(value, setValue) {
    for (let domain of domainArray) {
      if (domain.name === value) {
        setSelectedDomain(domain.id)
        setSelectedDomainName(domain.name)
      }
    }
    setValue('')
  }

  function activateToolip() {
    if (!filterActive) {
      setTooltipActive(true)
      setTimeout(() => setTooltipActive(false), 2000)
    }
  }

  return (
    <div className='workrooms__card__filter'>
      <div className="icon" onClick={handleClick}>
        <img src={filterActive ? filterActiveIcon : filterIcon}
             alt="Фильтр"
             onMouseOver={activateToolip}
             onMouseLeave={() => setTooltipActive(false)}/>
        <Tooltip text="Фильтры"
                 isVisible={tooltipActive}
                 corner="left-top"
                 position="side"
                 posL={40}
                 posT={20}/>
      </div>

      {filterActive &&
        <div className="filter">
          <div className="city">
            <span>Город</span>
            <DropDown request={getCities}
                      width={true}
                      input={true}
                      placeholder='Введите город'
                      onSelect={(value) => setSelectedCity(value)}/>
          </div>
          <div className="domain">
            <span>Тематика</span>
            <DropDown request={domainArray}
                      width={true}
                      placeholder='Выберите тематику'
                      onSelect={(value, setValue) => domainSelectHandler(value, setValue)}
                      domainArr={true}/>
            {selectedDomainName && <div className="selected-domain">{selectedDomainName}</div>}
          </div>
        </div>}
    </div>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    ActivateModal: () => dispatch(ActivateModal()),
    DeactivateModal: () => dispatch(DeactivateModal()),
  })
)(Filter)