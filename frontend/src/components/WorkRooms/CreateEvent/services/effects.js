import {getDomainArray} from '../ajax/event'
import {getLectureDetail} from "../../../Pages/Lecture/ajax/lecture";

export function singleRender(
  role, edit, SwapModalChooseDates, setRequiredFields, requiredFields, setDomainArray, setLectureData) {
  
  SwapModalChooseDates([])

  if (role === 'customer') setRequiredFields({...requiredFields, listeners: ''})
  getDomainArray()
    .then(response => response.json())
    .then(data => setDomainArray(data.data))
    .catch(error => console.log(error))
  
  if (edit !== null) {
    getLectureDetail(edit)
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        setLectureData(data.data[0])
      }
    })
    .catch(e => console.log(e))
  }
}

export function selectedDomainsRender(selectedDomains, domainArray, setDomainArray) {
    if (selectedDomains.length > 0 && domainArray) {
      let newDomainArray
      newDomainArray = domainArray.filter(elem => !selectedDomains.includes(elem.name))
      setDomainArray(newDomainArray)
    }
  }