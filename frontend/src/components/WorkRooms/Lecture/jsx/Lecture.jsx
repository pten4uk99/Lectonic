import React from "react";


function Lecture() {
  return (
    <div className="lecture__container">
      <div className="header__picture">
        
      </div>
      
      <div className="lecture__wrapper">
        
        <div className="left-block">
          <div className="lecture-photo">фото</div>
          <div className="status">статус</div>
          <div className="block__person">
            <div className="person-photo">фото</div>
            <div className="person-data">данные</div>
          </div>
          <div className="block__equipment">оборудование</div>
          <div className="block__cost">стоимость</div>
        </div>
        
        <div className="right-block">
          <div className="lecture-name">Доноры России</div>
          <div className="block__domains">тематики</div>
          <div className="block__dates">даты</div>
          <div className="block__address">адрес</div>
          <div className="block__description">описание</div>
          <button className="btn btn-response">Откликнуться</button>
        </div>
        
      </div>
    </div>
  );
}

export default Lecture;

