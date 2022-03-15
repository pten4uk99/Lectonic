import React, {useRef, useState} from 'react'
import downArrow from '~/assets/img/down-arrow.svg'


function CreateEvent() {
  let [titlePhotoSrc, setSrc] = useState('')
  
  function addPhotoHandler(inputEvent) {
    let file = inputEvent.target.files[0]
    let reader = new FileReader()
    reader.readAsDataURL(file);
    
    reader.onload = () => {
      console.log('Загружено блин')
      console.log(reader.result)
      setSrc(reader.result)
    }
  }
  
  return (
    <>
      <div className='create-event__wrapper'>
        <div className='heading'>
          <h1 className='main-heading'>Создание мероприятия</h1>
        </div>
        <div className='subheading'>
          <h2 className='main-subheading'>
            Вы можете создать одно или несколько мероприятий, чтобы потенциальне
            слушатели могли откликнуться.
          </h2>
        </div>
        
        <div className='cover-l label'> Обложка:</div>
        <label className='cover '>
          <img
            className='icon'
            src='assets/img/photo-icon.svg'
            alt='photo-icon'/>
            <span className='add-photo'>Добавить фото</span>
            <input className='add-photo__input' type='file' onChange={e => addPhotoHandler(e)}/>
          <img
            className='title-img'
            src={titlePhotoSrc}
            alt='Обложка'/>
        </label>
        
        <div className='domain-l label'>Тематика:</div>
        <div className='domains '>
          <div className='domain-list flex'>
            <select
              className='selector'
              style={{ backgroundImage: `url(${downArrow})` }}>
              <option value='' disabled selected>
                Выберите тематику
              </option>
              <option value='opt1'>opt1</option>
              <option value='opt2'>opt2</option>
              <option value='opt3'>opt3</option>
            </select>
            <div className='pill pill-grey'>Клуб Эльбрус</div>
            <div className='pill pill-grey'>Лидеры-доноры</div>
          </div>
        </div>
        <div className='topic-l label'>Тема лекции:</div>
        <div className='topic flex'>
          <input type='text' className='text-input' placeholder='Topic' />
        </div>
        <div className='type-l label'>Тип лекции:</div>
        <div className='type flex'>
          <div className='date-comp pill '>Онлайн</div>
          <div className='date-comp pill pill-blue'>Оффлайн</div>
          <div className='date-comp pill '>Гибрид</div>
        </div>
        <div className='date-l label'>Дата:</div>
        <div className='date flex'>
          <div className='date-comp pill pill-grey'>Дата</div>
          <div className='date-link'>Link</div>
        </div>
        <div className='time-l label'>Время:</div>
        <div className='time flex'>
          <span>
            c{' '}
            <select
              className='selector'
              style={{ backgroundImage: `url(${downArrow})` }}
            >
              <option value='' disabled selected>
                Now
              </option>
              <option value='opt1'>opt1</option>
              <option value='opt2'>opt2</option>
              <option value='opt3'>opt3</option>
            </select>
          </span>
          <span>
            {' '}
            до{' '}
            <select
              className='selector'
              style={{ backgroundImage: `url(${downArrow})` }}
            >
              <option value='' disabled selected>
                Then
              </option>
              <option value='opt1'>opt1</option>
              <option value='opt2'>opt2</option>
              <option value='opt3'>opt3</option>
            </select>
          </span>
        </div>
        <div className='workspace-l label'>Помещение для лекции:</div>
        <div className='workspace flex'>
          <div className='date-comp pill '>Есть</div>
          <div className='date-comp pill pill-blue'>Нет</div>
        </div>
        <div className='address-l label'>Адрес:</div>
        <div className='address flex'>
          <textarea
            name='lecture-address'
            rows='3'
            className='text-area'
            placeholder='Введите адрес помещения для лекции'
          ></textarea>
        </div>
        <div className='equip-l label'>Оборудование:</div>
        <div className='equip flex'>
          <textarea
            name='lecture-equipment'
            rows='3'
            className='text-area'
            placeholder='Перечислите имеющееся для лекции оборудование'
          ></textarea>
        </div>
        <div className='desc-l label'>Описание:</div>
        <div className='desc flex'>
          <textarea
            name='lecture-desc'
            rows='5'
            className='text-area'
            placeholder='Опишите лекцию'
          ></textarea>
        </div>
        <div className='fee-l label'>Цена лекции:</div>
        <div className='fee '>
          <div className='flex'>
            <div className='date-comp pill  pill-blue'>Платно</div>
            <div className='date-comp pill'>Бесплатно</div>
          </div>
          <input
            type='text'
            className='text-input'
            placeholder='Укажите цену'
          />
        </div>
        <div className='submit'>
          <button className='big-button'>Создать</button>
        </div>
      </div>
    </>
  )
}

export default CreateEvent

