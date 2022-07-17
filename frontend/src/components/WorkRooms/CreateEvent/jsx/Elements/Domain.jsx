import React, {useEffect, useState} from 'react'
import {connect} from 'react-redux'

import DropDown from '../../../../Utils/jsx/DropDown'
import btnDelete from '~/assets/img/btn-delete.svg'
import {ClearDomain, DeleteDomain, UpdateDomain} from '../../redux/actions/event'


function Domain(props) {
  let domainArray = props.domainArray
  let selectedDomains = props.selectedDomains
  let setDomainArray = props.setDomainArray
  let lectureData = props.lectureData
  
  useEffect(() => {props.ClearDomain()}, [])
  
  useEffect(() => {
    if (lectureData) for (let domain of lectureData.domain) props.UpdateDomain(domain)
  }, [lectureData])

  let [deletedDomain, setDeletedDomain] = useState({})

  function deleteElem(indexElem) {
    props.DeleteDomain(selectedDomains, indexElem)
    domainArray.push(deletedDomain)
    setDomainArray(domainArray.sort((a, b) => a.name > b.name ? 1 : -1))
  }

  function domainSelectHandler(value, setValue) {
    if (props.store.event.domain.length >= 10) return setValue('')
    props.UpdateDomain(value)
    setValue('')
  }

  return (
    <>
      <div className='domain-l label'>
        Тематика:
        <span className="required-sign step-block__required-sign">*</span>
      </div>
      <div className='domains'>
        <div className='domain-list flex'>
          <DropDown request={domainArray}
                    width={true}
                    placeholder='Выберите тематику'
                    onSelect={(value, setValue) => domainSelectHandler(value, setValue)}
                    domainArr={true}/>
        </div>
        <div className="step-block mt-12">
          <div className='domain-list flex'>
            {selectedDomains.map((domain, index) => {
              return <div key={index} className='pill pill-grey'
                          onMouseUp={() => {
                            setDeletedDomain({name: domain})
                          }}>
                {domain}
                <div className='pill-btn-delete'
                     onClick={() => deleteElem(index)}>
                  <img src={btnDelete} alt="delete"/>
                </div>
              </div>})}
            
          </div>
        </div>
      </div>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    ClearDomain: () => dispatch(ClearDomain()),
    UpdateDomain: (domain) => dispatch(UpdateDomain(domain)),
    DeleteDomain: (domain, i) => dispatch(DeleteDomain(domain, i)),
  })
)(Domain)
