import React, {useState} from 'react'
import background from '~/assets/img/rolepage/rolepage_header_bg.svg';
import FuturedLectures from '~@/Pages/RolePage/jsx/FuturedLectures';
import GiveLectures from '~@/Pages/RolePage/jsx/GiveLectures';
import '../styles/RolePage.styl'


function RolePage(props) {
  const [lecture, setLecture] = useState('GiveLectures');

  return (
    <>
        <div className="rolepage__header" style={{backgroundImage: `url(${background})`}}></div>
        <div className='container'>
            <div className='rolepage__title'>
                <div className='rolepage__img-wrapper'>
                    <img src="" alt="photo"/>
                </div>
                <div className='rolepage__title-box'>
                    <div className='rolepage__name'>
                        <span>Анатолий</span>
                        <span>Новосельцев</span>
                    </div>
                    <div>
                        <div className='rolepage__tag tag-role'>Лектор</div>
                        <div className='rolepage__tag tag-city'>г. Москва</div>
                    </div>
                </div>
            </div>
            <div className='rolepage__description'>
                <div className='rolepage__box-1'>
                    <div className='rolepage__description-box'>
                        <span>Лектор о себе:</span>
                        <p>Здесь Анатолий Ефремович напишет о себе в свободной форме ограниченное количество символов (например, до 1000).</p>
                    </div>
                    <div className='rolepage__description-box'>
                        <span>Образование:</span>
                        <p>Образование высшее (2004-2010): Тольяттинский государственный университет, специальность «Графический дизайн».
                        В 2021 году в дополнение к высшему образованию, прошёл онлайн-обучение в школе Contented на курсе «Графический дизайн».
                        Также окончил художественную школу.</p>
                    </div>
                    <div className='rolepage__description-box'>
                        <span>Ссылки на видео выступлений:</span>
                        <div className='pill pill-grey'>https://www.figma.com/file/zBIPC7qTuiAsczXy1dsuoj/%D0%9B%D0%B5%D0%BA%D1%82%D0%BE%D0%BD%D0%B8%D0%BA?node-id=3960%3A54407</div>
                    </div>
                    <div className='rolepage__description-box'>
                        <span>Ссылки на публикации:</span>
                        <div className='pill pill-grey'>https://www.behance.net/razumeetsya</div>
                    </div>
                </div>
                <div className='rolepage__box-2'>
                    <div className='rolepage__description-box'>
                        <span>Тематики:</span>
                        <div className='pill pill-grey'>Дизайн</div>
                        <div className='pill pill-grey'>Архитектура</div>
                        <div className='pill pill-grey'>Театры</div>
                    </div>
                    <div className='rolepage__description-box'>
                        <span>Помещение для лекций:</span>
                        <p>г. Москва, БЦ «Весна», ул. Заречная, д. 12</p>
                    </div>
                    <div className='rolepage__description-box'>
                        <span>Оборудование для лекций:</span>
                        <p>Фотоаппарат, проектор</p>
                    </div>
                </div>
            </div>
        </div>
        <div>
            <div className='rolepage__lecture'>
                <div className='rolepage__line'></div>
                <span 
                    onClick={() => setLecture('GiveLectures')}
                    className={lecture === 'GiveLectures' ? '' : 'no-active'}>
                        Проведеные лекции
                </span>
                <span 
                    onClick={() => setLecture('FuturedLectures')} 
                    className={lecture === 'FuturedLectures' ? '' : 'no-active'}>
                        Будущие лекции
                </span>
                <div style={{display: lecture === 'GiveLectures' ? 'block' : 'none'}}>
                    <GiveLectures/>
                </div>
                <div style={{display: lecture === 'FuturedLectures' ? 'block' : 'none'}}>
                    <FuturedLectures/>
                </div>
                <div className='rolepage__line rolepage__line-mt'></div>
                <button className='rolepage__lecture-btn'>Предложить заказ</button>
            </div>
        </div>
    </>
  )
}

export default RolePage;
