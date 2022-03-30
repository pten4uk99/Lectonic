import React from 'react'
import background from '~/assets/img/rolepage/rolepage_header_bg.svg';
import '../styles/RolePage.styl'


function RolePage(props) {
  return (
    <>
        <div className="rolepage__header" style={{backgroundImage: `url(${background})`}}>
            <div className='rolepage__option'>
                <span>Лектор</span>    
            </div>
        </div>
        <div className='container'>
            <div className='rolepage__title'>
                <div className='rolepage__title-box'>
                    <span>Homer</span>
                    <span>Jay</span>
                    <span>Simpson</span>
                </div>
                <div className='rolepage__title-box'>
                    <button className='btn-first'>Пообщаться</button>
                    <button className='btn-second'>Предложить лекцию</button>
                </div>
            </div>
            <div className='rolepage__section'>
                <span>Лектор</span>
                <div className='rolepage__img-wrapper'>
                    <img src="https://www.sostav.ru/app/public/images/news/2015/12/18/Screenshot_2.jpg?rand=0.2807936074677855" alt="photo"/>
                </div>
            </div>
            <div className='rolepage__about'>
                <span>О лекторе</span>
                <div className='rolepage__line'></div>
            </div>
            <div className='rolepage__lecture'>
                <span>Проведеные лекции</span>
                <span className='no-active'>Будущие лекции</span>
                <div className='rolepage__line'></div>
            </div>
        </div>
    </>
  )
}

export default RolePage;
