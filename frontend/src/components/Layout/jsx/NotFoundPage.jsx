import React from 'react'


export default function NotFoundPage() {
  return (
    <>
      <div className='not-found'>
        <div className='not-found__text'>
          <h2>Ошибка</h2>
          <p>
            Что-то пошло не так! Страница, которую Вы запрашиваете, не
            существует.<br />
            Возможно, она была удалена или был введён неверный адрес в адресной строке.
          </p>
        </div>
        <div className='not-found__lectonic'>
          <div className='not-found__lectonic__head'>
            <div className='not-found__lectonic__head-face'/>
          </div>
          <div className='not-found__lectonic__eye-left'/>
          <div className='not-found__lectonic__eye-right'/>
          <div className='not-found__lectonic__body'/>
          <div className='not-found__lectonic__number'>404</div>
        </div>
      </div>
    </>
  )
}
