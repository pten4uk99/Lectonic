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
  
  /*добавление ссылок видео выступлений*/
  const [videoLinksList, setVideoLinksList] = useState([{videoLink: ''}]);
  console.log("videoLinksList: ", videoLinksList);
  
  function handleVideoLinkAdd() {
    setVideoLinksList([...videoLinksList, {videoLink: ''}]);
  };
  
  function handleVideoLinkChange (e, index) {
    const {name, value} = e.target;
    const list = [...videoLinksList];
    list[index][name] = value;
    setVideoLinksList(list);
  };

  /*добавление ссылок публикаций*/
  const [publicationList, setPublicationList] = useState([{publicationLink: ''}]);
  console.log("publicationList: ", publicationList);

  function handlePublicationAdd() {
    setPublicationList([...publicationList, {publicationLink: ''}]);
  };

  function handlePublicationChange (e, index) {
    const {name, value} = e.target;
    const list = [...publicationList];
    list[index][name] = value;
    setPublicationList(list);
  };
  
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
      
      {videoLinksList.map((singleVideoLink, index) => (
        <div key={index} className="step-block margin-bottom-24">
          <p className="step-block__left-part">
            {videoLinksList.length - videoLinksList.length === index  && "Ссылки на видео Ваших выступлений:"}
          </p>
          <input
            className='input__add-link'
            placeholder="https://"
            type="text"
            name="videoLink"
            id="videoLink"
            value={singleVideoLink.videoLink}
            onChange={(e) => handleVideoLinkChange(e, index)}
          />
          <Icons
            className='add-link__icon'
            srcNormal={addLinkIcon}
            srcHovered={addHoveredIcon}
            onClick={handleVideoLinkAdd}
            alt="добавить"/>
        </div>
      ))}

      {publicationList.map((singlePublication, index) => (
        <div key={index} className="step-block margin-bottom-24">
          <p className="step-block__left-part">
            {publicationList.length - publicationList.length === index  && "Ссылки на Ваши публикации:"}
          </p>
          <input
            className='input__add-link'
            placeholder="https://"
            type="text"
            name="publicationLink"
            id="publicationLink"
            value={singlePublication.publicationLink}
            onChange={(e) => handlePublicationChange(e, index)}
          />
          <Icons
            className='add-link__icon'
            srcNormal={addLinkIcon}
            srcHovered={addHoveredIcon}
            onClick={handlePublicationAdd}
            alt="добавить"/>
        </div>
      ))}
    </>
  )
}
