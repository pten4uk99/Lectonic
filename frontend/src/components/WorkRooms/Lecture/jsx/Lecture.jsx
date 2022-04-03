import React from "react";


function Lecture() {
  return (
    <div >
      <div className="lecture__container">
            <div className="header">
                <div className="header__picture">
                  <div className="header__picture_label">
                    <div className="header__picture_label__text">Новые лекции</div>
                  </div>
                </div> 

                <div className="header__company_name">
                  <div className="header__company_name__text"> Доноры России </div>
                  <button className="button header__company_name__button_chat"> Пообщаться </button>
                  <button className="button header__company_name__button_response"> Откликнуться </button>
                </div>

                <p className="header__customer_text"> Заказчик</p>
                <p className="header__customer_logo"> Лого</p>

                <div className="header__project_card" >
                  <p className="header__project_card__customer_photo"> Фото </p>
                  <p className="header__project_card__customer_info"> Группа компаний "Газпром технологии" </p>
                  <p className="header__project_card__customer_info_name"> Петрова Анна <br></br> Александровна </p>
                </div>

            </div>

            <div className="body">

              <p className="body__about">О чём</p>
              <div className="body__title">
                Азбука донорства. Всё что нужно знать о донорстве.
              </div>
              <div className="body__article">1234</div>

              <button className=" button body__button_chat">Заказать</button>
              <button className="button body__button_order">Пообщаться</button>
            </div>
        </div>
    </div> 
  );
}

export default Lecture;

