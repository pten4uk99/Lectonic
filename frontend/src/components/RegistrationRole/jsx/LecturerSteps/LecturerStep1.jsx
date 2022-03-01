import React, {useState} from 'react'
import DropDownTest from "../../../UserArea/jsx/DropDownTest";
import addLinkIcon from '~/assets/img/addLink-icon.svg'
import addHoveredIcon from '~/assets/img/add-icon-hover.svg'
import addActiveIcon from '~/assets/img/add-icon-active.svg'
import Icons from "../../../UserArea/jsx/Icons";
// import '~/styles/RegistrationRole.styl'

export default function LecturerStep1(props) {
  /*временно, потом темы будут подтягиваться с бэка*/
  let topicSelect = {
    class: 'topic-select',
    default: 'Выберете тематику',
    options: ['Лидеры-доноры', 'Клуб Эльбрус'],
  }
  
  /*добавление ссылок*/
  /*тут пока вопрос у меня*/
  let videoLinksArray = [
    {
     /* 'name' : '1',*/
      'value' : ''
    },
    {
      /* 'name' : '1',*/
      'value' : ''
    }
  ]
  
  const [videoLinks, setVideoLinks] = useState( videoLinksArray)
  function onChangeVideoLinks(e) {
    setVideoLinks( [...videoLinks, {value : e.target.value}] )
    //console.log('videoLinks: ', videoLinks)
    console.log('target: ', [...videoLinks])
  }

  let mappedVideoLinks = videoLinksArray.map((link, index) => {
    return <div key={index} className="step-block margin-bottom-24">
    <p className="step-block__left-part"></p>
    <input
      className='input__add-link'
      type="text"
      placeholder="https://"
    //  name={link.name}
      value={link.value}
      onChange={onChangeVideoLinks}/>
    <Icons
      className='add-link__icon'
      srcNormal={addLinkIcon}
      srcHovered={addHoveredIcon}
      onClick={addVideoLink}
      alt="добавить"/>
  </div> 
  })
  
  const [publicationLinks, setPublicationLinks] = useState({
    link1: '',
  })
  function onChangePublicationLinks(e) {
    setPublicationLinks({ ...publicationLinks, [e.target.name]: e.target.value })
    console.log('pubLinks: ', publicationLinks)
  }
  
  function addVideoLink() {
    videoLinksArray.push({
      'value' : ''
    })
    console.log("444", videoLinksArray)
  }
  
  return (
    <>
      <div className="step-block margin-bottom-24">
        <p className="step-block__left-part">
          Тематика лекций:
        </p>
        <DropDownTest
          className='topic-select'
          selectDetails={topicSelect}
          placeholder='Выберете тематику'
          style={{ width: '249px' }}/>
      </div>

      <div className="step-block margin-bottom-24">
        <p className="step-block__left-part">
          Ссылки на видео Ваших выступлений:
        </p>
        <input
          className='input__add-link'
          placeholder="https://"
          name="linkk1"
          value={videoLinks.linkk1}
          onChange={onChangeVideoLinks}/>
        <Icons
          className='add-link__icon'
          srcNormal={addLinkIcon}
          srcHovered={addHoveredIcon}
          alt="добавить"/>
      </div>

      <div className="step-block margin-bottom-24">
        <p className="step-block__left-part">
          Ссылки на Ваши публикации:
        </p>
        <input
          className='input__add-link'
          placeholder="https://"
          name="linkk1"
          value={publicationLinks.linkk1}
          onChange={onChangePublicationLinks}/>
        <Icons
          className='add-link__icon'
          srcNormal={addLinkIcon}
          srcHovered={addHoveredIcon}
          alt="добавить"/>
      </div>
      {mappedVideoLinks}
    </>
  )
}
